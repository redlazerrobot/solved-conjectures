from collections import Counter
def caterpillar(signature):
    k=len(signature)
    E=[(i,i+1) for i in range(k-1)]
    v=k
    for i,w in enumerate(signature):
        E.extend((i,j) for j in range(v,v+w-1))
        v+=w-1
    return E
def get_h(n,E):
    out=Counter()
    for m in range(1,1<<n):
        size=m.bit_count()
        ie=b=0
        for i,j in E:
            a=(m>>i)&1;c=(m>>j)&1
            ie+=a*c;b+=a^c
        if ie+1==size:out[size,b]+=1
    return out
def cut_data(n,E,mid):
    u=Counter();s=Counter()
    for mask in range(1<<len(E)):
        d=list(range(n))
        def find(i):
            while d[i]!=i:i=d[i]
            return i
        for j,(a,b) in enumerate(E):
            if not mask>>j&1:d[find(a)]=find(b)
        profile=tuple(sorted(Counter(find(i) for i in range(n)).values()))
        u[profile]+=1
        if mask>>mid&1:s[profile]+=1
    return u,s
if __name__=='__main__':
    X=(2,2,1,2,1,3,3);Y=(3,1,2,1,2,3,2)
    A,B=map(caterpillar,(X,Y))
    hx,hy=get_h(14,A),get_h(14,B)
    assert hx==hy
    print('connected profiles',len(hx),'connected sets',sum(hx.values()))
    u,s=cut_data(14,A,3);v,t=cut_data(14,B,3)
    assert (s[(3,3,4,4)], t[(3,3,4,4)]) == (1,0)
    assert (u[(1,3,10)], v[(1,3,10)]) == (7,8)
    for l,r in [(s,t),(u,v)]:
        print([(p,l[p],r[p]) for p in sorted(set(l)|set(r),key=lambda x:(len(x),x)) if l[p]!=r[p]][:8])
