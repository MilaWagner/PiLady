import torch,os,soundfile as sf,sys
import script
torch.set_num_threads(2)
imp=torch.package.PackageImporter('v4_ru.pt'); m=imp.load_pickle("tts_models","model"); m.to('cpu')
for bi,b in enumerate(script.BLOCKS):
    for si,t in enumerate(b['text']):
        if t.strip()=='***': continue
        out=f'tts/{bi:02d}_{si:02d}.wav'
        if os.path.exists(out) and os.path.getsize(out)>2000: continue
        a=m.apply_tts(text=t,speaker='eugene',sample_rate=48000,put_accent=True,put_yo=True)
        sf.write(out,a.numpy(),48000)
    print('block',bi,flush=True)
print('DONE',flush=True)
