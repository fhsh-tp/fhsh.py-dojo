import json, os, sys
HERE=os.path.dirname(os.path.abspath(__file__))
# Re-measures only the marginal entries, on all 10 pool blocks, to show the
# cliff position does not move with the block the judge happens to serve.
data = json.load(open(os.environ.get('CLIFF_INPUTS', os.path.join(HERE,'inputs.json')), encoding='utf-8'))
OP=10_000_000
def parse(inp):
    tok=inp.split(); n=int(tok[0]); return n,[int(v) for v in tok[1:1+n]],[int(v) for v in tok[1+n:1+2*n]]
def brute_loop(inp):
    n,starts,durations=parse(inp)
    order=sorted(range(n),key=lambda i:(starts[i],i))
    s=[starts[i] for i in order]; end=[starts[i]+durations[i] for i in order]
    room=[0]*n; out=[0]*n
    for i in range(n):
        occupied=set()
        for j in range(i):
            if end[j]>s[i]:
                occupied.add(room[j])
        r=1
        while r in occupied:
            r+=1
        room[i]=r; out[order[i]]=r
    return max(room) if n else 0,out
def brute_comp(inp):
    n,starts,durations=parse(inp)
    order=sorted(range(n),key=lambda i:(starts[i],i))
    s=[starts[i] for i in order]; end=[starts[i]+durations[i] for i in order]
    room=[0]*n; out=[0]*n
    for i in range(n):
        occupied={room[j] for j in range(i) if end[j]>s[i]}
        r=1
        while r in occupied:
            r+=1
        room[i]=r; out[order[i]]=r
    return max(room) if n else 0,out
def cnt(fn,a):
    b=[0]
    def tr(f,e,x):
        b[0]+=1; return tr
    old_trace = sys.gettrace()
    sys.settrace(tr); sys._getframe().f_trace=tr
    try: r=fn(a)
    finally: sys.settrace(old_trace)
    return b[0],r
# marginal entries: index 13 (N=3500, loop) and 15,16 (N=4000/4500, comp)
print(f'{"blk":>3} {"e15 loop":>12} {"e16 comp":>12} {"e17 comp":>12} {"e20 rooms":>10}')
worst={'e15loop':[], 'e16comp':[], 'e17comp':[], 'rooms':[]}
for b,blk in enumerate(data['blocks']):
    l15,_=cnt(brute_loop,blk[14])
    c16,_=cnt(brute_comp,blk[15])
    c17,_=cnt(brute_comp,blk[16])
    k,_=brute_loop(blk[19])
    worst['e15loop'].append(l15); worst['e16comp'].append(c16); worst['e17comp'].append(c17); worst['rooms'].append(k)
    print(f'{b:>3} {l15:>12,} {c16:>12,} {c17:>12,} {k:>10}')
print('\nentry15 loop  min/max:', f"{min(worst['e15loop']):,}", f"{max(worst['e15loop']):,}", '-> all over limit:', min(worst['e15loop'])>OP)
print('entry16 comp  min/max:', f"{min(worst['e16comp']):,}", f"{max(worst['e16comp']):,}", '-> all under limit:', max(worst['e16comp'])<=OP)
print('entry17 comp  min/max:', f"{min(worst['e17comp']):,}", f"{max(worst['e17comp']):,}", '-> all over limit:', min(worst['e17comp'])>OP)
print('entry20 rooms min/max:', min(worst['rooms']), max(worst['rooms']))
with open(os.environ.get('CLIFF_CROSSBLOCK_OUT', os.path.join(HERE,'crossblock.json')), 'w') as fh:
    json.dump(worst, fh)
