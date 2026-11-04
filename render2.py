import sys,json,math,subprocess,numpy as np,cv2,os
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import script,clips as CL
FPS=24; OW,OH=1920,1080
tl=json.load(open('timeline.json')); total=tl['total']; NF=int(math.ceil(total*FPS))
voice=np.load('voice.npy'); SR=44100
GOLD=(184,150,82); CREAM=(246,239,221)
FP='/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf'
def font(sz,w=400):
    f=ImageFont.truetype(FP,sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def wrap(txt,f,maxw,d):
    words=txt.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines
_d=ImageDraw.Draw(Image.new('RGB',(10,10)))
def textlayer(lines,f,color,align='center',lh=1.28,shadow=True,pad=30):
    wmax=int(max(_d.textlength(l,font=f) for l in lines))+pad*2
    hl=int(f.size*lh); h=hl*len(lines)+pad*2
    im=Image.new('RGBA',(wmax,h),(0,0,0,0)); sh=Image.new('RGBA',(wmax,h),(0,0,0,0))
    sd=ImageDraw.Draw(sh); d=ImageDraw.Draw(im)
    for i,l in enumerate(lines):
        w=_d.textlength(l,font=f); x=(wmax-w)/2 if align=='center' else pad; y=pad+i*hl
        if shadow: sd.text((x+2,y+3),l,font=f,fill=(0,0,0,235))
        d.text((x,y),l,font=f,fill=color+(255,))
    if shadow:
        sh=sh.filter(ImageFilter.GaussianBlur(6)); im=Image.alpha_composite(sh,im)
    return np.array(im)
def comp(frame,layer,x,y,a):
    if a<=0.003: return
    h,w=layer.shape[:2]
    x0,y0=max(0,x),max(0,y); x1,y1=min(OW,x+w),min(OH,y+h)
    if x1<=x0 or y1<=y0: return
    L=layer[y0-y:y1-y,x0-x:x1-x]
    al=(L[...,3:4].astype(np.float32)/255.0)*a
    roi=frame[y0:y1,x0:x1].astype(np.float32); col=L[...,2::-1].astype(np.float32)
    frame[y0:y1,x0:x1]=(roi*(1-al)+col*al).astype(np.uint8)
def fade(t,a,b,fi=0.4,fo=0.4):
    if t<a or t>b: return 0.0
    return min(1.0,(t-a)/fi,(b-t)/fo)
BL=tl['blocks']; NB=len(BL)
# ---- slots
slots=[]  # (start,end,path)
for bi,b in enumerate(BL):
    s=0.0 if bi==0 else b['start']; e=total if bi==NB-1 else b['end']
    cl=CL.CLIPS[bi]; n=len(cl); d=(e-s)/n
    for k,c in enumerate(cl): slots.append((s+k*d,s+(k+1)*d,c))
XF=0.6
def slotfile(i): return f'slots/{i:03d}.mp4'
def prep(i):
    s,e,c=slots[i]; dur=e-s+XF+0.2
    cd=float(dict(l.split() for l in open('clips/durs.txt'))[c]); avail=cd-0.6
    sp=min(1.0,avail/dur)
    cmd=['ffmpeg','-y','-v','error','-ss','0.4','-i',f'clips/{c}.mp4','-t',f'{dur*sp:.3f}','-vf',
         f'setpts=PTS/{sp:.5f},fps={FPS},scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080','-an',
         '-c:v','libx264','-preset','ultrafast','-crf','17','-pix_fmt','yuv420p',slotfile(i)]
    subprocess.run(cmd,check=True)
caps={}
def getcap(i):
    if i not in caps:
        if len(caps)>6:
            for k in list(caps)[:3]:
                caps.pop(k).release(); pos.pop(k,None)
        caps[i]=cv2.VideoCapture(slotfile(i))
    return caps[i]
pos={}
def readslot(i,t):
    s=slots[i][0]; fi=max(0,int(round((t-s)*FPS))); c=getcap(i)
    if pos.get(i)!=fi:
        c.set(cv2.CAP_PROP_POS_FRAMES,fi)
    ok,fr=c.read()
    if not ok:
        n=int(c.get(cv2.CAP_PROP_FRAME_COUNT)); c.set(cv2.CAP_PROP_POS_FRAMES,max(0,n-1)); ok,fr=c.read(); pos[i]=None
    else: pos[i]=fi+1
    return fr
starts=np.array([s[0] for s in slots])
def base(t):
    i=int(np.searchsorted(starts,t,side='right'))-1; i=max(0,i)
    fr=readslot(i,t).astype(np.float32)
    if i>0 and t-slots[i][0]<XF:
        a=(t-slots[i][0])/XF; a=a*a*(3-2*a)
        fr=readslot(i-1,t).astype(np.float32)*(1-a)+fr*a
    return fr
# ---- overlays
overlays=[]
cf=font(46,600); pf=font(32,500); bf=font(104,700); tf=font(96,700); sf=font(40,500)
def dim(lay,k=150):
    h,w=lay.shape[:2]; im=np.zeros((h+300,w+300,4),np.uint8); a=np.zeros((h+300,w+300),np.uint8); a[110:h+190,110:w+190]=k
    a=cv2.GaussianBlur(a,(0,0),40); im[...,3]=a; return im
def cx(layer): return (OW-layer.shape[1])//2
for bi,b in enumerate(script.BLOCKS):
    s,e=BL[bi]['start'],BL[bi]['end']
    if bi==NB-1: continue
    if 'chapter' in b:
        lay=textlayer([b['chapter']],cf,(232,196,120),'left',pad=14); overlays.append((dim(lay,170),96-110,86-110,s+0.5,s+7.5)); overlays.append((lay,96,86,s+0.5,s+7.5))
    if 'plaque' in b:
        lay=textlayer([b['plaque']],pf,CREAM,'left',shadow=False,pad=18)
        h,w=lay.shape[:2]; plate=np.zeros((h,w,4),np.uint8); plate[...]=(12,10,9,185)
        plate[:3,:]=(184,150,82,255); plate[-3:,:]=(184,150,82,255)
        m=lay[...,3:4].astype(np.float32)/255.0; rgb=plate[...,:3].astype(np.float32)*(1-m)+lay[...,:3].astype(np.float32)*m
        plate[...,:3]=rgb.astype(np.uint8); plate[...,3]=np.maximum(plate[...,3],lay[...,3])
        overlays.append((plate,96,86+60+36 if 'chapter' in b else 96,s+1.3,s+8.3))
    if 'big' in b:
        lines=wrap(b['big'],bf,1500,_d); lay=textlayer(lines,bf,CREAM)
        t0=s+7.0; overlays.append((dim(lay,170),cx(lay)-150,300-150,t0,t0+5.0)); overlays.append((lay,cx(lay),300,t0,t0+5.0))
tl1=textlayer(wrap(script.TITLE.split(' | ')[0],tf,1700,_d),tf,CREAM); overlays.append((dim(tl1,185),cx(tl1)-150,60-150,0.0,6.5)); overlays.append((tl1,cx(tl1),60,0.0,6.5))
tl2=textlayer([script.TITLE.split(' | ')[1]],font(48,600),(232,196,120)); overlays.append((tl2,cx(tl2),60+tl1.shape[0]-6,0.3,6.5))
ob=textlayer(['ИСТОЧНИК'],font(150,700),(232,196,120)); overlays.append((dim(ob,185),cx(ob)-150,380-150,BL[-1]['start']+1.0,total+1)); overlays.append((ob,cx(ob),380,BL[-1]['start']+1.0,total+1))
ob2=textlayer(['Кто мы. Откуда. Зачем.'],font(46,400),CREAM); overlays.append((ob2,cx(ob2),580,BL[-1]['start']+2.0,total+1))
subs=[]
for c in tl['chunks']:
    lines=wrap(c['text'],sf,1440,_d); lay=textlayer(lines,sf,CREAM,lh=1.3); subs.append((lay,cx(lay),c['start'],c['end']))
subs_starts=np.array([s[2] for s in subs])
# logo (semi-transparent, bottom-left)
_av=cv2.imread('avatar.jpg'); LS=130
av=cv2.resize(_av,(LS,LS),interpolation=cv2.INTER_AREA); avm=np.zeros((LS,LS),np.uint8); cv2.circle(avm,(LS//2,LS//2),LS//2-2,255,-1,cv2.LINE_AA)
LX,LY=44,OH-LS-48
def put_logo(fr,amp,alpha=0.55):
    cx0,cy0=LX+LS//2,LY+LS//2
    ov=fr.copy()
    for k,rr in enumerate((LS//2+8,LS//2+8+int(8+26*amp),LS//2+8+int(22+52*amp))):
        col=(int(82*(1-0.25*k)+60),int(150*(1-0.25*k)+60),int(184*(1-0.25*k)+40))
        cv2.circle(ov,(cx0,cy0),rr,col,3 if k<2 else 2,cv2.LINE_AA)
    roi=ov[LY:LY+LS,LX:LX+LS]; al=(avm.astype(np.float32)/255)[...,None]
    ov[LY:LY+LS,LX:LX+LS]=(roi*(1-al)+av*al).astype(np.uint8)
    return cv2.addWeighted(ov,alpha,fr,1-alpha,0)
def amp_at(t):
    i=int(t*SR); seg=voice[max(0,i-1500):i+1500]
    return float(min(1.0,np.sqrt(np.mean(seg**2))/0.18)) if len(seg) else 0.0
foot=textlayer(['ИСТОЧНИК · Людмила Вагнер'],font(24,500),CREAM,'left',shadow=True,pad=8); foot[...,3]=(foot[...,3]*0.6).astype(np.uint8)
yy,xx=np.mgrid[0:OH,0:OW].astype(np.float32)
grad=(1-0.50*np.clip((yy-560)/420,0,1)**1.2)*(1-0.30*np.clip((260-yy)/260,0,1))
grad=(grad*0.93)[...,None].astype(np.float32)
def frame_at(f):
    t=f/FPS
    bi=next(i for i,b in enumerate(BL) if t<b['end']) if t<BL[-1]['end'] else NB-1
    img=base(t)*grad
    fr=np.clip(img,0,255).astype(np.uint8)
    for L,x,y,a,b in overlays:
        al=fade(t,a,b)
        if al>0: comp(fr,L,x,y,al)
    i=int(np.searchsorted(subs_starts,t,side='right'))-1
    if 0<=i<len(subs) and bi<NB-1:
        L,x,a,b=subs[i]
        if a<=t<=b+0.1: comp(fr,L,x,830,min(1.0,(t-a)/0.15))
    fr=put_logo(fr,amp_at(t))
    comp(fr,foot,OW-foot.shape[1]-40,OH-60,1.0)
    return fr
if __name__=='__main__':
    if sys.argv[1]=='prep':
        from concurrent.futures import ThreadPoolExecutor
        os.makedirs('slots',exist_ok=True)
        with ThreadPoolExecutor(4) as ex: list(ex.map(prep,range(len(slots))))
        print('prepped',len(slots)); sys.exit()
    a,b,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{OW}x{OH}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-threads','1',out]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for f in range(a,min(b,NF)):
        p.stdin.write(frame_at(f).tobytes())
        if f%240==0: print(f,NF,flush=True)
    p.stdin.close(); p.wait()
