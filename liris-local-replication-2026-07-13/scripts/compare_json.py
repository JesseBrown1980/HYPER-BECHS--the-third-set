#!/usr/bin/env python3
import json, sys
SKIP = ("_s", "_ns", "_gain")   # wall-clock/timing fields, never expected to match
def diffs(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if isinstance(k, str) and k.endswith(SKIP): continue
            if k not in a: yield (path+"/"+k, "<absent-local>", b[k])
            elif k not in b: yield (path+"/"+k, a[k], "<absent-ref>")
            else: yield from diffs(a[k], b[k], path+"/"+k)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): yield (path+"/len", len(a), len(b))
        for i,(x,y) in enumerate(zip(a,b)): yield from diffs(x,y,f"{path}[{i}]")
    elif a != b: yield (path, a, b)
d = list(diffs(json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))))
for p,x,y in d: print(f"DIFF {p}: local={x} ref={y}")
print("MATCH" if not d else f"MISMATCH ({len(d)} fields)")
sys.exit(1 if d else 0)
