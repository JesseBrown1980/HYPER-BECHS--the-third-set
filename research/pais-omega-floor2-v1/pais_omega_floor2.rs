// Pais Omega Floor Two — GitRAM trainer over BEHCS-1024 glyph streams.
// Trains FROM the sealed floor-one bodies (chains/payloads/receipts), never the raw PDFs.
// Old decodes new: this binary carries the floor-one PAISCHAIN1 decoder and every body
// input must restore byte-exact through it before any floor-two cell trains.
// Alphabet: 10-bit glyphs (1024). Control arm: 6-bit glyphs (64) on body 01's input.
// Shape: 27 base + 6 apex (+X,-X,+Y,-Y,+Z,-Z) + 1 Omega junction = 34 bodies x 800 cells.
// Schedule unchanged from floor one: 8 reversible A-lanes x 10 predictor lanes x 10 epochs.
// Higher floors HELD. Density = measured structure/repetition only. No record claims.

use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::time::Instant;

type AnyResult<T> = Result<T, String>;

const BODY_COUNT: usize = 34;
const BASE_COUNT: usize = 27;
const EPOCHS: usize = 10;
const FLOOR2_BITS: u32 = 10;
const CONTROL_BITS: u32 = 6;
const A_NAMES: [&str; 8] = [
    "G1024_FORWARD_IDENTITY",
    "G1024_REVERSE_GLYPHS",
    "G1024_FORWARD_XOR_DELTA",
    "G1024_REVERSE_ROTATE_BITS",
    "G1024_HALF_SWAP",
    "G1024_BLOCK_REVERSE",
    "G1024_NESTED_EVEN_ODD",
    "G1024_QPRISM_PRIME_BLOCK",
];
const B_DIRECTIONS: [&str; 2] = ["BLACK_FORWARD", "WHITE_REVERSE"];
const APEX_NAMES: [&str; 6] = ["+X", "-X", "+Y", "-Y", "+Z", "-Z"];

// ---------- sha256 / hex / receipts (ported verbatim in behavior from floor one) ----------

fn sha256(data: &[u8]) -> [u8; 32] {
    const K: [u32; 64] = [
        0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
        0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
        0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
        0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
        0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
        0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
        0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
        0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2,
    ];
    let mut msg = data.to_vec();
    let bit_len = (msg.len() as u64).wrapping_mul(8);
    msg.push(0x80);
    while msg.len() % 64 != 56 { msg.push(0); }
    msg.extend_from_slice(&bit_len.to_be_bytes());
    let mut h: [u32; 8] = [
        0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,
        0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19,
    ];
    for chunk in msg.chunks_exact(64) {
        let mut w = [0u32; 64];
        for i in 0..16 {
            w[i] = u32::from_be_bytes(chunk[i*4..i*4+4].try_into().unwrap());
        }
        for i in 16..64 {
            let s0 = w[i-15].rotate_right(7) ^ w[i-15].rotate_right(18) ^ (w[i-15] >> 3);
            let s1 = w[i-2].rotate_right(17) ^ w[i-2].rotate_right(19) ^ (w[i-2] >> 10);
            w[i] = w[i-16].wrapping_add(s0).wrapping_add(w[i-7]).wrapping_add(s1);
        }
        let (mut a,mut b,mut c,mut d,mut e,mut f,mut g,mut hh) =
            (h[0],h[1],h[2],h[3],h[4],h[5],h[6],h[7]);
        for i in 0..64 {
            let s1 = e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25);
            let ch = (e & f) ^ ((!e) & g);
            let t1 = hh.wrapping_add(s1).wrapping_add(ch).wrapping_add(K[i]).wrapping_add(w[i]);
            let s0 = a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22);
            let maj = (a & b) ^ (a & c) ^ (b & c);
            let t2 = s0.wrapping_add(maj);
            hh=g; g=f; f=e; e=d.wrapping_add(t1); d=c; c=b; b=a; a=t1.wrapping_add(t2);
        }
        h[0]=h[0].wrapping_add(a); h[1]=h[1].wrapping_add(b);
        h[2]=h[2].wrapping_add(c); h[3]=h[3].wrapping_add(d);
        h[4]=h[4].wrapping_add(e); h[5]=h[5].wrapping_add(f);
        h[6]=h[6].wrapping_add(g); h[7]=h[7].wrapping_add(hh);
    }
    let mut out = [0u8; 32];
    for (i, v) in h.iter().enumerate() { out[i*4..i*4+4].copy_from_slice(&v.to_be_bytes()); }
    out
}

fn hex(bytes: &[u8]) -> String {
    const H: &[u8; 16] = b"0123456789abcdef";
    let mut s = String::with_capacity(bytes.len()*2);
    for &b in bytes { s.push(H[(b>>4) as usize] as char); s.push(H[(b&15) as usize] as char); }
    s
}

fn sha_hex(data: &[u8]) -> String { hex(&sha256(data)) }

fn parse_fields(line: &str) -> HashMap<String, String> {
    let mut out = HashMap::new();
    for field in line.split('|').skip(1) {
        if let Some((k,v)) = field.split_once('=') { out.insert(k.to_string(), v.to_string()); }
    }
    out
}

fn write_lf(path: &Path, text: &str) -> AnyResult<()> {
    if let Some(parent) = path.parent() { fs::create_dir_all(parent).map_err(|e| e.to_string())?; }
    let normalized = text.replace("\r\n", "\n").replace('\r', "\n");
    fs::write(path, normalized.as_bytes()).map_err(|e| format!("write {}: {}", path.display(), e))
}

fn write_sidecar(path: &Path) -> AnyResult<String> {
    let bytes = fs::read(path).map_err(|e| e.to_string())?;
    let digest = sha_hex(&bytes);
    let name = path.file_name().unwrap().to_string_lossy();
    write_lf(&PathBuf::from(format!("{}.sha256", path.display())), &format!("{}  {}\n", digest, name))?;
    Ok(digest)
}

fn check_sidecar(path: &Path) -> AnyResult<String> {
    let bytes = fs::read(path).map_err(|e| format!("{}: {}", path.display(), e))?;
    let digest = sha_hex(&bytes);
    let side = fs::read_to_string(PathBuf::from(format!("{}.sha256", path.display())))
        .map_err(|e| format!("sidecar {}: {}", path.display(), e))?;
    let expected = side.split_whitespace().next().unwrap_or("");
    if expected != digest { return Err(format!("sidecar mismatch {}", path.display())); }
    Ok(digest)
}

fn pid8(label: &str) -> String { sha_hex(label.as_bytes())[..16].to_string() }

// ---------- floor-one byte layer (old decodes new): exact PAISCHAIN1 decoder ----------

fn t_r(data: &[u8]) -> Vec<u8> { data.iter().rev().copied().collect() }
fn t_n(data: &[u8]) -> Vec<u8> { data.iter().map(|b| (b<<4)|(b>>4)).collect() }
fn reverse_nibble(x: u8) -> u8 { ((x&1)<<3)|((x&2)<<1)|((x&4)>>1)|((x&8)>>3) }
fn t_q(data: &[u8]) -> Vec<u8> { data.iter().map(|b| (reverse_nibble(b>>4)<<4)|reverse_nibble(b&15)).collect() }

