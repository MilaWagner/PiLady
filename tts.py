import asyncio,ssl,os,re,subprocess,sys,json
import edge_tts,edge_tts.communicate as C
C._SSL_CTX=ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
import script
sents=[(bi,si,t) for bi,b in enumerate(script.BLOCKS) for si,t in enumerate(b['text'])]
sem=asyncio.Semaphore(4)
async def one(t,out,tries):
    for a in range(tries):
        try:
            async with sem:
                c=edge_tts.Communicate(t,"ru-RU-DmitryNeural")
                await asyncio.wait_for(c.save(out),30)
            if os.path.getsize(out)>2000: return True
        except Exception: pass
        await asyncio.sleep(0.4+0.2*a)
    return False
def variants(t):
    return [t, t[:1].lower()+t[1:], t.rstrip('.'), t[:1].lower()+t[1:].rstrip('.')]
async def synth(bi,si,t):
    out=f'tts/{bi:02d}_{si:02d}.mp3'
    if os.path.exists(out) and os.path.getsize(out)>2000: return
    for v in variants(t):
        if await one(v,out,6): return
    # clause split
    parts=[p.strip() for p in re.split(r'(?<=[,:;—])\s+',t) if p.strip()]
    if len(parts)>1:
        files=[]
        for i,p in enumerate(parts):
            f=f'tts/{bi:02d}_{si:02d}_p{i}.mp3'
            ok=False
            for v in variants(p):
                if await one(v,f,6): ok=True;break
            if not ok: print('FAILPART',bi,si,p,flush=True); return
            files.append(f)
        open(f'tts/{bi:02d}_{si:02d}.txt','w').write(''.join(f"file '{os.path.abspath(f)}'\n" for f in files))
        subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',f'tts/{bi:02d}_{si:02d}.txt','-c','copy',out],check=True)
        return
    print('FAIL',bi,si,t,flush=True)
async def main():
    await asyncio.gather(*[synth(*s) for s in sents])
    miss=[(bi,si) for bi,si,t in sents if not os.path.exists(f'tts/{bi:02d}_{si:02d}.mp3')]
    print('DONE missing',miss,flush=True)
asyncio.run(main())
