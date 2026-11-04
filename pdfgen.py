import json,script
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
pdfmetrics.registerFont(TTFont('S','/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'))
pdfmetrics.registerFont(TTFont('SB','/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'))
tl=json.load(open('timeline.json'))
def ts(sec):
    sec=int(round(sec)); return f"{sec//60}:{sec%60:02d}"
names={'ОТКУДА ЭТО ВЗЯЛОСЬ':'Откуда взялся миф','ДРУГИЕ ВОЗМОЖНЫЕ ИСТОКИ':'Другие возможные истоки','ПОЧЕМУ В ЭТО ВЕРЯТ':'Почему в это верят: опрос и фильм «Люси»','ЧТО ПОКАЗЫВАЮТ ТРАВМЫ':'Аргумент 1: травмы мозга','ЭНЕРГИЯ И ЭВОЛЮЦИЯ':'Аргумент 2: энергия и эволюция','ЧТО ПОКАЗЫВАЕТ СКАНИРОВАНИЕ':'Аргумент 3: сканирование мозга','ГДЕ ЕСТЬ РЕЗЕРВ':'Где есть резерв','ГЛАВНОЕ':'Итог'}
chap=[("0:00","Вступление")]
for i,b in enumerate(script.BLOCKS):
    if 'chapter' in b: chap.append((ts(tl['blocks'][i]['start']),names[b['chapter']]))
chap_txt="\n".join(f"{a} {b}" for a,b in chap)
dur=ts(tl['total']-3.5)
desc=("Правда ли, что человек использует только десять процентов мозга? Разбираем, откуда взялась эта цифра (Уильям Джеймс, предисловие Лоуэлла Томаса 1936 года к книге Карнеги), почему в миф верят (опрос в Рио-де-Жанейро, фильм «Люси») и что показывают травмы, энергозатраты и сканирование мозга.\n"
"Только то, что можно проверить, и честные оговорки. Миф о десяти процентах не подтверждается, а потенциал человека связан с обучением и опытом, а не с «молчащими» девяноста процентами мозга.\n\n"
+chap_txt+"\n\nИсточник — канал о том, кто мы на самом деле. Без религиозных догм и эзотерического тумана. Подписывайтесь.\n\n#мозг #мифыомозге #нейронаука #психология #источник")
tags=["10 процентов мозга","миф о 10 процентах мозга","используем ли мы 10 процентов мозга","мифы о мозге","как работает мозг","нейронаука","психология","нейроны","фильм Люси правда или нет","мозг человека","наука о мозге","Источник"]
json.dump(dict(title=script.TITLE,description=desc,tags=tags),open('meta.json','w'),ensure_ascii=False,indent=1)
facts=[
"B. Beyerstein, «Whence cometh the myth that we only use ten percent of our brains?», в сб. S. Della Sala (ed.), Mind Myths, Wiley, 1999, с. 1-24; популярный пересказ: Scientific American, «Do we really use only 10 percent of our brains?»: следы мифа ведут к У. Джеймсу, фраза о «10 процентах способностей» превратилась в «10 процентов мозга»; самая сильная раскрутка пришла через Лоуэлла Томаса и книгу Карнеги; шесть линий опровержения (травмы, сканирование, эволюция и энергия и др.).",
"У. Джеймс, «The Energies of Men» (1907/1908): мы используем лишь малую часть своих возможных умственных и физических ресурсов. Процент Джеймс не называл (Encyclopaedia Britannica).",
"Л. Томас, предисловие (1936) к книге Д. Карнеги «How to Win Friends and Influence People»: Джеймс якобы говорил, что средний человек развивает лишь 10 процентов своих скрытых умственных способностей.",
"S. Herculano-Houzel, «Do you know your brain? A survey on public neuroscience literacy at the closing of the decade of the brain», The Neuroscientist 8(2), 98-110 (2002); редакционная заметка «Brain myths», Nature Neuroscience 6, 99 (2003): около половины людей с высшим образованием в Рио-де-Жанейро верили в миф о 10 процентах.",
"F. Azevedo, ... S. Herculano-Houzel, «Equal numbers of neuronal and nonneuronal cells make the human brain an isometrically scaled-up primate brain», J. Comp. Neurol. 513(5), 532-541 (2009): в среднем 86,1 ± 8,1 млрд нейронов и 84,6 ± 9,8 млрд ненейронных клеток (метод изотропного фракционатора).",
"S. Herculano-Houzel, «The remarkable, yet not extraordinary, human brain as a scaled-up primate brain and its associated cost», PNAS 109 (Suppl 1), 10661-10668 (2012): около 2% массы тела и около 20% энергии организма.",
"M. Raichle, «The brain's dark energy», Science 314, 1249-1250 (2006); M. Raichle, «Two views of brain function», Trends in Cognitive Sciences 14(4), 180-190 (2010): рост расхода энергии при задачах часто меньше 5%; 60-80% энергии мозга связаны с передачей сигналов.",
"Фильм «Люси» (2014): герой Моргана Фримена утверждает, что люди используют около 10% возможностей мозга (разборы: Slate, Emory University, 2014). Замечание про судорожный припадок при одновременной активности всех нейронов: Slate.",
]
ver=[
"Проверено поиском 04.11.2026 по статье Scientific American (Beyerstein), Encyclopaedia Britannica, редакционной заметке Nature Neuroscience, аннотациям PubMed/PNAS (Herculano-Houzel 2009 и 2012), обзору Raichle 2010 (Trends in Cognitive Sciences), материалам Slate и Emory о фильме «Люси».",
"Не проверено по первоисточнику: полные тексты не читала. Версии про клетки глии (в 10 раз больше нейронов) и про опыты Лэшли с крысами как возможные истоки мифа взяты из вторичных источников (обзоры, Gizmodo, Wikipedia) и в видео поданы как гипотезы. Точной цифры опроса в Рио (в пересказах 59% и 6% нейроучёных) в видео нет: сказано «примерно половина».",
"Мои формулировки (общие, не научные факты): «Небольшое повреждение в нужном месте может нарушить речь, зрение или движение»; «в течение суток работает весь мозг»; «резерв в навыках, знаниях и привычках, которые можно развивать учёбой и практикой». Мозг частично перестраивается после травм: общеизвестный факт, в видео как оговорка.",
"Ударения и имена: голос Дмитрий (Microsoft). Проверьте на слух: Байерстайн, Лэшли, Эркулано-Хаузел, Райхл, Джеймс, Карнеги, Лоуэлл Томас, Рио-де-Жанейро, «Люси». Напишите, что прозвучало неверно, я исправлю.",
]
cover_en=("bright warm cinematic photo, a calm woman in her thirties looking up with curiosity, a soft glowing golden brain-shaped light made of fine sparks floating above her open hand, sunlit airy background with warm bokeh, clean negative space on the right for text, hopeful uplifting mood, no text, 16:9")
cover_ru=("Тёплый светлый кинематографичный кадр: спокойная женщина смотрит вверх с интересом, над раскрытой ладонью мягко светится золотистая форма мозга из мелких искр, воздушный солнечный фон, справа свободное место под текст. Надпись на обложке: «10% МОЗГА — МИФ?» (жёлтым «МИФ?», подзаголовок «Что говорит наука»).")
H=lambda t,s: Paragraph(t,s)
st=dict(h1=ParagraphStyle('h1',fontName='SB',fontSize=17,leading=22,textColor=HexColor('#8a6d2f'),spaceAfter=8),
 h2=ParagraphStyle('h2',fontName='SB',fontSize=12,leading=16,textColor=HexColor('#8a6d2f'),spaceBefore=12,spaceAfter=4),
 p=ParagraphStyle('p',fontName='S',fontSize=9.5,leading=14,textColor=HexColor('#222222'),spaceAfter=4))
