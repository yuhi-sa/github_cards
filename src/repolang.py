import json
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation

# github API overview
# https://docs.github.com/ja/rest/overview/endpoints-available-for-github-apps

root = "https://api.github.com/"

def getRepo(user):
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

def main():
    # テストデータ
    # repoLang = ['Dockerfile', 'Python', 'HTML', None, 'Jupyter Notebook', 'Rust', 'MATLAB', 'JavaScript', 'CSS', 'Shell', 'TeX', 'C', 'TypeScript']
    # repoLangNum = [1, 10, 3, 3, 4, 1, 1, 1, 1, 1, 2, 1, 1]

    user = os.environ.get("username")
    repoLang, repoLangNum = getRepo(user)
    fig, ax = plt.subplots()    
    colors = createColor("Set3", repoLang)
    chocopie = ax.pie(repoLangNum, labels=repoLang, autopct='%1.1f%%',shadow=True, startangle=0,colors=colors)
    ani = animation.FuncAnimation(fig, update, frames=91,fargs=[chocopie,ax,colors,repoLangNum,repoLang], interval=100)
    ani.save('../cards/repos.gif', writer="ffmpeg",dpi=100)

if __name__=='__main__':
    main()
