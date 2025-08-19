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
    Name, Size = [], []
    if repos.status_code == 200:
        j = repos.json()
        for i in range(len(j)):
            Name.append(j[i]["name"])
            Size.append(j[i].get("size", 0))
    return Name, Size

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
    ax.cla() # Clear the axis

    # Calculate current width of bars for this frame
    current_widths = df['Size'] * frame / 30

    # Redraw the bars
    bars = ax.barh(df['Name'], current_widths, color=colors, height=0.6)

    # Redraw the styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(False)
    ax.set_title("Top Size Repos", fontsize=20, fontweight='bold', pad=20)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_xlim(0, df['Size'].max() * 1.1)
    fig = plt.gcf()
    fig.tight_layout()

    # Redraw the value labels
    for bar in bars:
        width = bar.get_width()
        if width > 0:
            size_kb = width
            label = f'{int(size_kb)} KB'
            if size_kb > 1024:
                size_mb = size_kb / 1024
                label = f'{size_mb:.1f} MB'

            label_x_pos = width + (df['Size'].max() * 0.01)
            ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, label,
                    va='center', ha='left', fontsize=12, fontweight='bold')
    return ax,

def main():
    with open('../username.txt', 'r') as f:
        user = f.read().strip()

    Name, Size = getRepo(user)
    Name, Size = format(Name, Size)

    if not Name:
        print("No repo data to generate chart.")
        return

    df = pd.DataFrame({'Name': Name, 'Size': Size})
    df = df.sort_values(by='Size', ascending=False).reset_index(drop=True)
    df = df.iloc[::-1] # Invert order for horizontal bar chart

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 8))

    if df.empty or df['Size'].max() == 0:
        print("DataFrame is empty or all sizes are zero, cannot generate chart.")
        return

    cmap = plt.get_cmap('plasma')
    colors = cmap(np.linspace(0.1, 0.9, len(df)))

    # Initial static plot setup
    ax.barh(df['Name'], df['Size'], color=colors, height=0.6)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(False)
    ax.set_title("Top Size Repos", fontsize=20, fontweight='bold', pad=20)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_tick_params(labelsize=12)
    ax.set_xlim(0, df['Size'].max() * 1.1)
    fig.tight_layout()

    ani = animation.FuncAnimation(fig, update, frames=range(1, 31), fargs=(ax, df, colors), blit=False, interval=50)

    try:
        ani.save('../cards/top.gif', writer='imagemagick', dpi=100)
    except FileNotFoundError:
        print("imagemagick not found, falling back to ffmpeg.")
        ani.save('../cards/top.gif', writer='ffmpeg', dpi=100)

if __name__=='__main__':
    main()