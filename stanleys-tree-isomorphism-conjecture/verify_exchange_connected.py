"""Count by original connected vertex sets; root is 0 of either packet."""
from collections import Counter
from itertools import combinations
from verify_complementary_fringe import halves, edges

def census(n,E,root=None):
    out=Counter()
    for mask in range(1,1<<n):
        if root is not None and not (mask>>root)&1: continue
        count=mask.bit_count()
        ie=boundary=0
        for u,v in E:
            a=(mask>>u)&1
            b=(mask>>v)&1
            ie+=a*b; boundary+=a^b
        if ie+1==count:
            out[count,boundary]+=1
    return out

def attach(n,E,u,t):
    exp=edges(t,0)
    convert=lambda i: u if i==0 else n+i-1
    return n+len(exp),E+[(convert(i),convert(j)) for i,j in exp]

def join_two(n,E,u,v,B,C):
    n1,E1=attach(n,E,u,B)
    return attach(n1,E1,v,C)

def diff(a,b):
    a=a.copy()
    a.subtract(b)
    return a

def product_over_x(a,b):
    p=Counter()
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            p[i+k-1,j+l]+=x*y
    return p

if __name__=='__main__':
    total=nonzero=0
    B=((),())
    C=(((),),)
    for n in range(2,7):
        # use each rooted representative once; no claim of unrooted deduplication
        for t in halves(n):
            E=edges(t,0)
            root_data=[census(n,E,i) for i in range(n)]
            packet_diff=diff(census(3,edges(B,0),0),census(3,edges(C,0),0))
            for u,v in combinations(range(n),2):
                first=census(*join_two(n,E,u,v,B,C))
                second=census(*join_two(n,E,u,v,C,B))
                observed=diff(first,second)
                expected=product_over_x(packet_diff,diff(root_data[u],root_data[v]))
                assert observed==expected
                total+=1
                nonzero+=any(observed.values())
    print(total,'compared;',nonzero,'nonzero')