fn xor_undelta(data: &[u8]) -> Vec<u8> {
    if data.is_empty() { return Vec::new(); }
    let mut out=Vec::with_capacity(data.len()); out.push(data[0]);
    for i in 1..data.len() { let b=data[i]^out[i-1]; out.push(b); }
    out
}
fn block_reverse_bytes(data: &[u8], block: usize) -> Vec<u8> {
    let mut out=Vec::with_capacity(data.len());
    for c in data.chunks(block) { out.extend(c.iter().rev()); }
    out
}
fn undo_even_odd_bytes(data: &[u8]) -> Vec<u8> {
    let even=(data.len()+1)/2; let mut out=vec![0u8;data.len()];
    for i in 0..even { out[i*2]=data[i]; }
    for i in even..data.len() { out[(i-even)*2+1]=data[i]; }
    out
}
fn qprism_order_bytes(nblocks: usize, source_sha: &[u8;32]) -> Vec<usize> {
    let mut keyed:Vec<([u8;32],usize)>=(0..nblocks).map(|i| {
        let mut seed=b"QPRISM_PRIME_BLOCK_SHA256_V1|257|".to_vec();
        seed.extend_from_slice(source_sha); seed.extend_from_slice(&(i as u64).to_le_bytes());
        (sha256(&seed),i)
    }).collect();
    keyed.sort_by(|a,b| a.0.cmp(&b.0).then(a.1.cmp(&b.1)));
    keyed.into_iter().map(|x|x.1).collect()
}
fn undo_qprism_bytes(data: &[u8], source_sha: &[u8;32]) -> Vec<u8> {
    let block=257usize; let n=data.len()/block; let order=qprism_order_bytes(n,source_sha);
    let mut out=vec![0u8;data.len()];
    for (pos,orig) in order.into_iter().enumerate() {
        out[orig*block..(orig+1)*block].copy_from_slice(&data[pos*block..(pos+1)*block]);
    }
    out[n*block..].copy_from_slice(&data[n*block..]); out
}
fn a_inverse_bytes(index: usize, data: &[u8], source_sha: &[u8;32]) -> Vec<u8> {
    match index {
        0=>data.to_vec(),
        1=>t_r(data),
        2=>xor_undelta(data),
        3=>data.iter().map(|b|b.rotate_right(1)).rev().collect(),
        4=>t_n(data),
        5=>block_reverse_bytes(data,256),
        6=>undo_even_odd_bytes(data),
        7=>undo_qprism_bytes(data,source_sha),
        _=>unreachable!(),
    }
}

// ---------- LZ1 (identical to floor one) ----------

fn flush_literals(out:&mut Vec<u8>,lits:&mut Vec<u8>) {
    let mut at=0usize;
    while at<lits.len() { let n=(lits.len()-at).min(u16::MAX as usize); out.push(0); out.extend_from_slice(&(n as u16).to_le_bytes()); out.extend_from_slice(&lits[at..at+n]); at+=n; }
    lits.clear();
}

fn lz_compress(data:&[u8])->Vec<u8> {
    let mut out=b"LZ1\0".to_vec(); out.extend_from_slice(&(data.len() as u64).to_le_bytes());
    let mut last:HashMap<u32,usize>=HashMap::new(); let mut lits=Vec::new(); let mut i=0usize;
    while i<data.len() {
        let key=if i+2<data.len(){Some(((data[i] as u32)<<16)|((data[i+1] as u32)<<8)|data[i+2] as u32)}else{None};
        let mut best=0usize; let mut offset=0usize;
        if let Some(k)=key { if let Some(&p)=last.get(&k) { let off=i-p; if off>0&&off<=u16::MAX as usize { let max=(data.len()-i).min(u16::MAX as usize); while best<max&&data[p+best]==data[i+best]{best+=1;} if best>=4{offset=off;} } } }
        if best>=4 {
            flush_literals(&mut out,&mut lits); out.push(1); out.extend_from_slice(&(offset as u16).to_le_bytes()); out.extend_from_slice(&(best as u16).to_le_bytes());
            for pos in i..i+best { if pos+2<data.len(){let k=((data[pos] as u32)<<16)|((data[pos+1] as u32)<<8)|data[pos+2] as u32; last.insert(k,pos);} }
            i+=best;
        } else {
            if let Some(k)=key {last.insert(k,i);} lits.push(data[i]); i+=1; if lits.len()==u16::MAX as usize{flush_literals(&mut out,&mut lits);}
        }
    }
    flush_literals(&mut out,&mut lits); out
}

fn lz_decompress(data:&[u8])->AnyResult<Vec<u8>> {
    if data.len()<12||&data[..4]!=b"LZ1\0" {return Err("bad LZ1 header".into());}
    let want=u64::from_le_bytes(data[4..12].try_into().unwrap()) as usize; let mut at=12usize; let mut out=Vec::with_capacity(want);
    while at<data.len()&&out.len()<want {
        let tag=data[at]; at+=1;
        if tag==0 { if at+2>data.len(){return Err("short literal".into());} let n=u16::from_le_bytes(data[at..at+2].try_into().unwrap()) as usize; at+=2; if at+n>data.len(){return Err("literal overflow".into());} out.extend_from_slice(&data[at..at+n]); at+=n; }
        else if tag==1 { if at+4>data.len(){return Err("short match".into());} let off=u16::from_le_bytes(data[at..at+2].try_into().unwrap()) as usize; let n=u16::from_le_bytes(data[at+2..at+4].try_into().unwrap()) as usize; at+=4; if off==0||off>out.len(){return Err("bad match offset".into());} for _ in 0..n {let b=out[out.len()-off];out.push(b);} }
        else {return Err("bad LZ1 tag".into());}
    }
    if out.len()!=want {return Err("LZ1 length mismatch".into());} Ok(out)
}

// ---------- predictor (generalized to B-bit symbols; bits=8 replays floor-one exactly) ----------

#[derive(Clone, PartialEq, Eq)]
struct BestState { total: u32, best_symbol: u16, best_count: u32 }

#[derive(Clone, PartialEq, Eq)]
struct PredictorModel {
    bits: u32,
    order: u8,
    direction: u8,
    counts: HashMap<(u64, u16), u32>,
    best: HashMap<u64, BestState>,
    commit: [u8; 32],
    epochs: u32,
}

struct Metrics {
    predictions: u64,
    top1_correct: u64,
    unseen_contexts: u64,
    novel_pairs: u64,
    confident_blunders: u64,
}

impl PredictorModel {
    fn new(bits: u32, order: u8, direction: u8) -> Self {
        let mut domain=b"PAIS-PREDICTOR-STATE-V2|".to_vec();
        domain.push(bits as u8); domain.push(order); domain.push(direction);
        Self{bits,order,direction,counts:HashMap::new(),best:HashMap::new(),commit:sha256(&domain),epochs:0}
    }
    fn mask(&self)->u64 { (1u64 << (self.order as u32*self.bits))-1 }
    fn key(&self,ctx:u64,seen:usize)->u64 {
        let n=seen.min(self.order as usize) as u64;
        ctx | (n<<50) | ((self.order as u64)<<56)
    }
    fn predict(&self,key:u64)->(u16,u32,u32) {
        self.best.get(&key).map(|s|(s.best_symbol,s.best_count,s.total)).unwrap_or((0,0,0))
    }
    fn update(&mut self,key:u64,sym:u16)->bool {
        let count=self.counts.entry((key,sym)).or_insert(0); let novel=*count==0; *count+=1; let nc=*count;
        let state=self.best.entry(key).or_insert(BestState{total:0,best_symbol:0,best_count:0});
        state.total=state.total.saturating_add(1);
        if nc>state.best_count || (nc==state.best_count && sym<state.best_symbol) { state.best_symbol=sym; state.best_count=nc; }
        novel
    }
    fn finish_epoch(&mut self,seq:&[u16],m:&Metrics) {
        let packed=pack_glyphs(seq,self.bits);
        let mut b=Vec::new(); b.extend_from_slice(&self.commit); b.extend_from_slice(&sha256(&packed));
        b.extend_from_slice(&(self.epochs+1).to_le_bytes()); b.extend_from_slice(&m.predictions.to_le_bytes());
        b.extend_from_slice(&m.top1_correct.to_le_bytes()); b.extend_from_slice(&m.unseen_contexts.to_le_bytes());
        b.extend_from_slice(&m.novel_pairs.to_le_bytes()); b.extend_from_slice(&(self.counts.len() as u64).to_le_bytes());
        self.commit=sha256(&b); self.epochs+=1;
    }
    fn encode(&mut self,seq:&[u16])->(Vec<u16>,Metrics) {
        let mut residual=Vec::with_capacity(seq.len()); let mut ctx=0u64; let mut seen=0usize;
        let mut m=Metrics{predictions:0,top1_correct:0,unseen_contexts:0,novel_pairs:0,confident_blunders:0};
        let mask=self.mask();
        for &sym in seq {
            let key=self.key(ctx,seen); let (pred,best_count,total)=self.predict(key);
            if total==0 { m.unseen_contexts+=1; } else { m.predictions+=1; if pred==sym {m.top1_correct+=1;} else if (best_count as u64)*10 >= (total as u64)*9 {m.confident_blunders+=1;} }
            residual.push(sym^pred); if self.update(key,sym) {m.novel_pairs+=1;}
            ctx=((ctx<<self.bits)|(sym as u64))&mask; seen+=1;
        }
        self.finish_epoch(seq,&m); (residual,m)
    }
    fn decode(&mut self,residual:&[u16])->(Vec<u16>,Metrics) {
        let mut seq=Vec::with_capacity(residual.len()); let mut ctx=0u64; let mut seen=0usize;
        let mut m=Metrics{predictions:0,top1_correct:0,unseen_contexts:0,novel_pairs:0,confident_blunders:0};
        let mask=self.mask();
        for &r in residual {
            let key=self.key(ctx,seen); let (pred,best_count,total)=self.predict(key); let sym=r^pred;
            if total==0 { m.unseen_contexts+=1; } else { m.predictions+=1; if pred==sym {m.top1_correct+=1;} else if (best_count as u64)*10 >= (total as u64)*9 {m.confident_blunders+=1;} }
            if self.update(key,sym) {m.novel_pairs+=1;}
            seq.push(sym); ctx=((ctx<<self.bits)|(sym as u64))&mask; seen+=1;
        }
        self.finish_epoch(&seq,&m); (seq,m)
    }
}

