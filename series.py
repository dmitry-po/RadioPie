import requests
from bs4 import BeautifulSoup as bs


def get_series():
    episodes_list = []
    for episode in range(101, 130):
        try:
            req = requests.get(f'http://webarebears.cn-fan.tv/series.php?id={episode}')
            # req = requests.get(f'http://disenchantment.nf-fan.tv/series.php?id={episode}&voice=13')
            cont = bs(req.text, 'lxml')
            e = str(cont.find_all('script', class_=None)[-1:][0])
            res = []
            tr = str.maketrans('")', '  ')
            [res.append(i.split(',')[1].split(';')[0]) for i in e.split('\t') if 'mp4' in i]
            [episodes_list.append(str(i).translate(tr).strip(' ')) for i in res]
        except:
            break
    res = '<html>\n<head></head>\n<body>\n'
    res += '\n<br>'.join([f'<a href={i}>{i.split("/")[-1:]}</a>' for i in episodes_list])
    res += '\n</body>\n</html>'
    return res
