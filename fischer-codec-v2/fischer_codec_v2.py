#!/usr/bin/env python3
"""FISCHER-CODEC-v2: restore-gated black/white context tournament.

Five BLACK experts predict from decoder-known left context. Five WHITE experts
predict from decoder-known right context. The legal two-sided path uses a pyramid
coding order that establishes anchors before interior symbols. A Fischer tournament
selects, per block, between a conventional forward path and the valid two-sided path.

No future byte is used before the decoder can know it. `oracle` is a separate
non-codec audit that intentionally uses true future bytes and is labeled as such.
"""
from __future__ import annotations
import argparse, hashlib, json, math, struct, time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

TOP=1<<24; BOT=1<<16; MASK32=0xFFFFFFFF; TOT=1<<16
MASK64=(1<<64)-1
MAGIC=b'FSC2'; VERSION=1
DIRECTIONS=('black','white')

class RangeEncoder:
    def __init__(self): self.low=0; self.rng=MASK32; self.out=bytearray()
    def bit(self,bit:int,p1:int)->None:
        p1=max(1,min(TOT-1,int(p1)));p0=TOT-p1;r=self.rng//TOT
        if bit:self.low=(self.low+p0*r)&MASK32;self.rng=p1*r
        else:self.rng=p0*r
        while True:
            if ((self.low^((self.low+self.rng)&MASK32))&MASK32)<TOP:pass
            elif self.rng<BOT:self.rng=(-self.low)&(BOT-1)
            else:break
            self.out.append((self.low>>24)&255);self.low=(self.low<<8)&MASK32;self.rng=(self.rng<<8)&MASK32
    def finish(self)->bytes:
        for _ in range(4):self.out.append((self.low>>24)&255);self.low=(self.low<<8)&MASK32
        return bytes(self.out)

class RangeDecoder:
    def __init__(self,data:bytes):
        self.data=data;self.pos=4;self.low=0;self.rng=MASK32;self.code=int.from_bytes(data[:4].ljust(4,b'\0'),'big')
    def bit(self,p1:int)->int:
        p1=max(1,min(TOT-1,int(p1)));p0=TOT-p1;r=self.rng//TOT;target=((self.code-self.low)&MASK32)//r
        if target<p0:bit=0;self.rng=p0*r
        else:bit=1;self.low=(self.low+p0*r)&MASK32;self.rng=p1*r
        while True:
            if ((self.low^((self.low+self.rng)&MASK32))&MASK32)<TOP:pass
            elif self.rng<BOT:self.rng=(-self.low)&(BOT-1)
            else:break
            nxt=self.data[self.pos] if self.pos<len(self.data) else 0;self.pos+=1
            self.code=((self.code<<8)|nxt)&MASK32;self.low=(self.low<<8)&MASK32;self.rng=(self.rng<<8)&MASK32
        return bit

@dataclass(frozen=True)
class Task:
    index:int;left:tuple[int,...];right:tuple[int,...];stage:int

@lru_cache(maxsize=64)
def sequential_tasks(n:int)->tuple[Task,...]:
    return tuple(Task(i,tuple(range(i-1,max(-1,i-6),-1)),(),0) for i in range(n))

@lru_cache(maxsize=256)
def pyramid_tasks(n:int,stride:int)->tuple[Task,...]:
    if n<=0:return ()
    anchors=list(range(0,n,stride))
    if not anchors or anchors[-1]!=n-1:anchors.append(n-1)
    tasks=[Task(pos,tuple(reversed(anchors[max(0,i-5):i])),(),0) for i,pos in enumerate(anchors)]
    known=sorted(set(anchors));intervals=[(known[i],known[i+1]) for i in range(len(known)-1) if known[i+1]-known[i]>1]
    import bisect
    stage=1
    while intervals:
        mids=[];nxt=[]
        for l,r in intervals:
            if r-l<=1:continue
            m=(l+r)//2;j=bisect.bisect_left(known,m)
            left=tuple(reversed(known[max(0,j-5):j]));right=tuple(known[j:min(len(known),j+5)])
            tasks.append(Task(m,left,right,stage));mids.append(m)
            if m-l>1:nxt.append((l,m))
            if r-m>1:nxt.append((m,r))
        known=sorted(known+mids);intervals=nxt;stage+=1
    assert len(tasks)==n and len({t.index for t in tasks})==n
    return tuple(tasks)