// ---------- floor-one chain decode (PAISCHAIN1, byte symbols) ----------

fn decode_chain_floor1(data:&[u8])->AnyResult<Vec<u8>> {
    if data.len()<54||&data[..10]!=b"PAISCHAIN1" {return Err("bad chain header".into());}
    let mut at=10usize; let source_sha:[u8;32]=data[at..at+32].try_into().unwrap(); at+=32;
    let a=data[at] as usize; let direction=data[at+1]; let order=data[at+2]; let epochs=data[at+3] as usize; at+=4;
    let native_len=u64::from_le_bytes(data[at..at+8].try_into().unwrap()) as usize; at+=8;
    let mut model=PredictorModel::new(8,order,direction); let mut final_seq:Vec<u16>=Vec::new();
    for _ in 0..epochs {
        if at+8>data.len(){return Err("short chain length".into());}
        let n=u64::from_le_bytes(data[at..at+8].try_into().unwrap()) as usize; at+=8;
        if at+n>data.len(){return Err("short chain payload".into());}
        let residual_bytes=lz_decompress(&data[at..at+n])?; at+=n;
        let residual:Vec<u16>=residual_bytes.iter().map(|&b|b as u16).collect();
        let (seq,_)=model.decode(&residual); final_seq=seq;
    }
    let mut final_bytes:Vec<u8>=final_seq.iter().map(|&s|s as u8).collect();
    if direction==1 {final_bytes.reverse();}
    let native=a_inverse_bytes(a,&final_bytes,&source_sha);
    if native.len()!=native_len||sha256(&native)!=source_sha{return Err("chain native restore failed".into());}
    Ok(native)
}

fn parse_chain_payloads_floor1(data:&[u8])->AnyResult<Vec<Vec<u8>>> {
    if data.len()<54||&data[..10]!=b"PAISCHAIN1" {return Err("bad chain header".into());}
    let mut at=10usize+32; let epochs=data[at+3] as usize; at+=4; at+=8;
    let mut payloads=Vec::new();
    for _ in 0..epochs {
        if at+8>data.len(){return Err("short chain length".into());}
        let n=u64::from_le_bytes(data[at..at+8].try_into().unwrap()) as usize; at+=8;
        if at+n>data.len(){return Err("short chain payload".into());}
        payloads.push(data[at..at+n].to_vec()); at+=n;
    }
    Ok(payloads)
}

// ---------- glyph layer ----------

fn bytes_to_glyphs(bytes:&[u8], bits:u32)->Vec<u16> {
    let total_bits=bytes.len()*8;
    let count=(total_bits+bits as usize-1)/bits as usize;
    let mut out=Vec::with_capacity(count);
    let mut acc:u32=0; let mut nb:u32=0;
    for &b in bytes {
        acc=(acc<<8)|(b as u32); nb+=8;
        while nb>=bits { nb-=bits; out.push(((acc>>nb)&((1<<bits)-1)) as u16); }
    }
    if nb>0 { out.push(((acc<<(bits-nb))&((1<<bits)-1)) as u16); }
    debug_assert_eq!(out.len(),count);
    out
}

fn glyphs_to_bytes(glyphs:&[u16], bits:u32, native_len:usize)->Vec<u8> {
    let mut out=Vec::with_capacity(native_len+2);
    let mut acc:u32=0; let mut nb:u32=0;
    for &g in glyphs {
        acc=(acc<<bits)|(g as u32); nb+=bits;
        while nb>=8 { nb-=8; out.push(((acc>>nb)&0xff) as u8); }
    }
    if nb>0 { out.push(((acc<<(8-nb))&0xff) as u8); }
    out.truncate(native_len);
    out
}

fn pack_glyphs(glyphs:&[u16], bits:u32)->Vec<u8> {
    let mut out=Vec::with_capacity((glyphs.len()*bits as usize+7)/8);
    let mut acc:u32=0; let mut nb:u32=0;
    for &g in glyphs {
        acc=(acc<<bits)|(g as u32); nb+=bits;
        while nb>=8 { nb-=8; out.push(((acc>>nb)&0xff) as u8); }
    }
    if nb>0 { out.push(((acc<<(8-nb))&0xff) as u8); }
    out
}

fn unpack_glyphs(bytes:&[u8], bits:u32, count:usize)->Vec<u16> {
    let mut out=Vec::with_capacity(count);
    let mut acc:u32=0; let mut nb:u32=0;
    for &b in bytes {
        acc=(acc<<8)|(b as u32); nb+=8;
        while nb>=bits { if out.len()==count {break;} nb-=bits; out.push(((acc>>nb)&((1<<bits)-1)) as u16); }
        if out.len()==count {break;}
    }
    out
}

fn rev_bits(v:u16, n:u32)->u16 {
    let mut out=0u16;
    for i in 0..n { if v&(1<<i)!=0 { out|=1<<(n-1-i); } }
    out
}

// glyph transforms — R (reverse), N (half swap), Q (bit-reverse within halves)
fn g_r(data:&[u16])->Vec<u16> { data.iter().rev().copied().collect() }
fn g_n(data:&[u16], bits:u32)->Vec<u16> {
    let half=bits/2; let hm=(1u16<<half)-1;
    data.iter().map(|&g| ((g&hm)<<half)|(g>>half)).collect()
}
fn g_q(data:&[u16], bits:u32)->Vec<u16> {
    let half=bits/2; let hm=(1u16<<half)-1;
    data.iter().map(|&g| (rev_bits(g>>half,half)<<half)|rev_bits(g&hm,half)).collect()
}

fn geometry_view_glyphs(data:&[u16], mask:u8, bits:u32)->Vec<u16> {
    let mut out=data.to_vec();
    if mask&1 != 0 { out=g_r(&out); }
    if mask&2 != 0 { out=g_n(&out,bits); }
    if mask&4 != 0 { out=g_q(&out,bits); }
    out
}

fn group_gate_glyphs(data:&[u16], bits:u32)->(bool, Vec<String>, String) {
    let rr=g_r(&g_r(data))==*data;
    let nn=g_n(&g_n(data,bits),bits)==*data;
    let qq=g_q(&g_q(data,bits),bits)==*data;
    let rn=g_r(&g_n(data,bits))==g_n(&g_r(data),bits);
    let rq=g_r(&g_q(data,bits))==g_q(&g_r(data),bits);
    let nq=g_n(&g_q(data,bits),bits)==g_q(&g_n(data,bits),bits);
    let mut views=Vec::new();
    let mut uniq=HashSet::new();
    for m in 0..8 { let v=geometry_view_glyphs(data,m,bits); let h=sha_hex(&pack_glyphs(&v,bits)); uniq.insert(h.clone()); views.push(h); }
    let rnq=geometry_view_glyphs(data,7,bits);
    let total:Vec<u16>=data.iter().rev().map(|&g| rev_bits(g,bits)).collect();
    let total_ok=rnq==total;
    (rr&&nn&&qq&&rn&&rq&&nq&&uniq.len()==8&&total_ok, views, format!("squares={},{},{}|commutators={},{},{}|distinct={}|rnq_total={}", u8::from(rr),u8::from(nn),u8::from(qq),u8::from(rn),u8::from(rq),u8::from(nq),uniq.len(),u8::from(total_ok)))
}