def foot(c,d):
    c.saveState(); c.setFont('S',8); c.setFillColor(HexColor('#777777'))
    c.drawString(40,26,"Людмила Вагнер · Источник · Видео «Миф о 10% мозга»"); c.drawRightString(A4[0]-40,26,str(d.page)); c.restoreState()
doc=BaseDocTemplate('Видео-Мозг-описание.pdf',pagesize=A4,leftMargin=40,rightMargin=40,topMargin=40,bottomMargin=48)
doc.addPageTemplates([PageTemplate(id='a',frames=[Frame(40,48,A4[0]-80,A4[1]-88)],onPage=foot)])
def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('\n','<br/>')
S=[H("МИФ О 10% МОЗГА: правда ли, что мы используем только десятую часть?",st['h1']),H(f"Что говорит наука · длительность {dur}",st['p']),
 H("Заголовок",st['h2']),H(esc(script.TITLE),st['p']),H("Текст обложки",st['h2']),H("10% МОЗГА — МИФ?",st['p']),
 H("Описание",st['h2']),H(esc(desc),st['p']),H("Теги",st['h2']),H(esc(", ".join(tags)),st['p']),
 H("Промпт для обложки",st['h2']),H(esc(cover_en),st['p']),H(esc(cover_ru),st['p']),
 H("При загрузке отметить",st['h2']),H("Не для детей · без платной рекламы · контент создан ИИ · публикация 28 ноября 2026, 00:00",st['p']),
 H("Видеоматериал",st['h2']),H("Стоковые клипы Coverr (бесплатная лицензия, в том числе для коммерческого использования, без обязательной атрибуции). Музыка создана программно, лицензии не требуется.",st['p']),
 H("Факты и источники",st['h2'])]+[H("• "+esc(f),st['p']) for f in facts]+[H("Что проверено, что нет",st['h2'])]+[H("• "+esc(v),st['p']) for v in ver]
S+=[PageBreak(),H("Полный текст видео",st['h1'])]
for b in script.BLOCKS:
    if 'chapter' in b: S.append(H(esc(b['chapter']),st['h2']))
    S.append(H(esc(" ".join(b['text'])),st['p']))
doc.build(S); print(chap_txt)
