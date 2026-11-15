import re,json,math,random
tl=json.load(open('timeline.json')); BL=tl['blocks']; total=tl['total']
durs={l.split()[0]:float(l.split()[1]) for l in open('clips/durs.txt')}
BAD=re.compile(r'christmas|xmas|bible|religious|rosary|marijuana|weed|cigarette|smoking|weapon|seduct|kiss|champagne|beer|whisk|cognac|bartender|cocktail|casino|hanukkah|halloween|skull|clown|crypto|trade|thanksgiving|turkey|valentine|mother-s-day|twins|hide|swimsuit|swimwear|bikini|mask-and|tattoo|baby|newborn|crib|pregnant|stroller|cannabis|santa|candle|prays|pray|wine|drink-from|plane|private-jets|gas-station|air-kiss|whispering|flirting|sneakers|filmmaker|videographer|dance|dancing|hula|pov-walking|bulldozer|backhoe|toilet|handyman|hose|surf|longboard|skii?ng|ski-|a-man-does|push-ups|treadmill|man-rolling|out-of-breath|club|apocalyptic|scrabble|stop-sign|billboard|flags|tire|propeller|buffalo|parcel|spray|cleaning')
def tag(s):
    n=s[6:]
    return n
pool={k:[] for k in ['REFLECT','PHONE','CITY','EMPTY','NIGHT','CROWD','MONEY','FOOD','COFFEE','HOME','COUPLE','FAMILY','PETS','NATURE','CALM','WATER','TRAVEL','GARDEN','PARK','WORK','MARKET','VILLA','BEACH','FRIENDS']}
R={
'REFLECT':r'window|balcony|silhouette|looking-up|man-sitting-by|man-looking-at-nature|yawning',
'PHONE':r'smartphone|iphone|texting|phone|selfie|video-call|laptop',
'CITY':r'street|traffic|subway|bridge|city|town|tram|road|plaza|alley|walking-on|pedestrian|broadway|lviv|vilnius|brooklyn|london',
'EMPTY':r'empty|quiet|alley|narrow|small-alleyway|cathedral',
'NIGHT':r'night|bokeh|lights',
'MONEY':r'banknote|card-details|amazon|delivery|fish|market|sewing|street-food|food-vendor|food-sellers|shopping',
'FOOD':r'cooking|pouring|eggs|dough|mixer|pizza|pasta|gnocchi|sandwich|pie|orange|grapes|grill|cracking|whisking|milk|cake|baking|sushi|menu|restaurant|dinner|breakfast|ice-cream|picnic',
'COFFEE':r'coffee|a-cup|mug|breakfast|tea|juice|water',
'HOME':r'kitchen|house|home|sofa|couch|bed|room|tour|wardrobe|packing|tv|interior',
'COUPLE':r'couple|boyfriend|girlfriend|hugging|embrace|holding-each|meeting|a-stroll',
'FAMILY':r'mom|dad|father|grand|parents|daughter|son|family|child|boy|girl-jump|friends-embrace',
'PETS':r'cat|dog|kitten|horse',
'NATURE':r'mountain|forest|hill|meadow|lake|fog|valley|coast|rocky|campervan|wilderness|wind|national|plant|leaves|field|grass|palm|tropical',
'CALM':r'fog|lake|mist|mountains|plant-swaying|sunset|meadow|forest|hill|valley|coast|sea|horses-on-a-misty|house-by',
'WATER':r'boat|sail|yacht|kayak|canoe|ocean|sea|fisherman|fishing|marina|harbor|lagoon|cruising|paddling|port|dock|pier',
'TRAVEL':r'road|driving|car|campervan|suitcase|luggage|baggage|journey|journey|motorcycle|bike|trip',
'GARDEN':r'garden|peas|grape|vine|berries|leaves|plant|harvest|orchard',
'PARK':r'park|swings|walking|stretch|jogging|running|neighborhood|stroll',
'WORK':r'laptop|working|computer|smiling-couple-working|texting',
'MARKET':r'market|vendor|food|sellers|fish|sewing',
'VILLA':r'villa|resort|pool|yacht|marina|hotel|house-by|lake',
'BEACH':r'beach|surfer|sand|tropical|coast|palm|sea',
'FRIENDS':r'friends|picnic|party|confetti|toast|laughing|group|couple-walking|walking',
}
pool_all=[c for c in durs if not BAD.search(c)]
for c in pool_all:
    n=tag(c)
    for k,rx in R.items():
        if re.search(rx,n): pool[k].append(c)
random.seed(11)
for k in pool: random.shuffle(pool[k])
recipe=[ # per block categories (round robin)
 ['REFLECT','PHONE','CITY'],['CITY','CROWD' if False else 'PARK'],['REFLECT','WORK','PHONE'],['MONEY','FOOD','CITY'],['CITY','NIGHT','PARK'],
 ['HOME','FOOD','COFFEE'],['MONEY','PHONE','MARKET'],['MONEY','PHONE','CITY'],['COFFEE','FOOD','MARKET'],['CITY','COFFEE','PHONE'],
 ['TRAVEL','NATURE','CALM'],['GARDEN','NATURE','CALM'],['CITY','PARK','REFLECT'],['HOME','PHONE','COFFEE'],['CALM','WATER','NATURE'],
 ['REFLECT','CITY','PHONE'],['WORK','PHONE','HOME'],['NIGHT','CITY','REFLECT'],['COUPLE','PARK','FAMILY'],['COUPLE','FAMILY','HOME'],
 ['COUPLE','FAMILY','FRIENDS'],['HOME','COFFEE','COUPLE'],['FAMILY','PETS','HOME'],['EMPTY','CALM','REFLECT'],['NATURE','TRAVEL','CALM'],
 ['CITY','VILLA','WATER'],['CALM','REFLECT','PETS'],['FAMILY','COUPLE','FRIENDS'],['CALM','WATER','NATURE'],['HOME','COUPLE','COFFEE'],
 ['CALM','NATURE','WATER'],['VILLA','TRAVEL','WATER'],['BEACH','FRIENDS','WATER'],['FOOD','FRIENDS','FAMILY'],['GARDEN','CALM','COFFEE'],
 ['PARK','NATURE','FAMILY'],['HOME','COUPLE','COFFEE'],['CALM','NATURE','WATER'],['WATER','BEACH','CALM']]
assert len(recipe)>=len(BL),(len(recipe),len(BL))
used=set(); out=[]; plan=[]
def take(cat,mind):
    for c in pool.get(cat,[]):
        if c not in used and durs[c]>=mind: used.add(c); return c
for bi,b in enumerate(BL):
    s=0.0 if bi==0 else b['start']; e=total if bi==len(BL)-1 else b['end']
    n=max(1,math.ceil((e-s)/10.5)); slot=(e-s)/n; mind=max(4.8,slot/1.2+0.6)
    cl=[]; k=0
    for j in range(n):
        got=None
        for t in range(len(recipe[bi])*2):
            got=take(recipe[bi][(k+t)%len(recipe[bi])],mind)
            if got: break
        k+=1
        if not got:
            for cat in ['CALM','NATURE','CITY','PARK','WATER','HOME']:
                got=take(cat,mind)
                if got: break
        if not got: got=next(c for c in pool_all if c not in used and durs[c]>=mind); used.add(got)
        cl.append(got)
    out.append(cl); plan.append((bi,n,round(slot,1)))
open('clips.py','w').write('CLIPS='+json.dumps(out,indent=0)+'\n')
print('slots',sum(len(x) for x in out),'unique',len(set(c for x in out for c in x)),'pool',len(pool_all))
print(plan[:6])