fn xor_delta_glyphs(data:&[u16])->Vec<u16> {
    if data.is_empty() { return Vec::new(); }
    let mut out=Vec::with_capacity(data.len()); out.push(data[0]);
    for i in 1..data.len() { out.push(data[i]^data[i-1]); }
    out
}
fn xor_undelta_glyphs(data:&[u16])->Vec<u16> {
    if data.is_empty() { return Vec::new(); }
    let mut out=Vec::with_capacity(data.len()); out.push(data[0]);
    for i in 1..data.len() { let g=data[i]^out[i-1]; out.push(g); }
    out
}
fn rotate_left_glyph(g:u16, bits:u32)->u16 { let m=(1u16<<bits)-1; ((g<<1)|(g>>(bits-1)))&m }
fn rotate_right_glyph(g:u16, bits:u32)->u16 { let m=(1u16<<bits)-1; ((g>>1)|((g&1)<<(bits-1)))&m }
fn block_reverse_glyphs(data:&[u16], block:usize)->Vec<u16> {
    let mut out=Vec::with_capacity(data.len());
    for c in data.chunks(block) { out.extend(c.iter().rev()); }
    out
}
fn even_odd_glyphs(data:&[u16])->Vec<u16> {
    data.iter().step_by(2).chain(data.iter().skip(1).step_by(2)).copied().collect()
}
fn undo_even_odd_glyphs(data:&[u16])->Vec<u16> {
    let even=(data.len()+1)/2; let mut out=vec![0u16;data.len()];
    for i in 0..even { out[i*2]=data[i]; }
    for i in even..data.len() { out[(i-even)*2+1]=data[i]; }
    out
}
fn qprism_order_glyphs(nblocks:usize, source_sha:&[u8;32])->Vec<usize> {
    let mut keyed:Vec<([u8;32],usize)>=(0..nblocks).map(|i| {
        let mut seed=b"QPRISM_PRIME_BLOCK_GLYPH_V2|257|".to_vec();
        seed.extend_from_slice(source_sha); seed.extend_from_slice(&(i as u64).to_le_bytes());
        (sha256(&seed),i)
    }).collect();
    keyed.sort_by(|a,b| a.0.cmp(&b.0).then(a.1.cmp(&b.1)));
    keyed.into_iter().map(|x|x.1).collect()
}
fn qprism_glyphs(data:&[u16], source_sha:&[u8;32])->Vec<u16> {
    let block=257usize; let n=data.len()/block; let order=qprism_order_glyphs(n,source_sha);
    let mut out=Vec::with_capacity(data.len());
    for orig in order { out.extend_from_slice(&data[orig*block..(orig+1)*block]); }
    out.extend_from_slice(&data[n*block..]); out
}
fn undo_qprism_glyphs(data:&[u16], source_sha:&[u8;32])->Vec<u16> {
    let block=257usize; let n=data.len()/block; let order=qprism_order_glyphs(n,source_sha);
    let mut out=vec![0u16;data.len()];
    for (pos,orig) in order.into_iter().enumerate() {
        out[orig*block..(orig+1)*block].copy_from_slice(&data[pos*block..(pos+1)*block]);
    }
    out[n*block..].copy_from_slice(&data[n*block..]); out
}

fn a_apply_glyphs(index:usize, data:&[u16], bits:u32, source_sha:&[u8;32])->Vec<u16> {
    match index {
        0=>data.to_vec(),
        1=>g_r(data),
        2=>xor_delta_glyphs(data),
        3=>data.iter().rev().map(|&g|rotate_left_glyph(g,bits)).collect(),
        4=>g_n(data,bits),
        5=>block_reverse_glyphs(data,256),
        6=>even_odd_glyphs(data),
        7=>qprism_glyphs(data,source_sha),
        _=>unreachable!(),
    }
}
fn a_inverse_glyphs(index:usize, data:&[u16], bits:u32, source_sha:&[u8;32])->Vec<u16> {
    match index {
        0=>data.to_vec(),
        1=>g_r(data),
        2=>xor_undelta_glyphs(data),
        3=>data.iter().map(|&g|rotate_right_glyph(g,bits)).rev().collect(),
        4=>g_n(data,bits),
        5=>block_reverse_glyphs(data,256),
        6=>undo_even_odd_glyphs(data),
        7=>undo_qprism_glyphs(data,source_sha),
        _=>unreachable!(),
    }
}

// ---------- floor-two chain (PAISCHAIN2, B-bit glyph symbols) ----------

struct BestChain {
    a_index: u8,
    direction: u8,
    order: u8,
    payloads: Vec<Vec<u8>>,
    min_payload: usize,
}

fn chain_bytes_floor2(chain:&BestChain, source_sha:&[u8;32], bits:u32, native_len:usize, glyph_count:usize)->Vec<u8> {
    let mut out=b"PAISCHAIN2".to_vec(); out.extend_from_slice(source_sha);
    out.push(chain.a_index); out.push(chain.direction); out.push(chain.order); out.push(chain.payloads.len() as u8);
    out.push(bits as u8);
    out.extend_from_slice(&(native_len as u64).to_le_bytes());
    out.extend_from_slice(&(glyph_count as u64).to_le_bytes());
    for p in &chain.payloads {out.extend_from_slice(&(p.len() as u64).to_le_bytes());out.extend_from_slice(p);} out
}

fn decode_chain_floor2(data:&[u8])->AnyResult<Vec<u8>> {
    if data.len()<63||&data[..10]!=b"PAISCHAIN2" {return Err("bad chain2 header".into());}
    let mut at=10usize; let source_sha:[u8;32]=data[at..at+32].try_into().unwrap(); at+=32;
    let a=data[at] as usize; let direction=data[at+1]; let order=data[at+2]; let epochs=data[at+3] as usize; let bits=data[at+4] as u32; at+=5;
    let native_len=u64::from_le_bytes(data[at..at+8].try_into().unwrap()) as usize; at+=8;
    let glyph_count=u64::from_le_bytes(data[at..at+8].try_into().unwrap()) as usize; at+=8;
    if bits<2||bits>15 {return Err("bad chain2 bits".into());}
    let mut model=PredictorModel::new(bits,order,direction); let mut final_seq:Vec<u16>=Vec::new();
    for _ in 0..epochs {
        if at+8>data.len(){return Err("short chain2 length".into());}
        let n=u64::from_le_bytes(data[at..at+8].try_into().unwrap()) as usize; at+=8;
        if at+n>data.len(){return Err("short chain2 payload".into());}
        let packed=lz_decompress(&data[at..at+n])?; at+=n;
        let residual=unpack_glyphs(&packed,bits,glyph_count);
        if residual.len()!=glyph_count {return Err("chain2 residual glyph count".into());}
        let (seq,_)=model.decode(&residual); final_seq=seq;
    }
    if direction==1 {final_seq.reverse();}
    let native_glyphs=a_inverse_glyphs(a,&final_seq,bits,&source_sha);
    let native=glyphs_to_bytes(&native_glyphs,bits,native_len);
    if native.len()!=native_len||sha256(&native)!=source_sha{return Err("chain2 native restore failed".into());}
    Ok(native)
}

// ---------- floor-one intake: locate + verify the sealed floor-one tree ----------

struct Floor1Leaf { cube: usize, source_sha: String, leaf_sha: String, archive_sha: String, chain_sha: String }

struct Floor1 {
    root: PathBuf,
    omega: String,
    result_sha: String,
    leaves: Vec<Floor1Leaf>,
}

fn find_floor1_root(base:&Path)->AnyResult<PathBuf> {
    let direct=base.join("PAIS-OMEGA-FLOOR1-RESULT.hbp");
    if direct.exists() { return Ok(base.to_path_buf()); }
    let nested=base.join("fan-in").join("PAIS-OMEGA-FLOOR1-RESULT.hbp");
    if nested.exists() { return Ok(base.join("fan-in")); }
    Err(format!("floor-one result not found under {}", base.display()))
}

fn cube_dir_floor1(root:&Path, cube:usize)->AnyResult<PathBuf> {
    // tolerant checkpoint lookup: the floor-one artifact nests cube dirs either at
    // the root or under shard/ (the layout that made the floor-one fan-in retrain).
    for cand in [root.join(format!("cube-{:02}",cube)), root.join("shard").join(format!("cube-{:02}",cube))] {
        if cand.join("BEST-TRAINED-CHAIN.poc1").exists() { return Ok(cand); }
    }
    Err(format!("cube-{:02} chain not found under {}", cube, root.display()))
}

