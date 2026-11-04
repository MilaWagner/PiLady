import subprocess,os,sys
from concurrent.futures import ThreadPoolExecutor
from cand_lists import CANDS
used=set(l.split()[0] for l in open('used_all.txt') if l.strip())
allc=[c for b in CANDS for c in b if c not in used]
allc=list(dict.fromkeys(allc))
def dl(c):
    out=f'clips/{c}.mp4'
    if os.path.exists(out) and os.path.getsize(out)>100000: return c,True
    r=subprocess.run(['curl','-sS','-f','--max-time','120','-o',out,f'https://cdn.coverr.co/videos/{c}/1080p.mp4'],capture_output=True)
    ok=r.returncode==0 and os.path.getsize(out)>100000
    if not ok and os.path.exists(out): os.remove(out)
    return c,ok
with ThreadPoolExecutor(6) as ex: res=list(ex.map(dl,allc))
bad=[c for c,ok in res if not ok]
print('downloaded',len(res)-len(bad),'bad',bad)
d=open('clips/durs.txt','w')
for c,ok in res:
    if not ok: continue
    r=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'clips/{c}.mp4'],capture_output=True,text=True)
    try: d.write(f'{c} {float(r.stdout.strip())}\n')
    except Exception: print('probe fail',c)
d.close()
