import os
from json import dumps,load
from urllib.request import*
U=os.environ["MAKEFUN_ENV_URL"]
V={"P":100,"N":320,"B":330,"R":500,"Q":900,"K":9999}
KN=[(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
D8=[(a,b)for a in(-1,0,1)for b in(-1,0,1)if a|b]
N=[0]
def post(p,b):
 return load(urlopen(Request(U+p,data=dumps(b).encode(),headers={"content-type":"application/json"})))
def parse(f):
 z=f.split();b=["."]*64;i=0
 for c in z[0].replace("/",""):
  if c.isdigit():i+=int(c)
  else:b[i]=c;i+=1
 ca=sum(1<<i for i,ch in enumerate("KQkq")if ch in z[2])
 return b,z[1]=="w",ca,-1
def atk(b,s,by):
 x,y=s%8,s//8;pr=y+(1 if by else-1)
 for d in(-1,1):
  if 0<=pr<8 and 0<=x+d<8 and b[pr*8+x+d]==("P"if by else"p"):return 1
 for ds,ch in((KN,"N"),(D8,"K")):
  for dx,dy in ds:
   nx,ny=x+dx,y+dy
   if 0<=nx<8 and 0<=ny<8 and b[ny*8+nx]==(ch if by else ch.lower()):return 1
 for dx,dy in D8:
  nx,ny=x,y
  while 1:
   nx+=dx;ny+=dy
   if not(0<=nx<8 and 0<=ny<8):break
   c=b[ny*8+nx]
   if c!=".":
    if c.isupper()==by and(c.upper()=="Q"or c.upper()==("B"if dx and dy else"R")):return 1
    break
 return 0
def gen(b,w,ca,ep):
 ms=[];A=ms.append
 for s in range(64):
  c=b[s]
  if c=="."or c.isupper()!=w:continue
  x,y=s%8,s//8;u=c.upper()
  if u=="P":
   d=-8 if w else 8;t=s+d;pr=t<8 or t>55
   if b[t]==".":
    if pr:A((s,t,"q"))
    else:
     A((s,t,""))
     if y==(6 if w else 1)and b[t+d]==".":A((s,t+d,""))
   for dx in(-1,1):
    if 0<=x+dx<8:
     t=s+d+dx;v=b[t]
     if v!="."and v.isupper()!=w:A((s,t,"q"if pr else""))
  else:
   for dx,dy in(KN if u=="N"else D8):
    if(u=="B"and dx*dy==0)or(u=="R"and dx*dy!=0):continue
    nx,ny=x,y
    while 1:
     nx+=dx;ny+=dy
     if not(0<=nx<8 and 0<=ny<8):break
     t=ny*8+nx;v=b[t]
     if v=="."or v.isupper()!=w:A((s,t,""))
     if v!="."or u in"NK":break
   if u=="K":
    e=not w;kb=1 if w else 4
    for sg,bit in((1,kb),(-1,kb*2)):
     if ca&bit and b[s+(3 if sg>0 else-4)]==("R"if w else"r")and all(b[s+sg*i]=="."for i in((1,2)if sg>0 else(1,2,3)))and all(not atk(b,s+sg*i,e)for i in(0,1,2)):A((s,s+2*sg,"c"))
 return ms
def mk(b,w,ca,ep,m):
 f,t,p=m;b=b[:];c=b[f];b[f]="."
 b[t]=(p.upper()if w else p)if p not in("","c")else c
 if p=="c":
  r="R"if w else"r"
  if t>f:b[t-1]=r;b[t+1]="."
  else:b[t+1]=r;b[t-2]="."
 if c=="K":ca&=12
 if c=="k":ca&=3
 for s2 in(f,t):ca&=~{63:1,56:2,7:4,0:8}.get(s2,0)
 return b,not w,ca,-1
def legal(b,w,ca,ep):
 K="K"if w else"k"
 return[m for m in gen(b,w,ca,ep)if not atk((n:=mk(b,w,ca,ep,m)[0]),n.index(K),not w)]
def ev(b,w):
 s=0
 for i,c in enumerate(b):
  if c==".":continue
  u=c.upper();v=V[u];j=i if c.isupper()else i^56;ct=int(7-abs(3.5-i%8)-abs(3.5-i//8))
  if u=="P":v+=(6-j//8)**2*3+ct*2
  elif u=="N":v+=ct*9-12
  elif u=="K":v-=ct*6
  else:v+=ct*4
  s+=v if c.isupper()else-v
 return s if w else-s
def key(b,m):
 v=b[m[1]]
 return(V[v.upper()]if v!="."else 0)*10-V[b[m[0]].upper()]//100+800*(m[2]=="q")
def srt(b,ms):ms.sort(key=lambda m:-key(b,m))
def qs(b,w,ca,ep,a,be):
 N[0]+=1;st=ev(b,w)
 if st>a:a=st
 if a>=be or N[0]>12000:return a
 ms=[m for m in legal(b,w,ca,ep)if b[m[1]]!="."or m[2]=="q"]
 srt(b,ms)
 for m in ms:
  sc=-qs(*mk(b,w,ca,ep,m),-be,-a)
  if sc>a:a=sc
  if a>=be:break
 return a
def sr(b,w,ca,ep,d,a,be,ply):
 N[0]+=1
 if d==0:return qs(b,w,ca,ep,a,be)
 ms=legal(b,w,ca,ep)
 if not ms:
  K="K"if w else"k"
  return-100000+ply if atk(b,b.index(K),not w)else 0
 srt(b,ms)
 for m in ms:
  sc=-sr(*mk(b,w,ca,ep,m),d-1,-be,-a,ply+1)
  if sc>a:a=sc
  if a>=be or N[0]>12000:break
 return a
def uci(m):
 f,t,p=m;return chr(97+f%8)+str(8-f//8)+chr(97+t%8)+str(8-t//8)+p*(p=="q")
def choose(fen):
 b,w,ca,ep=parse(fen);ms=legal(b,w,ca,ep);N[0]=0;best=ms[0]
 srt(b,ms)
 for d in range(1,5):
  cb,cs=best,-10**9
  for m in ms:
   sc=-sr(*mk(b,w,ca,ep,m),d-1,-10**9,10**9,1)
   if sc>cs:cs,cb=sc,m
  if N[0]<=12000:best=cb
  else:break
 return uci(best)
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=post("/move",{"game":g["game"],"move":choose(g["fen"])})