fn load_floor1(base:&Path)->AnyResult<Floor1> {
    let root=find_floor1_root(base)?;
    let result_path=root.join("PAIS-OMEGA-FLOOR1-RESULT.hbp");
    let result_sha=check_sidecar(&result_path)?;
    let text=fs::read_to_string(&result_path).map_err(|e|e.to_string())?;
    let mut leaves=Vec::new(); let mut omega=String::new(); let mut anchor=String::new(); let mut leaf_lines=Vec::new();
    for line in text.lines() {
        if line.starts_with("OMEGALEAFREF|") {
            let f=parse_fields(line);
            leaves.push(Floor1Leaf{
                cube:f.get("cube").and_then(|x|x.parse().ok()).ok_or("leafref cube")?,
                source_sha:f.get("source_sha256").ok_or("leafref source")?.clone(),
                leaf_sha:f.get("leaf_sha256").ok_or("leafref leaf")?.clone(),
                archive_sha:f.get("archive_sha256").ok_or("leafref archive")?.clone(),
                chain_sha:f.get("chain_sha256").ok_or("leafref chain")?.clone(),
            });
            leaf_lines.push(line.to_string());
        } else if line.starts_with("OMEGAANCHOR|") { anchor=line.to_string(); }
        else if line.starts_with("OMEGACENTER|") { omega=parse_fields(line).get("omega_sha256").cloned().unwrap_or_default(); }
    }
    if leaves.len()!=BASE_COUNT {return Err(format!("expected 27 leafrefs got {}",leaves.len()));}
    if omega.is_empty()||anchor.is_empty() {return Err("floor-one omega/anchor missing".into());}
    let recomputed=sha_hex((anchor.clone()+"\n"+&leaf_lines.join("\n")+"\n").as_bytes());
    if recomputed!=omega {return Err(format!("floor-one omega recompute mismatch {} != {}",recomputed,omega));}
    leaves.sort_by_key(|l|l.cube);
    Ok(Floor1{root,omega,result_sha,leaves})
}

fn cube_coords(i:usize)->(usize,usize,usize) { let k=i-1; (k%3,(k/3)%3,k/9) }

fn axis_order(apex:usize)->Vec<usize> {
    // apex 0..6 = +X,-X,+Y,-Y,+Z,-Z; full 27-cube traversal ordered along the axis
    let axis=apex/2; let negative=apex%2==1;
    let mut idx:Vec<usize>=(1..=BASE_COUNT).collect();
    idx.sort_by_key(|&i| {
        let (x,y,z)=cube_coords(i);
        let primary=match axis {0=>x,1=>y,_=>z};
        let p=if negative {2-primary} else {primary};
        (p,x,y,z)
    });
    idx
}

struct BodyInput {
    index: usize,          // 1..=34
    label: String,
    composition: String,   // receipted design row
    data: Vec<u8>,
    sha: String,
}

fn build_body_input(f1:&Floor1, body:usize)->AnyResult<BodyInput> {
    if (1..=BASE_COUNT).contains(&body) {
        let leaf=&f1.leaves[body-1];
        let dir=cube_dir_floor1(&f1.root,body)?;
        let chain_path=dir.join("BEST-TRAINED-CHAIN.poc1");
        let chain=fs::read(&chain_path).map_err(|e|e.to_string())?;
        if sha_hex(&chain)!=leaf.chain_sha {return Err(format!("body {:02} chain sha mismatch",body));}
        // OLD DECODES NEW: the floor-one decoder inside this binary must restore the cube
        let native=decode_chain_floor1(&chain)?;
        if sha_hex(&native)!=leaf.source_sha {return Err(format!("body {:02} floor-one restore mismatch",body));}
        let sha=sha_hex(&chain);
        Ok(BodyInput{index:body,label:format!("BASE-{:02}",body),
            composition:format!("floor1_best_trained_chain|cube={:02}|chain_sha256={}|floor1_restore=1|timing_free_input=1",body,leaf.chain_sha),
            data:chain,sha})
    } else if (BASE_COUNT+1..=BASE_COUNT+6).contains(&body) {
        let apex=body-BASE_COUNT-1;
        let order=axis_order(apex);
        let mut data=Vec::new(); let mut parts=Vec::new();
        for &cube in &order {
            let leaf=&f1.leaves[cube-1];
            let dir=cube_dir_floor1(&f1.root,cube)?;
            let chain=fs::read(dir.join("BEST-TRAINED-CHAIN.poc1")).map_err(|e|e.to_string())?;
            if sha_hex(&chain)!=leaf.chain_sha {return Err(format!("apex {} cube {:02} chain sha mismatch",APEX_NAMES[apex],cube));}
            let payloads=parse_chain_payloads_floor1(&chain)?;
            let last=payloads.last().ok_or("empty chain payloads")?;
            parts.push(format!("{:02}:{}",cube,last.len()));
            data.extend_from_slice(last);
        }
        let sha=sha_hex(&data);
        let order_str:Vec<String>=order.iter().map(|c|format!("{:02}",c)).collect();
        Ok(BodyInput{index:body,label:format!("APEX{}",APEX_NAMES[apex]),
            composition:format!("floor1_final_epoch_payloads|axis={}|order={}|parts={}|timing_free_input=1",APEX_NAMES[apex],order_str.join(">"),parts.join(",")),
            data,sha})
    } else if body==BODY_COUNT {
        // LIRIS timing-contamination flag (2026-07-15): the junction body trains ONLY on
        // timing-free, seat-reproducible fields (source/archive/chain SHAs). Leaf hashes
        // and the floor-one omega carry elapsed_ms in their preimage and are EXCLUDED
        // from the training bytes (they stay pinned in receipts, not in the stream).
        let mut lines=Vec::new();
        lines.push("F2JUNCTIONHDR|schema=PAIS-OMEGA-FLOOR2-JUNCTION-V1|cubes=27|fields=source_archive_chain_shas_only|leaf_hashes_excluded=1|floor1_omega_excluded=1|timing_free=1|json=0".to_string());
        for leaf in &f1.leaves {
            lines.push(format!("F2JUNCTION|cube={:02}|source_sha256={}|archive_sha256={}|chain_sha256={}|json=0",leaf.cube,leaf.source_sha,leaf.archive_sha,leaf.chain_sha));
        }
        let data=(lines.join("\n")+"\n").into_bytes();
        let sha=sha_hex(&data);
        Ok(BodyInput{index:body,label:"OMEGA-JUNCTION".into(),
            composition:format!("floor1_junction_shas|cubes=27|timing_free=1|leaf_hashes_excluded=1"),
            data,sha})
    } else { Err(format!("body must be 1..={}, got {}",BODY_COUNT,body)) }
}

// ---------- floor-two body training ----------

struct BodyResult {
    index: usize,
    bits: u32,
    input_sha: String,
    leaf_sha: String,
    gain_bytes: u64,
    accepted: u64,
    held: u64,
    best_payload_bytes: usize,
    chain_sha: String,
}

fn body_dir_name(body:usize, bits:u32)->String {
    if bits==CONTROL_BITS { format!("body-{:02}-control64",body) } else { format!("body-{:02}",body) }
}

fn checkpoint_body(dir:&Path, input:&BodyInput, bits:u32)->AnyResult<Option<BodyResult>> {
    let meta=dir.join("BODY-META.hbp"); let receipt=dir.join("BODY-RESULT.hbp");
    if !meta.exists()||!receipt.exists(){return Ok(None);}
    let line=fs::read_to_string(&meta).map_err(|e|e.to_string())?; let f=parse_fields(line.trim());
    if f.get("status").map(String::as_str)!=Some("PASS")||f.get("input_sha").map(String::as_str)!=Some(input.sha.as_str())||f.get("bits").map(String::as_str)!=Some(bits.to_string().as_str()){return Ok(None);}
    if check_sidecar(&receipt).is_err(){return Ok(None);}
    Ok(Some(BodyResult{index:input.index,bits,input_sha:input.sha.clone(),
        leaf_sha:f["leaf_sha"].clone(),
        gain_bytes:f["gain_bytes"].parse().map_err(|_|"bad ckpt gain")?,
        accepted:f["accepted"].parse().map_err(|_|"bad ckpt accepted")?,
        held:f["held"].parse().map_err(|_|"bad ckpt held")?,
        best_payload_bytes:f["best_payload_bytes"].parse().map_err(|_|"bad ckpt best")?,
        chain_sha:f["chain_sha"].clone()}))
}

