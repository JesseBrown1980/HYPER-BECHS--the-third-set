use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::{mpsc, Arc, Mutex};
use std::thread;
use std::time::Instant;

type AnyResult<T> = Result<T, String>;

const CUBE_COUNT: usize = 27;
const EPOCHS: usize = 10;
const A_NAMES: [&str; 8] = [
    "DBBH_FORWARD_IDENTITY",
    "DBBH_REVERSE_BYTES",
    "DBWH_FORWARD_XOR_DELTA",
    "DBWH_REVERSE_ROTATE_BITS",
    "MIRROR_NIBBLE_SWAP",
    "PI_SLICE_BLOCK_REVERSE",
    "NESTED_EVEN_ODD",
    "QPRISM_PRIME_BLOCK_SHA256",
];
const B_DIRECTIONS: [&str; 2] = ["BLACK_FORWARD", "WHITE_REVERSE"];

#[derive(Clone)]
struct Patent {
    id: String,
    bytes: usize,
    sha: String,
    file: String,
    offset: usize,
}

#[derive(Clone)]
struct Cube {
    index: usize,
    start: usize,
    end: usize,
    data: Vec<u8>,
    sha: String,
}

#[derive(Clone)]
struct CubeResult {
    index: usize,
    source_sha: String,
    leaf_sha: String,
    gain_bytes: u64,
    accepted: u64,
    held: u64,
    best_payload_bytes: usize,
    archive_sha: String,
    chain_sha: String,
}

#[derive(Clone, PartialEq, Eq)]
struct BestState {
    total: u32,
    best_symbol: u8,
    best_count: u32,
}

