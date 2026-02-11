"""GitHub Cards - 共通ユーティリティモジュール."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import requests

# GitHub Dark テーマカラー
BG_COLOR = "#0d1117"
TEXT_COLOR = "#e6edf3"
SUBTEXT_COLOR = "#8b949e"

# モダンなカラーパレット（GitHub / Vercel風）
PALETTE = [
    "#58a6ff",  # blue
    "#3fb950",  # green
    "#d29922",  # yellow
    "#f78166",  # orange
    "#bc8cff",  # purple
    "#ff7b72",  # red
    "#79c0ff",  # light blue
    "#56d364",  # light green
    "#e3b341",  # gold
    "#ffa657",  # light orange
    "#d2a8ff",  # light purple
    "#ffa198",  # pink
    "#a5d6ff",  # pale blue
    "#7ee787",  # pale green
    "#f2cc60",  # pale yellow
    "#ffdfb6",  # peach
]

BASE_DIR = Path(__file__).resolve().parent.parent


def read_username() -> str:
    """username.txt からGitHubユーザー名を読み込む."""
    return (BASE_DIR / "username.txt").read_text().strip()


def fetch_repos(username: str) -> list[dict[str, Any]]:
    """GitHub APIからユーザーの全リポジトリを取得する（ページネーション対応）."""
    url = f"https://api.github.com/users/{username}/repos"
    params = {"per_page": 100, "page": 1}
    all_repos: list[dict[str, Any]] = []

    while True:
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code != 200:
            break
        page = resp.json()
        if not page:
            break
        all_repos.extend(page)
        params["page"] += 1

    return all_repos


def get_colors(n: int) -> list[str]:
    """n 個のカラーをパレットから循環的に返す."""
    return [PALETTE[i % len(PALETTE)] for i in range(n)]


def setup_figure(figsize: tuple[float, float] = (6, 6)) -> tuple[plt.Figure, plt.Axes]:
    """ダークテーマの Figure / Axes を作成する."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    return fig, ax


def save_animation(
    ani: animation.FuncAnimation,
    filename: str,
    dpi: int = 120,
) -> None:
    """アニメーションを cards/ ディレクトリにGIF保存する."""
    output = BASE_DIR / "cards" / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    ani.save(str(output), writer="pillow", dpi=dpi)


def consolidate_small(
    labels: list[str],
    values: list[float],
    threshold: float = 0.05,
) -> tuple[list[str], list[float]]:
    """閾値以下の項目を 'Others' にまとめる."""
    total = sum(values)
    if total == 0:
        return labels, values

    new_labels: list[str] = []
    new_values: list[float] = []
    others = 0.0

    for label, value in zip(labels, values):
        if value / total < threshold:
            others += value
        else:
            new_labels.append(label)
            new_values.append(value)

    if others > 0:
        new_labels.append("Others")
        new_values.append(others)

    return new_labels, new_values