fn train_body(input:&BodyInput, out_root:&Path, bits:u32, contract_sha:&str, floor1_omega:&str)->AnyResult<BodyResult> {
    let body_dir=out_root.join(body_dir_name(input.index,bits));
    fs::create_dir_all(&body_dir).map_err(|e|e.to_string())?;
    if let Some(r)=checkpoint_body(&body_dir,input,bits)?{println!("BODY_RESUME|body={:02}|bits={}|status=PASS",input.index,bits);return Ok(r);}
    let glyphs=bytes_to_glyphs(&input.data,bits);
    println!("BODY_START|body={:02}|bits={}|label={}|bytes={}|glyphs={}|sha256={}",input.index,bits,input.label,input.data.len(),glyphs.len(),input.sha);
    let started=Instant::now();
    let source_sha=sha256(&input.data);
    // exact glyph round-trip gate before anything trains
    if glyphs_to_bytes(&glyphs,bits,input.data.len())!=input.data {return Err(format!("body {:02} glyph roundtrip failed",input.index));}
    let (group_ok,vertex_hashes,group_detail)=group_gate_glyphs(&glyphs,bits);
    if !group_ok{return Err(format!("body {:02} glyph R/N/Q group gate failed: {}",input.index,group_detail));}
    let mut rows=Vec::new();
    rows.push(format!("PAISBODYHDR|schema=PAIS-OMEGA-FLOOR2-BODY-V1|body={:02}|bits={}|label={}|input_bytes={}|input_glyphs={}|input_sha256={}|contract_sha256={}|floor1_omega={}|cells=800|higher_floors=HELD|json=0",input.index,bits,input.label,input.data.len(),glyphs.len(),input.sha,contract_sha,floor1_omega));
    rows.push(format!("COMPOSE|body={:02}|{}|old_decodes_new=1|json=0",input.index,input.composition));
    rows.push(format!("GROUPGATE|body={:02}|group=C2^3_CONFIRMED_ON_GLYPHS|{}|vertices_sha256={}|all_inputs_distinct=1|status=PASS|json=0",input.index,group_detail,sha_hex(vertex_hashes.join("|").as_bytes())));
    let mut play_rows=Vec::new();
    for (axis,name) in [("R","R"),("N","N"),("Q","Q")] {
        let moved=match name {"R"=>g_r(&glyphs),"N"=>g_n(&glyphs,bits),_=>g_q(&glyphs,bits)};
        let back=match name {"R"=>g_r(&moved),"N"=>g_n(&moved,bits),_=>g_q(&moved,bits)};
        if back!=glyphs{return Err(format!("body {:02} axis {} failed",input.index,axis));}
        for sign in ['+','-'] {play_rows.push(format!("PLAY|body={:02}|dir={}{}|axis={}|from_sha256={}|to_sha256={}|back_sha256={}|roundtrip=1|same_transform_for_sign=1|json=0",input.index,sign,name,axis,input.sha,sha_hex(&pack_glyphs(&moved,bits)),sha_hex(&pack_glyphs(&back,bits))));}
    }
    let play_gate_sha=sha_hex((play_rows.join("\n")+"\n").as_bytes()); rows.extend(play_rows);
    let mut gain_total=0u64; let mut accepted=0u64; let mut held=0u64; let mut best:Option<BestChain>=None;
    for a in 0..8 {
        let view=a_apply_glyphs(a,&glyphs,bits,&source_sha);
        let restored=a_inverse_glyphs(a,&view,bits,&source_sha);
        if restored!=glyphs{return Err(format!("body {:02} A inverse {} failed",input.index,A_NAMES[a]));}
        let view_packed=pack_glyphs(&view,bits);
        let view_sha=sha_hex(&view_packed);
        rows.push(format!("AVIEWGATE|body={:02}|a={}|view_sha256={}|inverse_sha256={}|roundtrip=1|json=0",input.index,A_NAMES[a],view_sha,sha_hex(&pack_glyphs(&restored,bits))));
        for direction in 0..2u8 { for order in 1..=5u8 {
            let seq:Vec<u16>=if direction==0{view.clone()}else{view.iter().rev().copied().collect()};
            let mut enc=PredictorModel::new(bits,order,direction);
            let mut dec=PredictorModel::new(bits,order,direction);
            let mut lane_payloads=Vec::new(); let mut lane_min=usize::MAX;
            for epoch in 1..=EPOCHS {
                let before=hex(&enc.commit);
                let (residual,m)=enc.encode(&seq);
                let payload=lz_compress(&pack_glyphs(&residual,bits));
                let payload_sha=sha_hex(&payload);
                let decoded_packed=lz_decompress(&payload)?;
                let decoded_residual=unpack_glyphs(&decoded_packed,bits,seq.len());
                let (decoded_seq,dm)=dec.decode(&decoded_residual);
                let state_match=enc.commit==dec.commit&&enc.counts.len()==dec.counts.len()&&enc.best.len()==dec.best.len()&&m.predictions==dm.predictions&&m.unseen_contexts==dm.unseen_contexts;
                if decoded_seq!=seq||!state_match{return Err(format!("body {:02} cell restore a={} d={} o={} e={}",input.index,a,direction,order,epoch));}
                if epoch==EPOCHS&&enc!=dec{return Err(format!("body {:02} terminal model mismatch a={} d={} o={}",input.index,a,direction,order));}
                let cost=payload.len();
                let gain=view_packed.len().saturating_sub(cost) as u64;
                let decision=if gain>0{accepted+=1;gain_total+=gain;"ACCEPT"}else{held+=1;"HOLD"};
                lane_min=lane_min.min(cost);
                let actor=pid8(&format!("PAIS-F2|{:02}|{}|{}|{}|{}",input.index,bits,A_NAMES[a],B_DIRECTIONS[direction as usize],order));
                rows.push(format!("CELL|body={:02}|bits={}|a={}|b_direction={}|b_order={}|c_epoch={}|actor_pid={}|input_sha256={}|view_sha256={}|state_before={}|state_after={}|predictions={}|top1_correct={}|unseen_contexts={}|novel_pairs={}|confident_blunders={}|model_pairs={}|payload_bytes={}|payload_sha256={}|gain_bytes={}|decision={}|restore=1|state_match=1|play_gate_sha256={}|conditioning=VARIABLE_ORDER_PREDICTIVE_RESIDUAL_GLYPH_V2|json=0",input.index,bits,A_NAMES[a],B_DIRECTIONS[direction as usize],order,epoch,actor,input.sha,view_sha,before,hex(&enc.commit),m.predictions,m.top1_correct,m.unseen_contexts,m.novel_pairs,m.confident_blunders,enc.counts.len(),cost,payload_sha,gain,decision,play_gate_sha));
                lane_payloads.push(payload);
            }
            if best.as_ref().map(|b|lane_min<b.min_payload).unwrap_or(true){best=Some(BestChain{a_index:a as u8,direction,order,payloads:lane_payloads,min_payload:lane_min});}
        }}
    }
    if accepted+held!=800{return Err(format!("body {:02} cell count {}",input.index,accepted+held));}
    let best=best.ok_or("no best chain")?;
    let chain=chain_bytes_floor2(&best,&source_sha,bits,input.data.len(),glyphs.len());
    if decode_chain_floor2(&chain)?!=input.data{return Err(format!("body {:02} best chain restore",input.index));}
    let chain_path=body_dir.join("BEST-TRAINED-CHAIN.poc2");
    fs::write(&chain_path,&chain).map_err(|e|e.to_string())?;
    let chain_sha=write_sidecar(&chain_path)?;
    rows.push(format!("DENSITY|scope=body|body={:02}|bits={}|accepted_gain_bytes={}|input_glyphs={}|ratio_num={}|ratio_den={}|accepted={}|held={}|meaning=structure_repetition_only|archive_ratio=NOT_CLAIMED|json=0",input.index,bits,gain_total,glyphs.len(),gain_total,glyphs.len(),accepted,held));
    // LIRIS leaf-preimage law (2026-07-15): wall-clock never enters the leaf hash.
    // elapsed_ms is receipted AFTER the leaf is sealed, so leaf hashes and the
    // floor-two Omega are seat-convergent, not just science-convergent.
    rows.push(format!("BODYRESTORE|body={:02}|input_sha256={}|best_chain_sha256={}|restore=1|leaf_preimage=timing_free|json=0",input.index,input.sha,chain_sha));
    let leaf_sha=sha_hex((rows.join("\n")+"\n").as_bytes());
    rows.push(format!("OMEGALEAF|body={:02}|bits={}|input_sha256={}|cells=800|plays=6|leaf_sha256={}|restore=1|json=0",input.index,bits,input.sha,leaf_sha));
    rows.push(format!("TIMING|body={:02}|elapsed_ms={}|hashed_into_leaf=0|json=0",input.index,started.elapsed().as_millis()));
    rows.push(format!("PAISBODYFTR|body={:02}|bits={}|cells=800|accepted={}|held={}|gain_bytes={}|best_payload_bytes={}|restore=1|status=PASS|json=0",input.index,bits,accepted,held,gain_total,best.min_payload));
    let receipt=body_dir.join("BODY-RESULT.hbp");
    write_lf(&receipt,&(rows.join("\n")+"\n"))?; write_sidecar(&receipt)?;
    let meta=body_dir.join("BODY-META.hbp");
    write_lf(&meta,&format!("BODYMETA|body={:02}|bits={}|input_sha={}|leaf_sha={}|gain_bytes={}|accepted={}|held={}|best_payload_bytes={}|chain_sha={}|status=PASS|json=0\n",input.index,bits,input.sha,leaf_sha,gain_total,accepted,held,best.min_payload,chain_sha))?;
    write_sidecar(&meta)?;
    println!("BODY_OK|body={:02}|bits={}|cells=800|accepted={}|held={}|gain={}|leaf={}",input.index,bits,accepted,held,gain_total,leaf_sha);
    Ok(BodyResult{index:input.index,bits,input_sha:input.sha.clone(),leaf_sha,gain_bytes:gain_total,accepted,held,best_payload_bytes:best.min_payload,chain_sha})
}

