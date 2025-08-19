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

    Name = []
    Size = []
    if repos.status_code == 200:

        j = repos.json()

        for i in range(len(j)):
            Name.append(j[i]["name"])
            # Some repos might not have a size, default to 0
            Size.append(j[i].get("size", 0))

    return Name, Size

def format(Name, Size):
    sumsum = sum(Size)
    if sumsum == 0:
        return Name, Size

    Name2 = []
    Size2 = []
    others = 0
    # Create a DataFrame to handle sorting and filtering easily
    df = pd.DataFrame({'Name': Name, 'Size': Size})
    df = df.sort_values(by='Size', ascending=False)

    # Take top 9, group the rest into "others"
    top_df = df.head(9)
    others_size = df.iloc[9:]['Size'].sum()

    Name2 = top_df['Name'].tolist()
    Size2 = top_df['Size'].tolist()

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
        print("No repository data to generate chart.")
        return

    df = pd.DataFrame({'Name': Name, 'Size': Size})
    df = df.sort_values(by='Size', ascending=True)

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 8))

    if df.empty or df['Size'].max() == 0:
        print("DataFrame is empty or all sizes are zero, cannot generate chart.")
        return

    cmap = plt.get_cmap('plasma')
    colors = cmap(df['Size'] / float(df['Size'].max()))

    bars = ax.barh(df['Name'], df['Size'], color=colors, height=0.6)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(False)

    ax.set_title("Top Size Repos", fontsize=20, fontweight='bold', pad=20)

    ax.xaxis.set_visible(False)
    ax.yaxis.set_tick_params(labelsize=12)

    for bar in bars:
        width = bar.get_width()
        # Format size in KB
        size_kb = width
        label = f'{int(size_kb)} KB'
        if size_kb > 1024:
            size_mb = size_kb / 1024
            label = f'{size_mb:.1f} MB'

        label_x_pos = width + (df['Size'].max() * 0.01)
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, label,
                va='center', ha='left', fontsize=12, fontweight='bold')

    fig.tight_layout()

    fig.savefig('../cards/top.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())

if __name__=='__main__':
    main()