"""GitHub Cards - Repository language distribution donut chart."""

from __future__ import annotations

from collections import Counter

from matplotlib.animation import FuncAnimation

from utils import (
    BG_COLOR,
    SUBTEXT_COLOR,
    TEXT_COLOR,
    consolidate_small,
    fetch_repos,
    get_colors,
    read_username,
    save_animation,
    setup_figure,
)


def extract_languages(repos: list[dict]) -> tuple[list[str], list[int]]:
    """Extract language counts from repos, sorted by count descending."""
    counts: Counter[str] = Counter()
    for repo in repos:
        lang = repo.get("language")
        if lang is not None:
            counts[lang] += 1

    sorted_items = counts.most_common()
    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]
    return labels, values


def create_animation(
    labels: list[str],
    values: list[int],
    total_langs: int,
) -> FuncAnimation:
    """Build a rotating donut chart animation."""
    fig, ax = setup_figure(figsize=(6, 6))
    colors = get_colors(len(labels))

    def update(frame: int) -> None:
        ax.cla()
        ax.set_facecolor(BG_COLOR)

        ax.pie(
            values,
            labels=labels,
            autopct=lambda p: f"{p:.1f}%" if p >= 5 else "",
            startangle=frame * 3,
            colors=colors,
            wedgeprops=dict(width=0.4, edgecolor=BG_COLOR, linewidth=2),
            textprops=dict(color=TEXT_COLOR, fontsize=9),
        )

        ax.text(
            0, 0.05, str(total_langs),
            ha="center", va="center",
            fontsize=28, fontweight="bold", color=TEXT_COLOR,
        )
        ax.text(
            0, -0.12, "langs",
            ha="center", va="center",
            fontsize=10, color=SUBTEXT_COLOR,
        )

        ax.set_title(
            "Languages",
            color=TEXT_COLOR, fontsize=16, fontweight="bold", pad=20,
        )

    ani = FuncAnimation(fig, update, frames=72, interval=80)
    fig.tight_layout()
    return ani


def main() -> None:
    """Generate the animated language donut chart."""
    username = read_username()
    repos = fetch_repos(username)

    labels, values = extract_languages(repos)
    total_langs = len(labels)
    labels, values = consolidate_small(labels, values)

    ani = create_animation(labels, values, total_langs)
    save_animation(ani, "lang.gif")


if __name__ == "__main__":
    main()