fn hbi_for(hbp:&str)->String {
    let mut out=String::new();
    for (i,line) in hbp.lines().enumerate(){out.push_str(&format!("HBI|row={}|sha256={}|hex={}|json=0\n",i+1,sha_hex(line.as_bytes()),hex(line.as_bytes())));} out
}

// ---------- shard + fan-in ----------

fn run_shard(floor1:&Path, contract:&Path, output:&Path, body:usize, bits:u32)->AnyResult<()> {
    fs::create_dir_all(output).map_err(|e|e.to_string())?;
    let contract_bytes=fs::read(contract).map_err(|e|e.to_string())?;
    let contract_sha=sha_hex(&contract_bytes);
    let f1=load_floor1(floor1)?;
    let input=build_body_input(&f1,body)?;
    let result=train_body(&input,output,bits,&contract_sha,&f1.omega)?;
    let marker=if bits==CONTROL_BITS {"FLOOR2_CONTROL_PASS"} else {"FLOOR2_SHARD_PASS"};
    println!("{}|body={:02}|bits={}|cells=800|accepted={}|held={}|gain_bytes={}|leaf_sha256={}|status=PASS",marker,result.index,bits,result.accepted,result.held,result.gain_bytes,result.leaf_sha);
    Ok(())
}

fn run_train(floor1:&Path, contract:&Path, output:&Path, workers:usize)->AnyResult<()> {
    fs::create_dir_all(output).map_err(|e|e.to_string())?;
    let contract_bytes=fs::read(contract).map_err(|e|e.to_string())?;
    let contract_sha=sha_hex(&contract_bytes); write_sidecar(contract)?;
    let f1=load_floor1(floor1)?;
    // negative controls
    let zero=vec![0u16;4096];
    let (zero_pass,_,_)=group_gate_glyphs(&zero,FLOOR2_BITS);
    if zero_pass{return Err("zero glyph distinctness negative control failed".into());}
    let probe=build_body_input(&f1,1)?;
    let mut corrupt=probe.data.clone(); if let Some(first)=corrupt.first_mut(){*first^=1;}
    if sha_hex(&corrupt)==probe.sha {return Err("corruption negative control failed".into());}
    if decode_chain_floor1(&corrupt).is_ok(){return Err("corrupt chain decode negative control failed".into());}
    // build all 34 inputs up front (verifies every chain sha + floor-one restore per body)
    let mut inputs=Vec::new();
    for body in 1..=BODY_COUNT { inputs.push(build_body_input(&f1,body)?); }
    let queue=Arc::new(Mutex::new(VecDeque::from(inputs.iter().map(|i|i.index).collect::<Vec<_>>())));
    let inputs_arc=Arc::new(inputs);
    let (tx,rx)=mpsc::channel();
    let worker_count=workers.max(1).min(BODY_COUNT);
    let out_arc=Arc::new(output.to_path_buf());
    let cs=Arc::new(contract_sha.clone());
    let omega1=Arc::new(f1.omega.clone());
    let mut handles=Vec::new();
    for _ in 0..worker_count{
        let q=Arc::clone(&queue); let tx=tx.clone(); let out=Arc::clone(&out_arc); let cs=Arc::clone(&cs); let om=Arc::clone(&omega1); let ins=Arc::clone(&inputs_arc);
        handles.push(thread::spawn(move||loop{
            let body={q.lock().unwrap().pop_front()};
            match body{Some(b)=>{let input=&ins[b-1];let r=train_body(input,&out,FLOOR2_BITS,&cs,&om);let _=tx.send(r);},None=>break}
        }));
    }
    drop(tx);
    let mut results=Vec::new(); let mut errors=Vec::new();
    for r in rx{match r{Ok(x)=>results.push(x),Err(e)=>errors.push(e)}}
    for h in handles{let _=h.join();}
    if !errors.is_empty(){return Err(errors.join("; "));}
    if results.len()!=BODY_COUNT{return Err(format!("expected {} body results got {}",BODY_COUNT,results.len()));}
    results.sort_by_key(|r|r.index);
    // control arm: body 01 input at 6 bits (resumes from its artifact checkpoint if present)
    let control=train_body(&inputs_arc[0],output,CONTROL_BITS,&contract_sha,&f1.omega)?;
    let mut hbp=Vec::new();
    hbp.push(format!("PAISFLOORHDR|schema=PAIS-OMEGA-FLOOR2-V1|authority=OPERATOR_FLOOR2_UNLOCK_2026-07-15|mode=SHADOW_MEASURED|floor=2|body_count=34|base=27|apex=6|omega_bodies=1|bits=10|control_bits=6|ring_a=8|ring_b=10|ring_c=10|cells_per_body=800|cells_total=27200|directions=+R,-R,+N,-N,+Q,-Q|higher_floors=HELD_OPERATOR_SCOPE|contract_sha256={}|floor1_omega={}|floor1_result_sha256={}|json=0",contract_sha,f1.omega,f1.result_sha));
    hbp.push("CONTROL|name=ALL_ZERO_GLYPH_DISTINCTNESS|expected=FAIL_DISTINCT|observed=FAIL_DISTINCT|status=PASS|json=0".into());
    hbp.push("CONTROL|name=ONE_BYTE_CORRUPTION|expected=SHA_DIFFERENT_AND_DECODE_FAIL|observed=SHA_DIFFERENT_AND_DECODE_FAIL|status=PASS|json=0".into());
    let mut total_gain=0u64; let mut total_accept=0u64; let mut total_hold=0u64; let mut leaves=Vec::new();
    for r in &results{
        let receipt=output.join(body_dir_name(r.index,FLOOR2_BITS)).join("BODY-RESULT.hbp");
        let text=fs::read_to_string(&receipt).map_err(|e|e.to_string())?;
        hbp.extend(text.lines().map(str::to_string));
        total_gain+=r.gain_bytes; total_accept+=r.accepted; total_hold+=r.held;
        leaves.push(format!("OMEGALEAFREF|body={:02}|input_sha256={}|leaf_sha256={}|chain_sha256={}|json=0",r.index,r.input_sha,r.leaf_sha,r.chain_sha));
    }
    let control_receipt=output.join(body_dir_name(1,CONTROL_BITS)).join("BODY-RESULT.hbp");
    let control_text=fs::read_to_string(&control_receipt).map_err(|e|e.to_string())?;
    hbp.extend(control_text.lines().map(str::to_string));
    let body1=&results[0];
    let verdict=if control.gain_bytes<body1.gain_bytes {"CONTROL_COLLAPSED_AS_PREDICTED"} else {"CONTROL_DID_NOT_COLLAPSE_LAW_UNDER_REVIEW"};
    hbp.push(format!("CONTROLCOMPARE|body01_bits10_gain={}|body01_bits10_accepted={}|control_bits6_gain={}|control_bits6_accepted={}|prediction=64_collapses|observed={}|json=0",body1.gain_bytes,body1.accepted,control.gain_bytes,control.accepted,verdict));
    let anchor=format!("OMEGAANCHOR|schema=PAIS-OMEGA-FLOOR2-V1|contract_sha256={}|floor1_omega={}|body_count=34|epoch=FLOOR2_ONLY|json=0",contract_sha,f1.omega);
    let omega=sha_hex((anchor.clone()+"\n"+&leaves.join("\n")+"\n").as_bytes());
    hbp.push(anchor); hbp.extend(leaves.clone());
    hbp.push(format!("OMEGACENTER|method=sha256_over_anchor_plus_34_ordered_leaves_lf|omega_sha256={}|leaf_count=34|all_restore=1|higher_floors=HELD|json=0",omega));
    let total_glyphs:u64=results.iter().map(|r|{let d=&inputs_arc[r.index-1].data;((d.len() as u64)*8+9)/10}).sum();
    hbp.push(format!("DENSITY|scope=cohort|bits=10|accepted_gain_bytes={}|input_glyphs={}|ratio_num={}|ratio_den={}|accepted={}|held={}|meaning=structure_repetition_only|archive_ratio=NOT_CLAIMED|json=0",total_gain,total_glyphs,total_gain,total_glyphs,total_accept,total_hold));
    hbp.push(format!("PAISFLOORFTR|floor=2|cells=27200|accepted={}|held={}|restore_bodies=34_of_34|floor1_restore=27_of_27|omega={}|higher_floors=HELD|compression_record=NOT_CLAIMED|physics_validation=NOT_CLAIMED|status=PASS|json=0",total_accept,total_hold,omega));
    let floor_text=hbp.join("\n")+"\n";
    let floor=output.join("PAIS-OMEGA-FLOOR2-RESULT.hbp");
    write_lf(&floor,&floor_text)?;
    let floor_sha=write_sidecar(&floor)?;
    let hbi=output.join("PAIS-OMEGA-FLOOR2-RESULT.hbi");
    write_lf(&hbi,&hbi_for(&floor_text))?;
    let hbi_sha=write_sidecar(&hbi)?;
    let sums=format!("{}  PAIS-OMEGA-FLOOR2-RESULT.hbp\n{}  PAIS-OMEGA-FLOOR2-RESULT.hbi\n",floor_sha,hbi_sha);
    let sums_path=output.join("SHA256SUMS");
    write_lf(&sums_path,&sums)?; write_sidecar(&sums_path)?;
    println!("PAIS_FLOOR2_PASS|bodies=34|cells=27200|accepted={}|held={}|gain_bytes={}|body01_1024_gain={}|control64_gain={}|control={}|omega={}|floor1_omega={}|result_sha256={}|higher_floors=HELD",total_accept,total_hold,total_gain,body1.gain_bytes,control.gain_bytes,verdict,omega,f1.omega,floor_sha);
    Ok(())
}