class HashedExpert:
    def __init__(self,direction:str,order:int):
        self.direction=direction;self.order=order
        bits={1:15,2:17,3:18,4:18,5:18}[order]
        self.size=1<<bits;self.mask=self.size-1;self.counts=bytearray(self.size*2)
        self.loss_bits=0.0;self.bits=0;self.correct=0;self.blunders=0;self.touched=0
        self.seed=(0x9E3779B97F4A7C15 if direction=='black' else 0xD1B54A32D192ED03)^(order*0x94D049BB133111EB)
    def _slot(self,chain:tuple[int,...],stage:int,bitpos:int,prefix:int)->int:
        h=(self.seed^(min(stage,15)*0x9E3779B185EBCA87)^(bitpos*0xC2B2AE3D27D4EB4F)^prefix)&MASK64
        ctx=chain[:self.order];h^=len(ctx)*0x165667B19E3779F9
        for v in ctx:
            h^=(v+0x9E3779B9)&MASK64;h=(h*0x100000001B3)&MASK64;h^=h>>32
        return (h&self.mask)*2
    def predict(self,chain:tuple[int,...],stage:int,bitpos:int,prefix:int)->int:
        i=self._slot(chain,stage,bitpos,prefix);c0=self.counts[i];c1=self.counts[i+1]
        return max(1,min(TOT-1,((2*c1+1)*TOT)//(2*(c0+c1)+2)))
    def update(self,chain:tuple[int,...],stage:int,bitpos:int,prefix:int,bit:int,p1:int)->None:
        i=self._slot(chain,stage,bitpos,prefix);c0=self.counts[i];c1=self.counts[i+1]
        if c0==0 and c1==0:self.touched+=1
        if c0+c1>=250:c0=(c0+1)//2;c1=(c1+1)//2
        if bit:c1=min(255,c1+1)
        else:c0=min(255,c0+1)
        self.counts[i]=c0;self.counts[i+1]=c1
        pa=(p1 if bit else TOT-p1)/TOT;self.loss_bits+=-math.log2(max(pa,1/TOT));self.bits+=1
        if (p1>=TOT//2)==bool(bit):self.correct+=1
        if pa<.1:self.blunders+=1
    def digest(self)->bytes:return hashlib.sha256(self.counts).digest()

class ContextMixer:
    def __init__(self,n:int,power:int=4):
        self.n=n;self.power=power;self.trust:dict[tuple,list[int]]={};self.loss_bits=0.0;self.bits=0
        self.weight_mass=[0.0]*n;self.steps=0
    @staticmethod
    def cls(v:int|None)->int:
        if v is None:return 0
        if v in (9,10,13,32):return 1
        if 97<=v<=122:return 2
        if 65<=v<=90:return 3
        if 48<=v<=57:return 4
        if v<32 or v==127:return 5
        if v>=128:return 6
        if v in b'.,;:!?-_/\\"\'()[]{}<>=':return 7
        return 8
    def key(self,task:Task,buf:bytearray,bitpos:int)->tuple:
        lv=buf[task.left[0]] if task.left else None;rv=buf[task.right[0]] if task.right else None
        return bitpos,min(task.stage,7),self.cls(lv),self.cls(rv)
    def weights(self,key:tuple)->list[int]:
        w=self.trust.get(key)
        if w is None:w=[TOT//2]*self.n;self.trust[key]=w
        return w
    def predict(self,probs:list[int],key:tuple)->int:
        ws=self.weights(key);eff=[w**self.power for w in ws];den=sum(eff);logit=0.0
        for j,(w,p) in enumerate(zip(eff,probs)):
            q=max(1e-6,min(1-1e-6,p/TOT));logit+=w*math.log(q/(1-q));self.weight_mass[j]+=w/den
        self.steps+=1;logit/=den
        mix=1e-12 if logit<=-40 else (1-1e-12 if logit>=40 else 1/(1+math.exp(-logit)))
        return max(1,min(TOT-1,int(round(mix*TOT))))
    def update(self,probs:list[int],key:tuple,bit:int,p_mix:int)->None:
        ws=self.weights(key)
        for j,p in enumerate(probs):
            reward=p if bit else TOT-p;ws[j]=max(16,min(TOT-16,(15*ws[j]+reward)//16))
        pa=(p_mix if bit else TOT-p_mix)/TOT;self.loss_bits+=-math.log2(max(pa,1/TOT));self.bits+=1
    def digest(self)->bytes:
        h=hashlib.sha256()
        for k in sorted(self.trust):h.update(repr(k).encode());h.update(struct.pack('>'+('H'*len(self.trust[k])),*self.trust[k]))
        return h.digest()

class ModelState:
    def __init__(self,mode:str):
        spec=[]
        if mode in ('black','both'):spec += [('black',o) for o in range(1,6)]
        if mode in ('white','both'):spec += [('white',o) for o in range(1,6)]
        self.mode=mode;self.experts=[HashedExpert(d,o) for d,o in spec];self.mixer=ContextMixer(len(self.experts),4)
    def predict(self,buf:bytearray,task:Task,bitpos:int,prefix:int):
        left=tuple(buf[i] for i in task.left);right=tuple(buf[i] for i in task.right);probs=[];chains=[]
        for ex in self.experts:
            ch=left if ex.direction=='black' else right;chains.append(ch);probs.append(ex.predict(ch,task.stage,bitpos,prefix))
        key=self.mixer.key(task,buf,bitpos);return probs,chains,key,self.mixer.predict(probs,key)
    def update(self,task:Task,bitpos:int,prefix:int,bit:int,probs,chains,key,p_mix:int):
        self.mixer.update(probs,key,bit,p_mix)
        for ex,ch,p in zip(self.experts,chains,probs):ex.update(ch,task.stage,bitpos,prefix,bit,p)
    def digest(self)->str:
        h=hashlib.sha256();h.update(self.mixer.digest())
        for ex in self.experts:h.update(ex.digest())
        return h.hexdigest()
    def report(self)->dict[str,Any]:
        mass=self.mixer.weight_mass;den=sum(mass) or 1;best=min(ex.loss_bits/max(1,ex.bits) for ex in self.experts)
        rows=[]
        for ex,w in zip(self.experts,mass):
            avg=ex.loss_bits/max(1,ex.bits);rows.append({'expert':f'{ex.direction}-o{ex.order}','direction':ex.direction,'order':ex.order,
             'ideal_bpb':avg,'trust_pct':100*w/den,'accuracy':ex.correct/max(1,ex.bits),'blunders':ex.blunders,
             'table_bytes':len(ex.counts),'slots_touched':ex.touched,'cpl_vs_best':round(1000*max(0,avg-best))})
        return {'mode':self.mode,'mixer_ideal_bpb':self.mixer.loss_bits/max(1,self.mixer.bits),'state_sha256':self.digest(),
                'black_trust_pct':sum(x['trust_pct'] for x in rows if x['direction']=='black'),
                'white_trust_pct':sum(x['trust_pct'] for x in rows if x['direction']=='white'),'experts':rows}

def tasks(n:int,schedule:str,stride:int):return sequential_tasks(n) if schedule=='sequential' else pyramid_tasks(n,stride)

def encode_block(raw:bytes,state:ModelState,schedule:str,stride:int)->bytes:
    enc=RangeEncoder();buf=bytearray(raw)
    for task in tasks(len(raw),schedule,stride):
        value=raw[task.index];prefix=0
        for bitpos in range(8):
            bit=(value>>(7-bitpos))&1;probs,chains,key,p=state.predict(buf,task,bitpos,prefix);enc.bit(bit,p)
            state.update(task,bitpos,prefix,bit,probs,chains,key,p);prefix=(prefix<<1)|bit
    return enc.finish()

def decode_block(payload:bytes,n:int,state:ModelState,schedule:str,stride:int)->bytes:
    dec=RangeDecoder(payload);buf=bytearray(n)
    for task in tasks(n,schedule,stride):
        value=0;prefix=0
        for bitpos in range(8):
            probs,chains,key,p=state.predict(buf,task,bitpos,prefix);bit=dec.bit(p);value=(value<<1)|bit
            state.update(task,bitpos,prefix,bit,probs,chains,key,p);prefix=(prefix<<1)|bit
        buf[task.index]=value
    return bytes(buf)

def replay_block(raw:bytes,state:ModelState,schedule:str,stride:int)->None:
    buf=bytearray(raw)
    for task in tasks(len(raw),schedule,stride):
        value=raw[task.index];prefix=0
        for bitpos in range(8):
            bit=(value>>(7-bitpos))&1;probs,chains,key,p=state.predict(buf,task,bitpos,prefix)
            state.update(task,bitpos,prefix,bit,probs,chains,key,p);prefix=(prefix<<1)|bit

def tournament_encode(data:bytes,block_size:int=16384,stride:int=4)->tuple[bytes,dict]:
    black=ModelState('black');both=ModelState('both');body=bytearray();choices=[];sum_black=sum_both=0
    for block_no,off in enumerate(range(0,len(data),block_size)):
        raw=data[off:off+block_size];pb=encode_block(raw,black,'sequential',stride);pw=encode_block(raw,both,'pyramid',stride)
        sum_black+=len(pb);sum_both+=len(pw);mode=0 if len(pb)<=len(pw) else 1;selected=pb if mode==0 else pw
        body += struct.pack('>BII',mode,len(raw),len(selected))+selected
        choices.append({'block':block_no,'raw_bytes':len(raw),'black_bytes':len(pb),'blackwhite_bytes':len(pw),
                        'selected':'black-sequential' if mode==0 else 'blackwhite-pyramid','selected_bytes':len(selected),
                        'delta_black_minus_blackwhite':len(pb)-len(pw)})
    header=MAGIC+bytes([VERSION])+struct.pack('>I Q H I',block_size,len(data),stride,len(choices));archive=header+body
    rep={'schema':'FISCHER-CODEC-v2','raw_bytes':len(data),'archive_bytes':len(archive),'bpc':len(archive)*8/max(1,len(data)),
         'block_size':block_size,'pyramid_stride':stride,'blocks':len(choices),'black_selected':sum(c['selected'].startswith('black-sequential') for c in choices),
         'blackwhite_selected':sum(c['selected'].startswith('blackwhite') for c in choices),'always_black_payload_bytes':sum_black,
         'always_blackwhite_payload_bytes':sum_both,'selected_payload_bytes':sum(c['selected_bytes'] for c in choices),
         'header_and_block_index_bytes':len(archive)-sum(c['selected_bytes'] for c in choices),'choices':choices,
         'black_state':black.report(),'blackwhite_state':both.report(),'sha256_in':hashlib.sha256(data).hexdigest(),
         'sha256_archive':hashlib.sha256(archive).hexdigest()}
    return archive,rep

def tournament_decode(archive:bytes)->tuple[bytes,dict]:
    if archive[:4]!=MAGIC or archive[4]!=VERSION:raise ValueError('bad archive')
    block_size,n,stride,nblocks=struct.unpack('>I Q H I',archive[5:23]);pos=23;black=ModelState('black');both=ModelState('both');out=bytearray();choices=[]
    for block_no in range(nblocks):
        mode,raw_len,payload_len=struct.unpack('>BII',archive[pos:pos+9]);pos+=9;payload=archive[pos:pos+payload_len];pos+=payload_len
        if mode==0:raw=decode_block(payload,raw_len,black,'sequential',stride);replay_block(raw,both,'pyramid',stride);sel='black-sequential'
        elif mode==1:raw=decode_block(payload,raw_len,both,'pyramid',stride);replay_block(raw,black,'sequential',stride);sel='blackwhite-pyramid'
        else:raise ValueError('bad mode')
        out+=raw;choices.append({'block':block_no,'selected':sel,'raw_bytes':raw_len,'payload_bytes':payload_len})
    if len(out)!=n or pos!=len(archive):raise ValueError('framing mismatch')
    rep={'raw_bytes':n,'archive_bytes':len(archive),'bpc':len(archive)*8/max(1,n),'blocks':nblocks,'choices':choices,
         'black_state_sha256':black.digest(),'blackwhite_state_sha256':both.digest(),'sha256_out':hashlib.sha256(out).hexdigest()}
    return bytes(out),rep

def expert_audit(data:bytes,direction:str,order:int,stride:int=4,block_size:int=16384)->dict:
    ex=HashedExpert(direction,order)
    for off in range(0,len(data),block_size):
        raw=data[off:off+block_size];buf=bytearray(raw)
        for task in pyramid_tasks(len(raw),stride):
            ch=tuple(buf[i] for i in (task.left if direction=='black' else task.right));value=raw[task.index];prefix=0
            for bitpos in range(8):
                p=ex.predict(ch,task.stage,bitpos,prefix);bit=(value>>(7-bitpos))&1;ex.update(ch,task.stage,bitpos,prefix,bit,p);prefix=(prefix<<1)|bit
    return {'direction':direction,'order':order,'raw_bytes':len(data),'ideal_bpb':ex.loss_bits/max(1,ex.bits),
            'accuracy':ex.correct/max(1,ex.bits),'blunders':ex.blunders,'table_bytes':len(ex.counts),'slots_touched':ex.touched,
            'actor_pid':hashlib.sha256(f'FISCHER|{direction}|{order}'.encode()).hexdigest()[:16]}

def oracle_audit(data:bytes,max_order:int=5)->dict:
    # Deliberately uses actual future bytes. It is not a decodable standalone codec.
    states=[HashedExpert('black',o) for o in range(1,max_order+1)]+[HashedExpert('white',o) for o in range(1,max_order+1)]
    mix_black=ContextMixer(5,4);mix_both=ContextMixer(10,4);loss_black=loss_both=0.0;bits=0
    buf=bytearray(data)
    for i,value in enumerate(data):
        left=tuple(data[j] for j in range(i-1,max(-1,i-6),-1));right=tuple(data[j] for j in range(i+1,min(len(data),i+6)))
        task=Task(i,tuple(range(i-1,max(-1,i-6),-1)),tuple(range(i+1,min(len(data),i+6))),0);prefix=0
        for bitpos in range(8):
            probs=[];chains=[]
            for ex in states:
                ch=left if ex.direction=='black' else right;chains.append(ch);probs.append(ex.predict(ch,0,bitpos,prefix))
            kb=mix_black.key(task,buf,bitpos);ka=mix_both.key(task,buf,bitpos);pb=mix_black.predict(probs[:5],kb);pa=mix_both.predict(probs,ka)
            bit=(value>>(7-bitpos))&1
            loss_black += -math.log2((pb if bit else TOT-pb)/TOT);loss_both += -math.log2((pa if bit else TOT-pa)/TOT);bits+=1
            mix_black.update(probs[:5],kb,bit,pb);mix_both.update(probs,ka,bit,pa)
            for ex,ch,p in zip(states,chains,probs):ex.update(ch,0,bitpos,prefix,bit,p)
            prefix=(prefix<<1)|bit
    return {'scope':'ORACLE_NOT_CODEC','raw_bytes':len(data),'black_ideal_bpc':loss_black/max(1,len(data)),
            'blackwhite_ideal_bpc':loss_both/max(1,len(data)),'apparent_gain_pct':100*(1-loss_both/max(loss_black,1e-9)),
            'reason':'white contexts contain true future target bytes unavailable to a standalone decoder'}

def main():
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest='cmd',required=True)
    b=sp.add_parser('bench');b.add_argument('input');b.add_argument('--bytes',type=int);b.add_argument('--block-size',type=int,default=16384);b.add_argument('--stride',type=int,default=4);b.add_argument('--output-dir',default='fischer-v2-out')
    a=sp.add_parser('audit');a.add_argument('input');a.add_argument('--bytes',type=int);a.add_argument('--direction',choices=DIRECTIONS,required=True);a.add_argument('--order',type=int,choices=range(1,6),required=True);a.add_argument('--stride',type=int,default=4);a.add_argument('--block-size',type=int,default=16384);a.add_argument('--output')
    o=sp.add_parser('oracle');o.add_argument('input');o.add_argument('--bytes',type=int);o.add_argument('--output')
    x=p.parse_args();data=Path(x.input).read_bytes();data=data[:x.bytes] if getattr(x,'bytes',None) else data
    if x.cmd=='audit':
        rep=expert_audit(data,x.direction,x.order,x.stride,x.block_size);text=json.dumps(rep,indent=2);print(text)
        if x.output:Path(x.output).write_text(text)
    elif x.cmd=='oracle':
        rep=oracle_audit(data);text=json.dumps(rep,indent=2);print(text)
        if x.output:Path(x.output).write_text(text)
    else:
        out=Path(x.output_dir);out.mkdir(parents=True,exist_ok=True);t=time.time();arc,enc=tournament_encode(data,x.block_size,x.stride);enc['encode_s']=time.time()-t
        Path(out/'fischer-v2.fsc').write_bytes(arc);t=time.time();raw,dec=tournament_decode(arc);dec['decode_s']=time.time()-t
        enc['restore']=raw==data;enc['sha256_out']=hashlib.sha256(raw).hexdigest();enc['decoder_black_state_sha256']=dec['black_state_sha256'];enc['decoder_blackwhite_state_sha256']=dec['blackwhite_state_sha256'];enc['state_match']=enc['black_state']['state_sha256']==dec['black_state_sha256'] and enc['blackwhite_state']['state_sha256']==dec['blackwhite_state_sha256']
        Path(out/'bench.json').write_text(json.dumps(enc,indent=2));Path(out/'decoded.bin').write_bytes(raw);print(json.dumps(enc))
        if not enc['restore'] or not enc['state_match']:raise SystemExit(1)

if __name__=='__main__':main()