#[derive(Clone, PartialEq, Eq)]
struct PredictorModel {
    order: u8,
    direction: u8,
    counts: HashMap<(u64, u8), u32>,
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

struct BestChain {
    a_index: u8,
    direction: u8,
    order: u8,
    payloads: Vec<Vec<u8>>,
    min_payload: usize,
}

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

fn load_patents(manifest: &Path) -> AnyResult<(Vec<Patent>, Vec<u8>, String, String)> {
    let manifest_bytes = fs::read(manifest).map_err(|e| format!("manifest: {}", e))?;
    let manifest_sha = sha_hex(&manifest_bytes);
    let sidecar_path = PathBuf::from(format!("{}.sha256", manifest.display()));
    let sidecar = fs::read_to_string(&sidecar_path).map_err(|e| format!("manifest sidecar: {}", e))?;
    let expected = sidecar.split_whitespace().next().ok_or("empty manifest sidecar")?;
    if expected != manifest_sha { return Err("manifest sidecar SHA mismatch".into()); }
    let root = manifest.parent().ok_or("manifest has no parent")?;
    let text = String::from_utf8(manifest_bytes).map_err(|e| e.to_string())?;
    let mut patents = Vec::new();
    let mut corpus = Vec::new();
    for line in text.lines().filter(|l| l.starts_with("PAISPATENT|")) {
        let f = parse_fields(line);
        let id = f.get("id").ok_or("patent id missing")?.clone();
        let bytes: usize = f.get("bytes").ok_or("patent bytes missing")?.parse().map_err(|_| "bad patent bytes")?;
        let expected_sha = f.get("sha256").ok_or("patent sha missing")?.clone();
        let file = f.get("file").ok_or("patent file missing")?.clone();
        if file.contains("..") || Path::new(&file).is_absolute() { return Err(format!("unsafe patent path {}", file)); }
        let body = fs::read(root.join(&file)).map_err(|e| format!("{}: {}", id, e))?;
        if body.len() != bytes || body.get(0..4) != Some(b"%PDF") || sha_hex(&body) != expected_sha {
            return Err(format!("patent integrity failed: {}", id));
        }
        let offset = corpus.len();
        corpus.extend_from_slice(&body);
        patents.push(Patent { id, bytes, sha: expected_sha, file, offset });
    }
    if patents.len() != 11 { return Err(format!("expected 11 patents, got {}", patents.len())); }
    let corpus_sha = sha_hex(&corpus);
    Ok((patents, corpus, corpus_sha, manifest_sha))
}

fn partition_cubes(corpus: &[u8]) -> Vec<Cube> {
    let q = corpus.len()/CUBE_COUNT;
    let r = corpus.len()%CUBE_COUNT;
    let mut cubes = Vec::new();
    let mut start = 0usize;
    for i in 0..CUBE_COUNT {
        let n = q + usize::from(i < r);
        let end = start+n;
        let data = corpus[start..end].to_vec();
        let sha = sha_hex(&data);
        cubes.push(Cube { index:i+1, start, end, data, sha });
        start=end;
    }
    cubes
}

fn t_r(data: &[u8]) -> Vec<u8> { data.iter().rev().copied().collect() }
fn t_n(data: &[u8]) -> Vec<u8> { data.iter().map(|b| (b<<4)|(b>>4)).collect() }
fn reverse_nibble(x: u8) -> u8 { ((x&1)<<3)|((x&2)<<1)|((x&4)>>1)|((x&8)>>3) }
fn t_q(data: &[u8]) -> Vec<u8> { data.iter().map(|b| (reverse_nibble(b>>4)<<4)|reverse_nibble(b&15)).collect() }

fn geometry_view(data: &[u8], mask: u8) -> Vec<u8> {
    let mut out = data.to_vec();
    if mask&1 != 0 { out=t_r(&out); }
    if mask&2 != 0 { out=t_n(&out); }
    if mask&4 != 0 { out=t_q(&out); }
    out
}

fn group_gate(data: &[u8]) -> (bool, Vec<String>, String) {
    let rr=t_r(&t_r(data))==data;
    let nn=t_n(&t_n(data))==data;
    let qq=t_q(&t_q(data))==data;
    let rn=t_r(&t_n(data))==t_n(&t_r(data));
    let rq=t_r(&t_q(data))==t_q(&t_r(data));
    let nq=t_n(&t_q(data))==t_q(&t_n(data));
    let mut views=Vec::new();
    let mut uniq=HashSet::new();
    for m in 0..8 { let v=geometry_view(data,m); let h=sha_hex(&v); uniq.insert(h.clone()); views.push(h); }
    let rnq=geometry_view(data,7);
    let total:Vec<u8>=data.iter().rev().map(|b| b.reverse_bits()).collect();
    let total_ok=rnq==total;
    (rr&&nn&&qq&&rn&&rq&&nq&&uniq.len()==8&&total_ok, views, format!("squares={},{},{}|commutators={},{},{}|distinct={}|rnq_total={}", u8::from(rr),u8::from(nn),u8::from(qq),u8::from(rn),u8::from(rq),u8::from(nq),uniq.len(),u8::from(total_ok)))
}

fn xor_delta(data: &[u8]) -> Vec<u8> {
    if data.is_empty() { return Vec::new(); }
    let mut out=Vec::with_capacity(data.len()); out.push(data[0]);
    for i in 1..data.len() { out.push(data[i]^data[i-1]); }
    out
}
fn xor_undelta(data: &[u8]) -> Vec<u8> {
    if data.is_empty() { return Vec::new(); }
    let mut out=Vec::with_capacity(data.len()); out.push(data[0]);
    for i in 1..data.len() { let b=data[i]^out[i-1]; out.push(b); }
    out
}
fn block_reverse(data: &[u8], block: usize) -> Vec<u8> {
    let mut out=Vec::with_capacity(data.len());
    for c in data.chunks(block) { out.extend(c.iter().rev()); }
    out
}
fn even_odd(data: &[u8]) -> Vec<u8> {
    data.iter().step_by(2).chain(data.iter().skip(1).step_by(2)).copied().collect()
}
fn undo_even_odd(data: &[u8]) -> Vec<u8> {
    let even=(data.len()+1)/2; let mut out=vec![0u8;data.len()];
    for i in 0..even { out[i*2]=data[i]; }
    for i in even..data.len() { out[(i-even)*2+1]=data[i]; }
    out
}

fn qprism_order(nblocks: usize, source_sha: &[u8;32]) -> Vec<usize> {
    let mut keyed:Vec<([u8;32],usize)>=(0..nblocks).map(|i| {
        let mut seed=b"QPRISM_PRIME_BLOCK_SHA256_V1|257|".to_vec();
        seed.extend_from_slice(source_sha); seed.extend_from_slice(&(i as u64).to_le_bytes());
        (sha256(&seed),i)
    }).collect();
    keyed.sort_by(|a,b| a.0.cmp(&b.0).then(a.1.cmp(&b.1)));
    keyed.into_iter().map(|x|x.1).collect()
}

fn qprism(data: &[u8], source_sha: &[u8;32]) -> Vec<u8> {
    let block=257usize; let n=data.len()/block; let order=qprism_order(n,source_sha);
    let mut out=Vec::with_capacity(data.len());
    for orig in order { out.extend_from_slice(&data[orig*block..(orig+1)*block]); }
    out.extend_from_slice(&data[n*block..]); out
}
fn undo_qprism(data: &[u8], source_sha: &[u8;32]) -> Vec<u8> {
    let block=257usize; let n=data.len()/block; let order=qprism_order(n,source_sha);
    let mut out=vec![0u8;data.len()];
    for (pos,orig) in order.into_iter().enumerate() {
        out[orig*block..(orig+1)*block].copy_from_slice(&data[pos*block..(pos+1)*block]);
    }
    out[n*block..].copy_from_slice(&data[n*block..]); out
}

fn a_apply(index: usize, data: &[u8], source_sha: &[u8;32]) -> Vec<u8> {
    match index {
        0=>data.to_vec(),
        1=>t_r(data),
        2=>xor_delta(data),
        3=>data.iter().rev().map(|b|b.rotate_left(1)).collect(),
        4=>t_n(data),
        5=>block_reverse(data,256),
        6=>even_odd(data),
        7=>qprism(data,source_sha),
        _=>unreachable!(),
    }
}
fn a_inverse(index: usize, data: &[u8], source_sha: &[u8;32]) -> Vec<u8> {
    match index {
        0=>data.to_vec(),
        1=>t_r(data),
        2=>xor_undelta(data),
        3=>data.iter().map(|b|b.rotate_right(1)).rev().collect(),
        4=>t_n(data),
        5=>block_reverse(data,256),
        6=>undo_even_odd(data),
        7=>undo_qprism(data,source_sha),
        _=>unreachable!(),
    }
}

impl PredictorModel {
    fn new(order:u8,direction:u8)->Self {
        let mut domain=b"PAIS-PREDICTOR-STATE-V1|".to_vec(); domain.push(order); domain.push(direction);
        Self{order,direction,counts:HashMap::new(),best:HashMap::new(),commit:sha256(&domain),epochs:0}
    }
    fn mask(&self)->u64 { (1u64 << (self.order as u32*8))-1 }
    fn key(&self,ctx:u64,seen:usize)->u64 {
        let n=seen.min(self.order as usize) as u64;
        ctx | (n<<48) | ((self.order as u64)<<56)
    }
    fn predict(&self,key:u64)->(u8,u32,u32) {
        self.best.get(&key).map(|s|(s.best_symbol,s.best_count,s.total)).unwrap_or((0,0,0))
    }
    fn update(&mut self,key:u64,byte:u8)->bool {
        let count=self.counts.entry((key,byte)).or_insert(0); let novel=*count==0; *count+=1; let nc=*count;
        let state=self.best.entry(key).or_insert(BestState{total:0,best_symbol:0,best_count:0});
        state.total=state.total.saturating_add(1);
        if nc>state.best_count || (nc==state.best_count && byte<state.best_symbol) { state.best_symbol=byte; state.best_count=nc; }
        novel
    }
    fn finish_epoch(&mut self,seq:&[u8],m:&Metrics) {
        let mut b=Vec::new(); b.extend_from_slice(&self.commit); b.extend_from_slice(&sha256(seq));
        b.extend_from_slice(&(self.epochs+1).to_le_bytes()); b.extend_from_slice(&m.predictions.to_le_bytes());
        b.extend_from_slice(&m.top1_correct.to_le_bytes()); b.extend_from_slice(&m.unseen_contexts.to_le_bytes());
        b.extend_from_slice(&m.novel_pairs.to_le_bytes()); b.extend_from_slice(&(self.counts.len() as u64).to_le_bytes());
        self.commit=sha256(&b); self.epochs+=1;
    }
    fn encode(&mut self,seq:&[u8])->(Vec<u8>,Metrics) {
        let mut residual=Vec::with_capacity(seq.len()); let mut ctx=0u64; let mut seen=0usize;
        let mut m=Metrics{predictions:0,top1_correct:0,unseen_contexts:0,novel_pairs:0,confident_blunders:0};
        let mask=self.mask();
        for &byte in seq {
            let key=self.key(ctx,seen); let (pred,best_count,total)=self.predict(key);
            if total==0 { m.unseen_contexts+=1; } else { m.predictions+=1; if pred==byte {m.top1_correct+=1;} else if (best_count as u64)*10 >= (total as u64)*9 {m.confident_blunders+=1;} }
            residual.push(byte^pred); if self.update(key,byte) {m.novel_pairs+=1;}
            ctx=((ctx<<8)|(byte as u64))&mask; seen+=1;
        }
        self.finish_epoch(seq,&m); (residual,m)
    }
    fn decode(&mut self,residual:&[u8])->(Vec<u8>,Metrics) {
        let mut seq=Vec::with_capacity(residual.len()); let mut ctx=0u64; let mut seen=0usize;
        let mut m=Metrics{predictions:0,top1_correct:0,unseen_contexts:0,novel_pairs:0,confident_blunders:0};
        let mask=self.mask();
        for &r in residual {
            let key=self.key(ctx,seen); let (pred,best_count,total)=self.predict(key); let byte=r^pred;
            if total==0 { m.unseen_contexts+=1; } else { m.predictions+=1; if pred==byte {m.top1_correct+=1;} else if (best_count as u64)*10 >= (total as u64)*9 {m.confident_blunders+=1;} }
            if self.update(key,byte) {m.novel_pairs+=1;}
            seq.push(byte); ctx=((ctx<<8)|(byte as u64))&mask; seen+=1;
        }
        self.finish_epoch(&seq,&m); (seq,m)
    }
}

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

fn chain_bytes(chain:&BestChain,source_sha:&[u8;32],native_len:usize)->Vec<u8> {
    let mut out=b"PAISCHAIN1".to_vec(); out.extend_from_slice(source_sha); out.push(chain.a_index); out.push(chain.direction); out.push(chain.order); out.push(chain.payloads.len() as u8); out.extend_from_slice(&(native_len as u64).to_le_bytes());
    for p in &chain.payloads {out.extend_from_slice(&(p.len() as u64).to_le_bytes());out.extend_from_slice(p);} out
}

fn decode_chain(data:&[u8])->AnyResult<Vec<u8>> {
    if data.len()<54||&data[..10]!=b"PAISCHAIN1" {return Err("bad chain header".into());}
    let mut at=10usize; let source_sha:[u8;32]=data[at..at+32].try_into().unwrap(); at+=32;
    let a=data[at] as usize; let direction=data[at+1]; let order=data[at+2]; let epochs=data[at+3] as usize; at+=4;
    let native_len=u64::from_le_bytes(data[at..at+8].try_into().unwrap()) as usize; at+=8;
    let mut model=PredictorModel::new(order,direction); let mut final_seq=Vec::new();
    for _ in 0..epochs { if at+8>data.len(){return Err("short chain length".into());} let n=u64::from_le_bytes(data[at..at+8].try_into().unwrap()) as usize; at+=8; if at+n>data.len(){return Err("short chain payload".into());} let residual=lz_decompress(&data[at..at+n])?; at+=n; let (seq,_)=model.decode(&residual); final_seq=seq; }
    if direction==1 {final_seq.reverse();}
    let native=a_inverse(a,&final_seq,&source_sha); if native.len()!=native_len||sha256(&native)!=source_sha{return Err("chain native restore failed".into());} Ok(native)
}

fn pid8(label:&str)->String {sha_hex(label.as_bytes())[..16].to_string()}

fn checkpoint(dir:&Path,cube:&Cube)->AnyResult<Option<CubeResult>> {
    let meta=dir.join("CUBE-META.hbp"); let receipt=dir.join("CUBE-RESULT.hbp");
    if !meta.exists()||!receipt.exists(){return Ok(None);} let line=fs::read_to_string(&meta).map_err(|e|e.to_string())?; let f=parse_fields(line.trim());
    if f.get("status").map(String::as_str)!=Some("PASS")||f.get("source_sha").map(String::as_str)!=Some(cube.sha.as_str()){return Ok(None);}
    let side=fs::read_to_string(PathBuf::from(format!("{}.sha256",receipt.display()))).map_err(|e|e.to_string())?; let expected=side.split_whitespace().next().unwrap_or(""); let actual=sha_hex(&fs::read(&receipt).map_err(|e|e.to_string())?); if expected!=actual{return Ok(None);}
    Ok(Some(CubeResult{index:cube.index,source_sha:cube.sha.clone(),leaf_sha:f["leaf_sha"].clone(),gain_bytes:f["gain_bytes"].parse().map_err(|_|"bad checkpoint gain")?,accepted:f["accepted"].parse().map_err(|_|"bad checkpoint accepted")?,held:f["held"].parse().map_err(|_|"bad checkpoint held")?,best_payload_bytes:f["best_payload_bytes"].parse().map_err(|_|"bad checkpoint best")?,archive_sha:f["archive_sha"].clone(),chain_sha:f["chain_sha"].clone()}))
}

fn train_cube(cube:&Cube,out_root:&Path,contract_sha:&str,corpus_sha:&str)->AnyResult<CubeResult> {
    let cube_dir=out_root.join(format!("cube-{:02}",cube.index)); fs::create_dir_all(&cube_dir).map_err(|e|e.to_string())?;
    if let Some(r)=checkpoint(&cube_dir,cube)?{println!("CUBE_RESUME|cube={:02}|status=PASS",cube.index);return Ok(r);}
    println!("CUBE_START|cube={:02}|bytes={}|sha256={}",cube.index,cube.data.len(),cube.sha);
    let started=Instant::now(); let source_sha=sha256(&cube.data);
    let archive=lz_compress(&cube.data); if lz_decompress(&archive)?!=cube.data{return Err(format!("cube {} base archive restore",cube.index));}
    let archive_path=cube_dir.join("BASE-CUBE.lz1"); fs::write(&archive_path,&archive).map_err(|e|e.to_string())?; let archive_sha=write_sidecar(&archive_path)?;
    let (group_ok,vertex_hashes,group_detail)=group_gate(&cube.data); if !group_ok{return Err(format!("cube {} R/N/Q group gate failed: {}",cube.index,group_detail));}
    let mut rows=Vec::new(); rows.push(format!("PAISCUBEHDR|schema=PAIS-OMEGA-CUBE-V1|cube={:02}|source_bytes={}|source_sha256={}|contract_sha256={}|corpus_sha256={}|cells=800|higher_floors=HELD|json=0",cube.index,cube.data.len(),cube.sha,contract_sha,corpus_sha));
    rows.push(format!("COLD|cube={:02}|source_bytes={}|behcs1024_input_glyphs={}|base_archive_bytes={}|base_archive_sha256={}|restore=1|json=0",cube.index,cube.data.len(),((cube.data.len()+4)/5)*4,archive.len(),archive_sha));
    rows.push(format!("GROUPGATE|cube={:02}|group=C2^3_CONFIRMED_ON_INPUTS|{}|vertices_sha256={}|all_inputs_distinct=1|status=PASS|json=0",cube.index,group_detail,sha_hex(vertex_hashes.join("|").as_bytes())));
    let mut play_rows=Vec::new();
    for (axis,name,apply) in [("R","R",t_r as fn(&[u8])->Vec<u8>),("N","N",t_n),("Q","Q",t_q)] {
        let moved=apply(&cube.data); let back=apply(&moved); if back!=cube.data{return Err(format!("cube {} axis {} failed",cube.index,axis));}
        for sign in ['+','-'] {play_rows.push(format!("PLAY|cube={:02}|dir={}{}|axis={}|from_sha256={}|to_sha256={}|back_sha256={}|roundtrip=1|same_transform_for_sign=1|json=0",cube.index,sign,name,axis,cube.sha,sha_hex(&moved),sha_hex(&back)));}
    }
    let play_gate_sha=sha_hex((play_rows.join("\n")+"\n").as_bytes()); rows.extend(play_rows);
    let mut gain_total=0u64; let mut accepted=0u64; let mut held=0u64; let mut best:Option<BestChain>=None;
    for a in 0..8 {
        let view=a_apply(a,&cube.data,&source_sha); let restored=a_inverse(a,&view,&source_sha); if restored!=cube.data{return Err(format!("cube {} A inverse {} failed",cube.index,A_NAMES[a]));}
        let view_sha=sha_hex(&view); rows.push(format!("AVIEWGATE|cube={:02}|a={}|view_sha256={}|inverse_sha256={}|roundtrip=1|json=0",cube.index,A_NAMES[a],view_sha,sha_hex(&restored)));
        for direction in 0..2u8 { for order in 1..=5u8 {
            let seq:Vec<u8>=if direction==0{view.clone()}else{view.iter().rev().copied().collect()};
            let mut enc=PredictorModel::new(order,direction); let mut dec=PredictorModel::new(order,direction); let mut lane_payloads=Vec::new(); let mut lane_min=usize::MAX;
            for epoch in 1..=EPOCHS {
                let before=hex(&enc.commit); let (residual,m)=enc.encode(&seq); let payload=lz_compress(&residual); let payload_sha=sha_hex(&payload); let decoded_residual=lz_decompress(&payload)?; let (decoded_seq,dm)=dec.decode(&decoded_residual);
                let state_match=enc.commit==dec.commit&&enc.counts.len()==dec.counts.len()&&enc.best.len()==dec.best.len()&&m.predictions==dm.predictions&&m.unseen_contexts==dm.unseen_contexts;
                if decoded_seq!=seq||!state_match{return Err(format!("cube {} cell restore a={} d={} o={} e={}",cube.index,a,direction,order,epoch));}
                if epoch==EPOCHS&&enc!=dec{return Err(format!("cube {} terminal model mismatch a={} d={} o={}",cube.index,a,direction,order));}
                let cost=payload.len(); let gain=view.len().saturating_sub(cost) as u64; let decision=if gain>0{accepted+=1;gain_total+=gain;"ACCEPT"}else{held+=1;"HOLD"}; lane_min=lane_min.min(cost);
                let actor=pid8(&format!("PAIS|{:02}|{}|{}|{}",cube.index,A_NAMES[a],B_DIRECTIONS[direction as usize],order));
                rows.push(format!("CELL|cube={:02}|a={}|b_direction={}|b_order={}|c_epoch={}|actor_pid={}|input_sha256={}|view_sha256={}|state_before={}|state_after={}|predictions={}|top1_correct={}|unseen_contexts={}|novel_pairs={}|confident_blunders={}|model_pairs={}|payload_bytes={}|payload_sha256={}|gain_bytes={}|decision={}|restore=1|state_match=1|play_gate_sha256={}|conditioning=VARIABLE_ORDER_PREDICTIVE_RESIDUAL_V1|json=0",cube.index,A_NAMES[a],B_DIRECTIONS[direction as usize],order,epoch,actor,cube.sha,view_sha,before,hex(&enc.commit),m.predictions,m.top1_correct,m.unseen_contexts,m.novel_pairs,m.confident_blunders,enc.counts.len(),cost,payload_sha,gain,decision,play_gate_sha));
                lane_payloads.push(payload);
            }
            if best.as_ref().map(|b|lane_min<b.min_payload).unwrap_or(true){best=Some(BestChain{a_index:a as u8,direction,order,payloads:lane_payloads,min_payload:lane_min});}
        }}
    }
    if accepted+held!=800{return Err(format!("cube {} cell count {}",cube.index,accepted+held));}
    let best=best.ok_or("no best chain")?; let chain=chain_bytes(&best,&source_sha,cube.data.len()); if decode_chain(&chain)?!=cube.data{return Err(format!("cube {} best chain restore",cube.index));}
    let chain_path=cube_dir.join("BEST-TRAINED-CHAIN.poc1"); fs::write(&chain_path,&chain).map_err(|e|e.to_string())?; let chain_sha=write_sidecar(&chain_path)?;
    let glyphs=((cube.data.len()+4)/5*4) as u64; rows.push(format!("DENSITY|scope=cube|cube={:02}|accepted_gain_bytes={}|input_glyphs={}|ratio_num={}|ratio_den={}|accepted={}|held={}|meaning=structure_repetition_only|archive_ratio=NOT_CLAIMED|json=0",cube.index,gain_total,glyphs,gain_total,glyphs,accepted,held));
    rows.push(format!("CUBERESTORE|cube={:02}|source_sha256={}|base_archive_sha256={}|best_chain_sha256={}|restore=1|elapsed_ms={}|json=0",cube.index,cube.sha,archive_sha,chain_sha,started.elapsed().as_millis()));
    let leaf_sha=sha_hex((rows.join("\n")+"\n").as_bytes()); rows.push(format!("OMEGALEAF|cube={:02}|source_sha256={}|cells=800|plays=6|leaf_sha256={}|restore=1|json=0",cube.index,cube.sha,leaf_sha));
    rows.push(format!("PAISCUBEFTR|cube={:02}|cells=800|accepted={}|held={}|gain_bytes={}|best_payload_bytes={}|restore=1|status=PASS|json=0",cube.index,accepted,held,gain_total,best.min_payload));
    let receipt=cube_dir.join("CUBE-RESULT.hbp"); write_lf(&receipt,&(rows.join("\n")+"\n"))?; write_sidecar(&receipt)?;
    let meta=cube_dir.join("CUBE-META.hbp"); write_lf(&meta,&format!("CUBEMETA|cube={:02}|source_sha={}|leaf_sha={}|gain_bytes={}|accepted={}|held={}|best_payload_bytes={}|archive_sha={}|chain_sha={}|status=PASS|json=0\n",cube.index,cube.sha,leaf_sha,gain_total,accepted,held,best.min_payload,archive_sha,chain_sha))?; write_sidecar(&meta)?;
    println!("CUBE_OK|cube={:02}|cells=800|accepted={}|held={}|gain={}|leaf={}",cube.index,accepted,held,gain_total,leaf_sha);
    Ok(CubeResult{index:cube.index,source_sha:cube.sha.clone(),leaf_sha,gain_bytes:gain_total,accepted,held,best_payload_bytes:best.min_payload,archive_sha,chain_sha})
}

fn hbi_for(hbp:&str)->String {
    let mut out=String::new();
    for (i,line) in hbp.lines().enumerate(){out.push_str(&format!("HBI|row={}|sha256={}|hex={}|json=0\n",i+1,sha_hex(line.as_bytes()),hex(line.as_bytes())));} out
}

fn run_train(manifest:&Path,contract:&Path,output:&Path,workers:usize)->AnyResult<()> {
    fs::create_dir_all(output).map_err(|e|e.to_string())?; let contract_bytes=fs::read(contract).map_err(|e|e.to_string())?; let contract_sha=sha_hex(&contract_bytes); write_sidecar(contract)?;
    let (patents,corpus,corpus_sha,manifest_sha)=load_patents(manifest)?; let cubes=partition_cubes(&corpus); let cube_root=output.join("cubes"); fs::create_dir_all(&cube_root).map_err(|e|e.to_string())?;
    let mut intake=Vec::new(); intake.push(format!("PAISINTAKEHDR|schema=PAIS-OMEGA-INTAKE-V1|manifest_sha256={}|contract_sha256={}|sources=11|cubes=27|corpus_bytes={}|corpus_sha256={}|json=0",manifest_sha,contract_sha,corpus.len(),corpus_sha));
    for (ord,p) in patents.iter().enumerate(){intake.push(format!("SOURCE|ord={}|patent={}|bytes={}|sha256={}|magic=25504446|offset={}|file={}|json=0",ord+1,p.id,p.bytes,p.sha,p.offset,p.file));}
    for c in &cubes {let path=cube_root.join(format!("LX-{:03}.bin",c.index));fs::write(&path,&c.data).map_err(|e|e.to_string())?;intake.push(format!("CUBEINTAKE|cube={:02}|start={}|end_exclusive={}|bytes={}|sha256={}|file=cubes/LX-{:03}.bin|json=0",c.index,c.start,c.end,c.data.len(),c.sha,c.index));}
    let restored:Vec<u8>=cubes.iter().flat_map(|c|c.data.iter().copied()).collect(); if restored!=corpus{return Err("cube concatenation restore failed".into());}
    for p in &patents {if sha_hex(&restored[p.offset..p.offset+p.bytes])!=p.sha{return Err(format!("final source restore failed {}",p.id));}}
    intake.push(format!("INTAKEGATE|sources=11|cubes=27|coverage=ALL_BYTES|gaps=0|overlaps=0|corpus_sha256={}|restore_11_of_11=1|status=PASS|json=0",corpus_sha));
    let intake_path=output.join("PAIS-INTAKE.hbp");write_lf(&intake_path,&(intake.join("\n")+"\n"))?;write_sidecar(&intake_path)?;
    let zero=vec![0u8;4096];let (zero_pass,_,_)=group_gate(&zero);if zero_pass{return Err("zero distinctness negative control failed".into());}
    let mut corrupt=corpus.clone();if let Some(first)=corrupt.first_mut(){*first^=1;}let corruption_diff=sha_hex(&corrupt)!=corpus_sha;
    let mut reversed_sources=Vec::new();for p in patents.iter().rev(){reversed_sources.extend_from_slice(&corpus[p.offset..p.offset+p.bytes]);}let order_diff=sha_hex(&reversed_sources)!=corpus_sha;
    if !corruption_diff||!order_diff{return Err("negative control failed".into());}
    let queue=Arc::new(Mutex::new(VecDeque::from(cubes.clone())));let (tx,rx)=mpsc::channel();let worker_count=workers.max(1).min(CUBE_COUNT);let out_arc=Arc::new(output.to_path_buf());let cs=Arc::new(contract_sha.clone());let corpus_s=Arc::new(corpus_sha.clone());
    let mut handles=Vec::new();for _ in 0..worker_count{let q=Arc::clone(&queue);let tx=tx.clone();let out=Arc::clone(&out_arc);let cs=Arc::clone(&cs);let cps=Arc::clone(&corpus_s);handles.push(thread::spawn(move||loop{let cube={q.lock().unwrap().pop_front()};match cube{Some(c)=>{let r=train_cube(&c,&out,&cs,&cps);let _=tx.send(r);},None=>break}}));}drop(tx);
    let mut results=Vec::new();let mut errors=Vec::new();for r in rx{match r{Ok(x)=>results.push(x),Err(e)=>errors.push(e)}}for h in handles{let _=h.join();}if !errors.is_empty(){return Err(errors.join("; "));}if results.len()!=CUBE_COUNT{return Err(format!("expected 27 cube results got {}",results.len()));}results.sort_by_key(|r|r.index);
    let mut hbp=Vec::new();hbp.push(format!("PAISFLOORHDR|schema=PAIS-OMEGA-FLOOR1-V1|authority=OPERATOR_SUPERSEDING_2026-07-15|mode=SHADOW_MEASURED|floor=1|cube_count=27|ring_a=8|ring_b=10|ring_c=10|cells_per_cube=800|cells_total=21600|directions=+R,-R,+N,-N,+Q,-Q|higher_floors=HELD_OPERATOR_SCOPE|contract_sha256={}|manifest_sha256={}|corpus_sha256={}|json=0",contract_sha,manifest_sha,corpus_sha));
    hbp.extend(intake.iter().skip(1).cloned());hbp.push(format!("CONTROL|name=ALL_ZERO_DISTINCTNESS|expected=FAIL_DISTINCT|observed={}|status=PASS|json=0",if zero_pass{"PASS_DISTINCT"}else{"FAIL_DISTINCT"}));hbp.push("CONTROL|name=ONE_BYTE_CORRUPTION|expected=SHA_DIFFERENT|observed=SHA_DIFFERENT|status=PASS|json=0".into());hbp.push("CONTROL|name=SOURCE_ORDER_REVERSAL|expected=SHA_DIFFERENT|observed=SHA_DIFFERENT|status=PASS|json=0".into());
    let mut total_gain=0u64;let mut total_accept=0u64;let mut total_hold=0u64;let mut leaves=Vec::new();for r in &results{let receipt=output.join(format!("cube-{:02}/CUBE-RESULT.hbp",r.index));let text=fs::read_to_string(&receipt).map_err(|e|e.to_string())?;hbp.extend(text.lines().map(str::to_string));total_gain+=r.gain_bytes;total_accept+=r.accepted;total_hold+=r.held;leaves.push(format!("OMEGALEAFREF|cube={:02}|source_sha256={}|leaf_sha256={}|archive_sha256={}|chain_sha256={}|json=0",r.index,r.source_sha,r.leaf_sha,r.archive_sha,r.chain_sha));}
    let anchor=format!("OMEGAANCHOR|schema=PAIS-OMEGA-FLOOR1-V1|contract_sha256={}|corpus_sha256={}|cube_count=27|epoch=FLOOR1_ONLY|json=0",contract_sha,corpus_sha);let omega=sha_hex((anchor.clone()+"\n"+&leaves.join("\n")+"\n").as_bytes());hbp.push(anchor);hbp.extend(leaves);hbp.push(format!("OMEGACENTER|method=sha256_over_anchor_plus_27_ordered_leaves_lf|omega_sha256={}|leaf_count=27|all_restore=1|higher_floors=HELD|json=0",omega));let glyphs=((corpus.len()+4)/5*4) as u64;hbp.push(format!("DENSITY|scope=cohort|accepted_gain_bytes={}|input_glyphs={}|ratio_num={}|ratio_den={}|accepted={}|held={}|meaning=structure_repetition_only|archive_ratio=NOT_CLAIMED|json=0",total_gain,glyphs,total_gain,glyphs,total_accept,total_hold));hbp.push(format!("PAISFLOORFTR|cells=21600|direction_routes=162|accepted={}|held={}|restore_cubes=27_of_27|restore_pdfs=11_of_11|omega={}|higher_floors=HELD|compression_record=NOT_CLAIMED|physics_validation=NOT_CLAIMED|status=PASS|json=0",total_accept,total_hold,omega));
    let floor_text=hbp.join("\n")+"\n";let floor=output.join("PAIS-OMEGA-FLOOR1-RESULT.hbp");write_lf(&floor,&floor_text)?;let floor_sha=write_sidecar(&floor)?;let hbi=output.join("PAIS-OMEGA-FLOOR1-RESULT.hbi");write_lf(&hbi,&hbi_for(&floor_text))?;let hbi_sha=write_sidecar(&hbi)?;let sums=format!("{}  PAIS-OMEGA-FLOOR1-RESULT.hbp\n{}  PAIS-OMEGA-FLOOR1-RESULT.hbi\n{}  PAIS-INTAKE.hbp\n",floor_sha,hbi_sha,sha_hex(&fs::read(&intake_path).map_err(|e|e.to_string())?));let sums_path=output.join("SHA256SUMS");write_lf(&sums_path,&sums)?;write_sidecar(&sums_path)?;
    println!("PAIS_FLOOR_PASS|cubes=27|cells=21600|accepted={}|held={}|gain_bytes={}|omega={}|result_sha256={}|higher_floors=HELD",total_accept,total_hold,total_gain,omega,floor_sha);Ok(())
}

fn run_shard(manifest:&Path,contract:&Path,output:&Path,cube_index:usize)->AnyResult<()> {
    if !(1..=CUBE_COUNT).contains(&cube_index) {
        return Err(format!("cube must be 1..={}, got {}", CUBE_COUNT, cube_index));
    }
    fs::create_dir_all(output).map_err(|e|e.to_string())?;
    let contract_bytes=fs::read(contract).map_err(|e|e.to_string())?;
    let contract_sha=sha_hex(&contract_bytes);
    let (_patents,corpus,corpus_sha,_manifest_sha)=load_patents(manifest)?;
    let cubes=partition_cubes(&corpus);
    let result=train_cube(&cubes[cube_index-1],output,&contract_sha,&corpus_sha)?;
    println!("GITRAM_SHARD_PASS|cube={:02}|cells=800|accepted={}|held={}|gain_bytes={}|leaf_sha256={}|status=PASS",
        result.index,result.accepted,result.held,result.gain_bytes,result.leaf_sha);
    Ok(())
}
fn flag(args:&[String],name:&str)->AnyResult<String>{let i=args.iter().position(|x|x==name).ok_or_else(||format!("missing {}",name))?;args.get(i+1).cloned().ok_or_else(||format!("missing value for {}",name))}

fn main()->Result<(),String>{
    let args:Vec<String>=env::args().collect();if args.len()<2{return Err("usage: train --manifest PATH --contract PATH --output PATH [--workers N] | shard --manifest PATH --contract PATH --output PATH --cube N | play --chain PATH --output PATH".into());}
    match args[1].as_str(){
        "train"=>{let manifest=PathBuf::from(flag(&args,"--manifest")?);let contract=PathBuf::from(flag(&args,"--contract")?);let output=PathBuf::from(flag(&args,"--output")?);let workers=flag(&args,"--workers").ok().and_then(|x|x.parse().ok()).unwrap_or(8);run_train(&manifest,&contract,&output,workers)},
        "shard"=>{let manifest=PathBuf::from(flag(&args,"--manifest")?);let contract=PathBuf::from(flag(&args,"--contract")?);let output=PathBuf::from(flag(&args,"--output")?);let cube=flag(&args,"--cube")?.parse().map_err(|_|"bad --cube")?;run_shard(&manifest,&contract,&output,cube)},
        "play"=>{let chain=PathBuf::from(flag(&args,"--chain")?);let output=PathBuf::from(flag(&args,"--output")?);let raw=decode_chain(&fs::read(&chain).map_err(|e|e.to_string())?)?;fs::write(&output,&raw).map_err(|e|e.to_string())?;println!("PLAY_OK|bytes={}|sha256={}|output={}",raw.len(),sha_hex(&raw),output.display());Ok(())},
        _=>Err("unknown command".into()),
    }
}
