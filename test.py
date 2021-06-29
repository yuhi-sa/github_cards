import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation

# github API overview
# https://docs.github.com/ja/rest/overview/endpoints-available-for-github-apps

root = "https://api.github.com/"
user = "yuhi-sa"

url = root + "users/" + user +"/repos"

# repos = requests.get(url)

# repoLang = []
# repoLangNum = []
# if repos.status_code == 200:
#     # json を取得
#     j = repos.json()
#     print(len(j))
#     for i in range(len(j)):
#         lang = j[i]["language"]

#         if lang in repoLang:
#             repoLangNum[repoLang.index(lang)] += 1
#         else:
#             repoLang.append(lang)
#             repoLangNum.append(1)
            

repoLang = ['Dockerfile', 'Python', 'HTML', None, 'Jupyter Notebook', 'Rust', 'MATLAB', 'JavaScript', 'CSS', 'Shell', 'TeX', 'C', 'TypeScript']
repoLangNum = [1, 10, 3, 3, 4, 1, 1, 1, 1, 1, 2, 1, 1]


# plt.pie(repoLangNum,counterclock=False , autopct=lambda f: '{:.1f}%'.format(f) if f > 5 else '')
# plt.legend(repoLang, bbox_to_anchor=(0.5, 1.175), loc="upper center", ncol = 5)
# plt.axis('equal')
# plt.tight_layout()
# plt.show()




def update(num,chocopie, a,b):
    if len(chocopie) > 0:
        ax.cla()
    
    chocopie,a,b, = ax.pie(repoLangNum, labels=repoLang, autopct='%1.1f%%',shadow=True, startangle=4*num ,colors=colors)
    
    ax.set_title("Repos per Language")

cm = plt.get_cmap("Set3")
colors = []
for i in range(len(repoLang)):
    colors.append(cm(i))

fig, ax = plt.subplots()    
chocopie,a,b, = ax.pie(repoLangNum, labels=repoLang, autopct='%1.1f%%',shadow=True, startangle=0,colors=colors)
ani = animation.FuncAnimation(fig, update, frames=91,fargs=[chocopie, a,b], interval=100)

dpi=100
ani.save('card.gif', writer="ffmpeg",dpi=dpi)

