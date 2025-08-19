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
    repoLang, repoLangNum = [], []
    if repos.status_code == 200:
        j = repos.json()
        for i in range(len(j)):
            lang = j[i]["language"]
            if lang is None:
                continue
            if lang in repoLang:
                repoLangNum[repoLang.index(lang)] += 1
            else:
                repoLang.append(lang)
                repoLangNum.append(1)
    return repoLang, repoLangNum

def format(Name, Size):
    sumsum = sum(Size)
    if sumsum == 0:
        return [], []
    df = pd.DataFrame({'Name': Name, 'Size': Size})
    df = df.sort_values(by='Size', ascending=False)

    # Keep top 9, group rest into 'others'
    top_df = df.head(9)
    others_size = df.iloc[9:]['Size'].sum()

    Name2 = top_df['Name'].tolist()
    Size2 = top_df['Size'].tolist()

    if others_size > 0:
        Name2.append("others")
        Size2.append(others_size)

    return Name2, Size2

def update(frame, ax, df, colors):
    ax.cla()  # Clear the axis

    # Calculate current width of bars for this frame
    current_widths = df['Count'] * frame / 30

    # Redraw the bars
    bars = ax.barh(df['Language'], current_widths, color=colors, height=0.6)

    # Redraw the styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(False)
    ax.set_title("Repos per Language", fontsize=20, fontweight='bold', pad=20)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_xlim(0, df['Count'].max() * 1.1)
    fig = plt.gcf()
    fig.tight_layout()

    # Redraw the value labels
    for bar in bars:
        width = bar.get_width()
        if width > 0:
            label_x_pos = width + (df['Count'].max() * 0.01)
            ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{int(width)}',
                    va='center', ha='left', fontsize=12, fontweight='bold')
    return ax,

def main():
    with open('../username.txt', 'r') as f:
        user = f.read().strip()

    repoLang, repoLangNum = getRepo(user)
    repoLang, repoLangNum = format(repoLang, repoLangNum)

    if not repoLang:
        print("No language data to generate chart.")
        return

    df = pd.DataFrame({'Language': repoLang, 'Count': repoLangNum})
    df = df.sort_values(by='Count', ascending=False).reset_index(drop=True)
    df = df.iloc[::-1] # Invert order for horizontal bar chart

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 8))

    if df.empty:
        print("DataFrame is empty, cannot generate chart.")
        return

    cmap = plt.get_cmap('plasma')
    colors = cmap(np.linspace(0.1, 0.9, len(df)))

    # Initial static plot setup
    ax.barh(df['Language'], df['Count'], color=colors, height=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(False)
    ax.set_title("Repos per Language", fontsize=20, fontweight='bold', pad=20)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_xlim(0, df['Count'].max() * 1.1)
    fig.tight_layout()

    # Create animation
    ani = animation.FuncAnimation(fig, update, frames=range(1, 31), fargs=(ax, df, colors), blit=False, interval=50)

    # The original script used 'ffmpeg', let's stick to that if 'imagemagick' is unavailable.
    try:
        ani.save('../cards/lang.gif', writer='imagemagick', dpi=100)
    except FileNotFoundError:
        print("imagemagick not found, falling back to ffmpeg.")
        ani.save('../cards/lang.gif', writer='ffmpeg', dpi=100)

if __name__=='__main__':
    main()