![GitHub last commit](https://img.shields.io/github/last-commit/yuhi-sa/github_cards)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/yuhi-sa/github_cards)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/yuhi-sa/github_cards)
![GitHub top language](https://img.shields.io/github/languages/top/yuhi-sa/github_cards)
![GitHub language count](https://img.shields.io/github/languages/count/yuhi-sa/github_cards)

# GitHub Cards

GitHub のプロフィールに載せるリポジトリ情報の可視化カード。
ダークテーマのモダンなドーナツチャートで、言語分布とリポジトリサイズを表示します。

<img src="https://github.com/yuhi-sa/github_cards/blob/master/cards/lang.gif?raw=true" width="48%"> <img src="https://github.com/yuhi-sa/github_cards/blob/master/cards/top.gif?raw=true" width="48%">

## How to Use

1. このリポジトリを fork する
2. [`username.txt`](username.txt) を自身のユーザー名に書き換える
3. GitHub Actions を起動 (Run workflow)

<img width="80%" alt="Actions" src="https://user-images.githubusercontent.com/62089243/123906737-ae32c880-d9af-11eb-829e-449bbca0c27c.png">

> 一週間ごとに自動で更新されます

### プロフィール README に追加

`{username}` を自身のユーザー名に置き換えてください。

```markdown
<img src="https://github.com/{username}/github_cards/blob/master/cards/lang.gif?raw=true" width="48%">
<img src="https://github.com/{username}/github_cards/blob/master/cards/top.gif?raw=true" width="48%">
```

## Preview

### Repos per Language
![Repos per Language](/cards/lang.gif)

### Top Size Repos
![Top Size Repos](/cards/top.gif)
