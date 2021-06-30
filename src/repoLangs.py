import json
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation

def getRepo(user):
    root = "https://api.github.com/"
    url = root + "users/" + user +"/repos"

    repos = requests.get(url)

    repoLang = []
    repoLangNum = []
    if repos.status_code == 200:

        j = repos.json()

        for i in range(len(j)):
            lang = j[i]["language"]

            if lang == "None":
                pass
            elif lang in repoLang:
                repoLangNum[repoLang.index(lang)] += 1
            else:
                repoLang.append(lang)
                repoLangNum.append(1)
    return repoLang, repoLangNum

def createColor(cname, repoLang):
    cm = plt.get_cmap(cname)
    colors = []
    for i in range(len(repoLang)):
        colors.append(cm(i))
    return colors

def update(num,chocopie, ax, colors, repoLangNum, repoLang):
    if len(chocopie) > 0:
        ax.cla()  
    chocopie = ax.pie(repoLangNum, labels=repoLang, autopct='%1.1f%%',shadow=True, startangle=4*num ,colors=colors)
    ax.set_title("Repos per Language")

def format(Name, Size):
    sumsum = sum(Size)
    Name2 = []
    Size2 = []
    others = 0
    for i in range(len(Name)):
        if Size[i]/sumsum <= 0.05:
            others += Size[i]
        else:
            Name2.append(Name[i])
            Size2.append(Size[i])
    Name2.append("others")
    Size2.append(others)

    return Name2, Size2

def main():
    user = os.environ.get("username")
    repoLang, repoLangNum = getRepo(user)
    # repoLang, repoLangNum = format(repoLang, repoLangNum)
    fig, ax = plt.subplots()    
    colors = createColor("Set3", repoLang)
    chocopie = ax.pie(repoLangNum, labels=repoLang, autopct=lambda p: '{:.1f}%'.format(p) if p >= 5 else '',shadow=True, startangle=0,colors=colors)
    ani = animation.FuncAnimation(fig, update, frames=91,fargs=[chocopie,ax,colors,repoLangNum,repoLang], interval=100)
    ani.save('../cards/lang.gif', writer="ffmpeg",dpi=100)

if __name__=='__main__':
    main()