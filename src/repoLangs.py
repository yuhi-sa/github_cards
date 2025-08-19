import json
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def getRepo(user):
    root = "https://api.github.com/"
    url = root + "users/" + str(user) +"/repos"

    repos = requests.get(url)

    repoLang = []
    repoLangNum = []
    if repos.status_code == 200:

        j = repos.json()

        for i in range(len(j)):
            lang = j[i]["language"]

            if lang == None:
                pass
            elif lang in repoLang:
                repoLangNum[repoLang.index(lang)] += 1
            else:
                repoLang.append(lang)
                repoLangNum.append(1)
    return repoLang, repoLangNum

def format(Name, Size):
    sumsum = sum(Size)
    if sumsum == 0:
        return Name, Size

    Name2 = []
    Size2 = []
    others = 0
    for i in range(len(Name)):
        if Size[i]/sumsum <= 0.05:
            others += Size[i]
        else:
            Name2.append(Name[i])
            Size2.append(Size[i])

    if others > 0:
        Name2.append("others")
        Size2.append(others)

    return Name2, Size2

def main():
    f = open('../username.txt', 'r') 
    user = f.read()
    f.close()
    repoLang, repoLangNum = getRepo(user)

    repoLang, repoLangNum = format(repoLang, repoLangNum)

    if not repoLang:
        print("No language data to generate chart.")
        return

    df = pd.DataFrame({'Language': repoLang, 'Count': repoLangNum})
    df = df.sort_values(by='Count', ascending=True)

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 8))

    # Ensure there's data to avoid max() error on empty sequence
    if df.empty:
        print("DataFrame is empty, cannot generate chart.")
        return

    cmap = plt.get_cmap('plasma')
    colors = cmap(df['Count'] / float(df['Count'].max()))

    bars = ax.barh(df['Language'], df['Count'], color=colors, height=0.6)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(False)

    ax.set_title("Repos per Language", fontsize=20, fontweight='bold', pad=20)

    ax.xaxis.set_visible(False)
    ax.yaxis.set_tick_params(labelsize=12)

    for bar in bars:
        width = bar.get_width()
        label_x_pos = width + (df['Count'].max() * 0.01)
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{int(width)}',
                va='center', ha='left', fontsize=12, fontweight='bold')

    fig.tight_layout()

    fig.savefig('../cards/lang.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())

if __name__=='__main__':
    main()