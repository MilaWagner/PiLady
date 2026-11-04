import subprocess,re,sys
from concurrent.futures import ThreadPoolExecutor
def get(q):
    h=subprocess.run(['curl','-s','--max-time','40',f'https://coverr.co/s?q={q.replace(" ","+")}'],capture_output=True,text=True).stdout
    return list(dict.fromkeys(re.findall(r'cdn\.coverr\.co/videos/(coverr-[a-z0-9_-]+)',h)))
base=set(get('zzqxjkv'))
used=set(l.split()[0] for l in open('/home/claude/vbrain/used_all.txt') if l.strip())
qs=sys.argv[1:]
with ThreadPoolExecutor(6) as ex: res=list(ex.map(get,qs))
for q,r in zip(qs,res):
    r=[s for s in r if s not in base and s not in used and 'premium' not in s and 'temp' not in s]
    print('==',q,len(r)); print(' '.join(r[:14]))
