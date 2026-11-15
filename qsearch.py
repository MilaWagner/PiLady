import subprocess,re,json,sys
from concurrent.futures import ThreadPoolExecutor
def get(q):
    h=subprocess.run(['curl','-s','--max-time','40',f'https://coverr.co/s?q={q.replace(" ","+")}'],capture_output=True,text=True).stdout
    return list(dict.fromkeys(re.findall(r'cdn\.coverr\.co/videos/(coverr-[a-z0-9_-]+)',h)))
base=set(get('zzqxjkv'))
used=set(l.split()[0] for l in open('used_all.txt') if l.strip())
qs=[l.strip() for l in open(sys.argv[1],encoding='utf-8') if l.strip()]
with ThreadPoolExecutor(6) as ex: res=list(ex.map(get,qs))
out={}
for q,r in zip(qs,res):
    out[q]=[s for s in r if s not in base and s not in used and 'premium' not in s and 'temp' not in s]
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
allc=set(s for v in out.values() for s in v)
print(len(qs),'queries',len(allc),'unique unused')
