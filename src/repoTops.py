import json
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
import numpy as np

def getRepo(user):
    root = "https://api.github.com/"
    url = root + "users/" + str(user) +"/repos"
    repos = requests.get(url)
    Name = []
    Size = []
    if repos.status_code == 200:
        j = repos.json()
        for i in range(len(j)):
            Name.append(j[i]["name"])
            Size.append(j[i].get("size", 0))
    return Name, Size

def update(num,chocopie, ax, colors, Name, Size):
    if len(chocopie) > 0:
        ax.cla()
    chocopie = ax.pie(Size, labels=Name, autopct=lambda p: '{:.1f}%'.format(p) if p >= 2.5 else '', shadow=False, startangle=4*num ,colors=colors)
    ax.set_title("Top Size Repos")

def format(Name, Size):
    sumsum = sum(Size)
    if sumsum == 0:
        return [], []

    df = pd.DataFrame({'Name': Name, 'Size': Size})
    df['percentage'] = df['Size'] / sumsum

    main_df = df[df['percentage'] > 0.05]
    others_size = df[df['percentage'] <= 0.05]['Size'].sum()

    Name2 = main_df['Name'].tolist()
    Size2 = main_df['Size'].tolist()

    if others_size > 0:
        Name2.append("others")
        Size2.append(others_size)

    return Name2, Size2

def main():
    f = open('../username.txt', 'r')
    user = f.read()
    f.close()
    Name, Size = getRepo(user)
    Name, Size = format(Name, Size)

    if not Name:
        print("No repo data to generate chart.")
        return

    fig, ax = plt.subplots()
    colors = plt.get_cmap('plasma')(np.linspace(0.1, 0.9, len(Name)))
    chocopie = ax.pie(Size, labels=Name, autopct=lambda p: '{:.1f}%'.format(p) if p >= 5 else '' , shadow=False, startangle=0, colors=colors)
    ani = animation.FuncAnimation(fig, update, frames=91, fargs=(chocopie, ax, colors, Name, Size), interval=100)

    try:
        ani.save('../cards/top.gif', writer='imagemagick', dpi=100)
    except FileNotFoundError:
        print("imagemagick not found, falling back to ffmpeg.")
        ani.save('../cards/top.gif', writer='ffmpeg', dpi=100)

if __name__=='__main__':
    main()