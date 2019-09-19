import requests
from bs4 import BeautifulSoup as bs


def get_series():
    episodes_list = []
    series = [{'name': 'We Bare Bears',
               'link': 'http://webarebears.cn-fan.tv/series.php?id=',
               'voice': ''},
              {'name': 'Disenchantment',
               'link': 'http://disenchantment.nf-fan.tv/series.php?id=',
               'voice': '&voice=13'},
              {'name': 'Love. Death. Robots',
               'link': 'http://ldr.nf-fan.tv/series.php?id=',
               'voice': '&voice=1'}  # 1-Rus.Pifagor, 4-Original+RusSub, 5-Original+EngSub
              ]
    res = '<html>\n<head></head>\n<body>\n'
    for s in series:
        res += f"<h3>{s['name']}</h3>"
        episodes_list = []
        for episode in range(101, 150):
            try:
                req = requests.get(f"{s['link']}{episode}{s['voice']}")
                cont = bs(req.text, 'lxml')
                e = str(cont.find_all('script', class_=None)[-1:][0])
                ret = []
                tr = str.maketrans('")', '  ')
                [ret.append(i.split(',')[1].split(';')[0]) for i in e.split('\t') if 'mp4' in i]
                [episodes_list.append(str(i).translate(tr).strip(' ')) for i in ret]
            except:
                break
        res += '\n<br>'.join([f'<a href={i}>{i.split("/")[-1:]}</a>' for i in episodes_list])
    res += '\n</body>\n</html>'
    return res
