import re
from urllib.request import Request, urlopen
import pandas
ovr = []
name = []
stat = []
sho = []
dri = []
pas = []
de = []
pac = []
phy = []
ntn = []
pic = []
club = []
a = ''
b = ''
c = ''
ide = 0
for k in range(1,12):
    req = Request("https://www.futhead.com/18/players/?level=gold_nif&group=cf&page="+str(k)+"&bin_platform=xb", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    data = webpage.decode("utf-8")
    indices = []
    for i in range(0,48):
        x = '<span class="revision-gradient shadowed font-12 fut18 gold nif">'  
        indices = [s.end() for s in re.finditer(x,data)]
        ovr.append(data[indices[i]:indices[i]+2])
        x = '<span class="player-name">'
        indices = [s.end() for s in re.finditer(x,data)]
        a = data[indices[i]:indices[i]+25]
        b = a.split("<")[0].split(' ')
        ide = len(b)
        name.append(b[ide-1].lower())
        x = 'player-image'
        indices = [s.end() for s in re.finditer(x,data)]
        a = data[indices[i]:indices[i]+300]
        b = re.search("data-src",a)
        c = re.search("png",a)
        pic.append(a[b.end()+2 : c.end()])
        x = 'player-nation'
        indices = [s.end() for s in re.finditer(x,data)]
        a = data[indices[i]:indices[i]+300]
        b = re.search("data-src",a)
        c = re.search("png",a)
        ntn.append(a[b.end()+2 : c.end()])
    x = 'player-club'
    indices = [s.end() for s in re.finditer(x,data)]
    for i in range(0,96,2):
        a = data[indices[i]:indices[i]+300]
        b = re.search("data-src",a)
        c = re.search("png",a)
        club.append(a[b.end()+2 : c.end()])
    for i in range(0,288):
        x = '<span class="player-stat stream-col-60 hidden-md hidden-sm"><span class="value">'
        indices = [s.end() for s in re.finditer(x,data)]
        stat.append(data[indices[i]:indices[i]+2])
    for i in range(0,288):
        ide = (i+1)%6
        if ide == 1:
            pac.append(stat[i])
        elif ide == 2:
            sho.append(stat[i])
        elif ide == 3:
            pas.append(stat[i])
        elif ide == 4:
            dri.append(stat[i])
        elif ide == 5:
            de.append(stat[i])
        elif ide == 0:
            phy.append(stat[i])
        else:
            pass
    di = {"Ovr": ovr, "Name": name, "Pac": pac, "Sho": sho, "Pas": pas, "Dri": dri, "Def": de, "Phy": phy, "Pic": pic, "Club": club, "Nation": ntn}
    players = pandas.DataFrame(di, columns=["Ovr", "Name", "Pac", "Sho", "Pas", "Dri", "Def", "Phy", "Pic", "Club", "Nation"])
    players.to_csv('st.csv', encoding = 'utf-8', index = False)
