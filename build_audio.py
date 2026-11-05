import numpy as np,subprocess,json,os,re
import script
SR=44100
def load(path):
    r=subprocess.run(['ffmpeg','-v','error','-i',path,'-af','atempo=1.03,aresample=44100','-ac','1','-f','f32le','-'],capture_output=True,check=True)
    return np.frombuffer(r.stdout,dtype=np.float32)
voice=[np.zeros(int(0.15*SR),dtype=np.float32)]
t=0.15; tl={'blocks':[],'sents':[]}
cur=t
for bi,b in enumerate(script.BLOCKS):
    bstart=cur
    for si,txt in enumerate(b['text']):
        a=load(f'tts/{bi:02d}_{si:02d}.mp3')
        d=len(a)/SR
        voice.append(a); tl['sents'].append(dict(b=bi,s=si,start=cur,end=cur+d,text=txt))
        cur+=d
        gap=0.28 if si<len(b['text'])-1 else 0.9
        voice.append(np.zeros(int(gap*SR),dtype=np.float32)); cur+=gap
    tl['blocks'].append(dict(start=bstart,end=cur))
voice=np.concatenate(voice)
total=len(voice)/SR+3.5
voice=np.concatenate([voice,np.zeros(int(3.5*SR),dtype=np.float32)])
# normalize voice
voice=voice/ (np.max(np.abs(voice))+1e-9)*0.85
tl['total']=total
# music: B-flat aeolian drone pad, unique key for this video
rng=np.random.default_rng(89)
n=len(voice); tt=np.arange(n)/SR
def note(m): return 440*2**((m-69)/12)
chords=[[45,52,57,61],[40,47,52,56],[43,50,55,59],[38,45,50,54]]
L=np.zeros(n);R=np.zeros(n)
seg=22.0
for i in range(int(total/seg)+2):
    ch=chords[i%len(chords)]
    s0=int(i*seg*SR); s1=min(n,int((i+1)*seg*SR+4*SR))
    if s0>=n: break
    x=tt[s0:s1]-i*seg
    env=np.clip(x/6,0,1)*np.clip((seg+4-x)/6,0,1)
    for k,m in enumerate(ch):
        f=note(m)
        for det in (-0.6,0.0,0.7):
            ph=rng.uniform(0,6.28)
            w=np.sin(2*np.pi*(f+det)*x+ph)+0.3*np.sin(2*np.pi*2*(f+det)*x+ph)
            lfo=0.75+0.25*np.sin(2*np.pi*(0.05+0.02*k)*x+ph)
            sig=w*env*lfo
            pan=0.5+0.3*np.sin(ph)
            L[s0:s1]+=sig*(1-pan);R[s0:s1]+=sig*pan
# soft high shimmer
for j in range(14):
    f=note(82+ (j*3)%12); st=rng.uniform(5,total-8); x=tt-st
    env=np.exp(-np.clip(x,0,None)/2.5)*(x>0)
    s=np.sin(2*np.pi*f*x)*env*0.05
    L+=s*0.7;R+=s*0.3
fade=np.clip(tt/4,0,1)*np.clip((total-tt)/4,0,1)
L*=fade;R*=fade
mus=np.stack([L,R],1)
rms=np.sqrt(np.mean(mus**2)); mus=mus/rms
# level: music about -44 dB rms relative to full scale, voice rms ~ -20
mus*=10**(-52/20)
# duck under voice
env=np.abs(voice); k=int(0.25*SR)
env=np.convolve(env,np.ones(k)/k,mode='same'); duck=1-0.45*np.clip(env/0.12,0,1)
mus*=duck[:,None]
vst=np.stack([voice,voice],1)
mix=vst*10**(-3/20)+mus
peak=np.max(np.abs(mix)); print('peak',peak,'music rms dB',20*np.log10(np.sqrt(np.mean(mus**2))), 'voice rms dB',20*np.log10(np.sqrt(np.mean(voice**2))))
mix=mix/max(peak,1)*0.97
pcm=(mix*32767).astype('<i2')
open('mix.raw','wb').write(pcm.tobytes())
subprocess.run(['ffmpeg','-y','-v','error','-f','s16le','-ar','44100','-ac','2','-i','mix.raw','-c:a','aac','-b:a','160k','audio.m4a'],check=True)
np.save('voice.npy',voice)
# subtitle chunks
chunks=[]
for s in tl['sents']:
    words=s['text'].split(); n_w=len(words)
    parts=max(1,round(n_w/13)); size=int(np.ceil(n_w/parts))
    pieces=[' '.join(words[i:i+size]) for i in range(0,n_w,size)]
    tot=sum(len(p) for p in pieces); a=s['start']
    for p in pieces:
        d=(s['end']-s['start'])*len(p)/tot
        chunks.append(dict(start=a,end=a+d,text=p)); a+=d
tl['chunks']=chunks
json.dump(tl,open('timeline.json','w'),ensure_ascii=False,indent=1)
print('total',total, 'blocks',[(round(b['start']),round(b['end'])) for b in tl['blocks']])
