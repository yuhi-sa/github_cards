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

    Name = []
    Size = []
    if repos.status_code == 200:

        j = repos.json()

        for i in range(len(j)):
            Name.append(j[i]["name"])
            Size.append(j[i]["size"])

    return Name, Size
            

def createColor(cname, Name):
    cm = plt.get_cmap(cname)
    colors = []
    for i in range(len(Name)):
        colors.append(cm(i))
    return colors

def update(num,chocopie, ax, colors, Name, Size):
    if len(chocopie) > 0:
        ax.cla()  
    chocopie = ax.pie(Size, labels=Name, autopct=lambda p: '{:.1f}%'.format(p) if p >= 2.5 else '',shadow=True, startangle=4*num ,colors=colors)
    ax.set_title("Top Size Repos")

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
    Name, Size = getRepo(user)
    Name, Size = format(Name, Size)
    fig, ax = plt.subplots()    
    colors = createColor("Set3", Name)
    chocopie = ax.pie(Size, labels=Name, autopct=lambda p: '{:.1f}%'.format(p) if p >= 2.5 else '' ,shadow=True, startangle=0,colors=colors)
    ani = animation.FuncAnimation(fig, update, frames=91,fargs=[chocopie,ax,colors,Name,Size], interval=100)
    ani.save('../cards/top.gif', writer="ffmpeg",dpi=100)

if __name__=='__main__':
    main()