// ---------- selftest (no floor-one tree needed) ----------

fn selftest()->AnyResult<()> {
    // deterministic pseudo-data from chained sha256 (no OS randomness)
    let mut data=Vec::new(); let mut seed=sha256(b"PAIS-FLOOR2-SELFTEST-V1");
    while data.len()<60000 { data.extend_from_slice(&seed); seed=sha256(&seed); }
    data.truncate(59999); // odd length exercises padding
    for &bits in &[FLOOR2_BITS,CONTROL_BITS,8u32] {
        let glyphs=bytes_to_glyphs(&data,bits);
        if glyphs_to_bytes(&glyphs,bits,data.len())!=data {return Err(format!("selftest roundtrip bits={}",bits));}
        let (ok,_,detail)=group_gate_glyphs(&glyphs,bits);
        if !ok {return Err(format!("selftest group gate bits={}: {}",bits,detail));}
        let source_sha=sha256(&data);
        for a in 0..8 {
            let v=a_apply_glyphs(a,&glyphs,bits,&source_sha);
            if a_inverse_glyphs(a,&v,bits,&source_sha)!=glyphs {return Err(format!("selftest A{} bits={}",a,bits));}
        }
        for direction in 0..2u8 { for order in [1u8,3,5] {
            let seq:Vec<u16>=if direction==0{glyphs.clone()}else{glyphs.iter().rev().copied().collect()};
            let mut enc=PredictorModel::new(bits,order,direction);
            let mut dec=PredictorModel::new(bits,order,direction);
            for _ in 0..2 {
                let (residual,_)=enc.encode(&seq);
                let payload=lz_compress(&pack_glyphs(&residual,bits));
                let back=unpack_glyphs(&lz_decompress(&payload)?,bits,seq.len());
                let (decoded,_)=dec.decode(&back);
                if decoded!=seq||enc.commit!=dec.commit {return Err(format!("selftest predictor bits={} o={} d={}",bits,order,direction));}
            }
        }}
    }
    // chain2 roundtrip
    let glyphs=bytes_to_glyphs(&data,FLOOR2_BITS);
    let source_sha=sha256(&data);
    let mut enc=PredictorModel::new(FLOOR2_BITS,2,0);
    let mut payloads=Vec::new(); let mut min=usize::MAX;
    for _ in 0..3 { let (r,_)=enc.encode(&glyphs); let p=lz_compress(&pack_glyphs(&r,FLOOR2_BITS)); min=min.min(p.len()); payloads.push(p); }
    let chain=chain_bytes_floor2(&BestChain{a_index:0,direction:0,order:2,payloads,min_payload:min},&source_sha,FLOOR2_BITS,data.len(),glyphs.len());
    if decode_chain_floor2(&chain)?!=data {return Err("selftest chain2 roundtrip".into());}
    let mut corrupt=chain.clone(); let mid=corrupt.len()/2; corrupt[mid]^=1;
    if decode_chain_floor2(&corrupt).is_ok() {return Err("selftest chain2 corruption not caught".into());}
    // axis orders are permutations and distinct
    let mut seen=HashSet::new();
    for apex in 0..6 {
        let o=axis_order(apex);
        let mut s=o.clone(); s.sort();
        if s!=(1..=BASE_COUNT).collect::<Vec<_>>() {return Err(format!("selftest axis {} not a permutation",apex));}
        if !seen.insert(o.clone()) {return Err(format!("selftest axis {} duplicate order",apex));}
    }
    println!("SELFTEST_PASS|bits=10,6,8|transforms=8|predictor=OK|chain2=OK|axis_orders=6_distinct");
    Ok(())
}

fn flag(args:&[String],name:&str)->AnyResult<String>{let i=args.iter().position(|x|x==name).ok_or_else(||format!("missing {}",name))?;args.get(i+1).cloned().ok_or_else(||format!("missing value for {}",name))}

fn main()->Result<(),String>{
    let args:Vec<String>=env::args().collect();
    if args.len()<2{return Err("usage: selftest | shard --floor1 DIR --contract PATH --output DIR --body N [--control64] | train --floor1 DIR --contract PATH --output DIR [--workers N]".into());}
    match args[1].as_str() {
        "selftest"=>selftest(),
        "shard"=>{
            let floor1=PathBuf::from(flag(&args,"--floor1")?);
            let contract=PathBuf::from(flag(&args,"--contract")?);
            let output=PathBuf::from(flag(&args,"--output")?);
            let body:usize=flag(&args,"--body")?.parse().map_err(|_|"bad --body")?;
            let bits=if args.iter().any(|a|a=="--control64"){CONTROL_BITS}else{FLOOR2_BITS};
            run_shard(&floor1,&contract,&output,body,bits)
        },
        "train"=>{
            let floor1=PathBuf::from(flag(&args,"--floor1")?);
            let contract=PathBuf::from(flag(&args,"--contract")?);
            let output=PathBuf::from(flag(&args,"--output")?);
            let workers=flag(&args,"--workers").ok().and_then(|x|x.parse().ok()).unwrap_or(4);
            run_train(&floor1,&contract,&output,workers)
        },
        _=>Err("unknown command".into()),
    }
}
