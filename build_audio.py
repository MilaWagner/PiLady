import numpy as np,subprocess,json,os,sys
from scipy.ndimage import uniform_filter1d
import soundfile as sf
import script
SR=44100
TEMPO=float(sys.argv[1]) if len(sys.argv)>1 else 0.90
GAP=0.8; BLOCK_GAP=2.4; STAR=4.2
def load(path):
    r=subprocess.run(['ffmpeg','-v','error','-i',path,'-af',f'atempo={TEMPO},aresample={SR}','-ac','1','-f','f32le','-'],capture_output=True,check=True)
    return np.frombuffer(r.stdout,dtype=np.float32)
parts=[np.zeros(int(0.3*SR),dtype=np.float32)]
cur=0.3; tl={'blocks':[],'sents':[]}
for bi,b in enumerate(script.BLOCKS):
    bstart=cur; n=len(b['text'])
    for si,txt in enumerate(b['text']):
        if txt.strip()=='***':
            parts.append(np.zeros(int(STAR*SR),dtype=np.float32)); cur+=STAR; continue
        a=load(f'tts/{bi:02d}_{si:02d}.wav'); d=len(a)/SR
        parts.append(a); tl['sents'].append(dict(b=bi,s=si,start=cur,end=cur+d,text=txt)); cur+=d
        gap=GAP if si<n-1 else BLOCK_GAP
        parts.append(np.zeros(int(gap*SR),dtype=np.float32)); cur+=gap
    tl['blocks'].append(dict(start=bstart,end=cur))
voice=np.concatenate(parts); del parts
tail=3.5; voice=np.concatenate([voice,np.zeros(int(tail*SR),dtype=np.float32)])
total=len(voice)/SR
voice=voice/(np.max(np.abs(voice))+1e-9)*0.85
tl['total']=total
# voice envelope at 100 Hz for logo pulse
hop=SR//100; nn=len(voice)//hop
env100=np.sqrt((voice[:nn*hop].reshape(nn,hop)**2).mean(1)).astype(np.float32)
np.save('env100.npy',env100)
# duck envelope
k=int(0.25*SR); denv=uniform_filter1d(np.abs(voice),k,mode='constant')
duck=(1-0.45*np.clip(denv/0.12,0,1)).astype(np.float32); del denv
# music (chunked)
def note(m): return 440*2**((m-69)/12)
chords=[[57,64,69,73],[54,61,66,70],[52,59,64,68],[55,62,67,71]]
seg=22.0
shim=[]; rs=np.random.default_rng(77)
for j in range(int(total/28)):
    shim.append((rs.uniform(5,total-8),note(82+(j*3)%12)))
def music_chunk(c0,c1):
    n=c1-c0; tt=(np.arange(c0,c1)/SR)
    L=np.zeros(n,np.float32); R=np.zeros(n,np.float32)
    t0,t1=c0/SR,c1/SR
    for i in range(max(0,int((t0-4)//seg)),int(t1//seg)+1):
        s_t=i*seg
        if s_t>=t1 or s_t+seg+4<=t0: continue
        rng=np.random.default_rng(1000+i); ch=chords[i%4]
        x=tt-s_t
        env=np.clip(x/6,0,1)*np.clip((seg+4-x)/6,0,1)
        env=np.where((x>=0)&(x<=seg+4),env,0)
        for kk,m in enumerate(ch):
            f=note(m)
            for det in (-0.6,0.0,0.7):
                ph=rng.uniform(0,6.28)
                w=np.sin(2*np.pi*(f+det)*x+ph)+0.3*np.sin(2*np.pi*2*(f+det)*x+ph)
                lfo=0.75+0.25*np.sin(2*np.pi*(0.05+0.02*kk)*x+ph)
                sig=(w*env*lfo).astype(np.float32); pan=0.5+0.3*np.sin(ph)
                L+=sig*(1-pan); R+=sig*pan
    for st,f in shim:
        if st>t1 or st+12<t0: continue
        x=tt-st; e=np.exp(-np.clip(x,0,None)/2.5)*(x>0)
        s=(np.sin(2*np.pi*f*x)*e*0.05).astype(np.float32); L+=s*0.7; R+=s*0.3
    fade=(np.clip(tt/4,0,1)*np.clip((total-tt)/4,0,1)).astype(np.float32)
    return L*fade,R*fade
CH=SR*30
# calibrate rms on 90s sample
cl,cr=music_chunk(SR*30,SR*120); rms=float(np.sqrt(np.mean(np.concatenate([cl,cr])**2)))
gain=10**(-52/20)/rms
N=len(voice); peak=0.0
out=open('mix.f32','wb')
for c0 in range(0,N,CH):
    c1=min(N,c0+CH); L,R=music_chunk(c0,c1)
    d=duck[c0:c1]; v=voice[c0:c1]
    mixL=v*10**(-3/20)+L*gain*d; mixR=v*10**(-3/20)+R*gain*d
    peak=max(peak,float(np.max(np.abs(mixL))),float(np.max(np.abs(mixR))))
    out.write(np.stack([mixL,mixR],1).astype('<f4').tobytes())
out.close()
subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar','44100','-ac','2','-i','mix.f32','-af',f'volume={0.97/peak:.4f}','-c:a','aac','-b:a','160k','audio.m4a'],check=True)
os.remove('mix.f32')
# subtitle chunks
chunks=[]
for s in tl['sents']:
    words=s['text'].split(); n_w=len(words)
    pc=max(1,round(n_w/13)); size=int(np.ceil(n_w/pc))
    pieces=[' '.join(words[i:i+size]) for i in range(0,n_w,size)]
    tot=sum(len(p) for p in pieces); a=s['start']
    for p in pieces:
        dd=(s['end']-s['start'])*len(p)/tot
        chunks.append(dict(start=a,end=a+dd,text=p)); a+=dd
tl['chunks']=chunks
json.dump(tl,open('timeline.json','w'),ensure_ascii=False,indent=1)
print('tempo',TEMPO,'total min',round(total/60,2),'peak',peak,'music gain',gain)
print('blocks',[round((b['end']-b['start'])) for b in tl['blocks']])
