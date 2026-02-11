"""GitHub Cards - Top Repos by Size (animated donut chart)."""

from __future__ import annotations

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


def extract_repo_data(repos: list[dict]) -> tuple[list[str], list[float], int]:
    """Extract repo names and sizes, sorted by size descending."""
    pairs = [(r["name"], r["size"]) for r in repos if r.get("size", 0) > 0]
    pairs.sort(key=lambda p: p[1], reverse=True)
    total_count = len(pairs)
    names = [p[0] for p in pairs]
    sizes = [float(p[1]) for p in pairs]
    names, sizes = consolidate_small(names, sizes, 0.05)
    return names, sizes, total_count


def create_animation(
    names: list[str],
    sizes: list[float],
    total_count: int,
) -> FuncAnimation:
    """Build a rotating donut chart animation."""
    fig, ax = setup_figure(figsize=(6, 6))
    colors = get_colors(len(names))

    def update(frame: int) -> None:
        ax.cla()
        ax.set_facecolor(BG_COLOR)

        ax.pie(
            sizes,
            labels=names,
            colors=colors,
            startangle=frame * 3,
            autopct=lambda p: f"{p:.1f}%" if p >= 2.5 else "",
            wedgeprops=dict(width=0.4, edgecolor=BG_COLOR, linewidth=2),
            textprops=dict(color=TEXT_COLOR, fontsize=9),
        )

        ax.text(
            0, 0.05, str(total_count),
            ha="center", va="center",
            fontsize=28, fontweight="bold", color=TEXT_COLOR,
        )
        ax.text(
            0, -0.12, "repos",
            ha="center", va="center",
            fontsize=10, color=SUBTEXT_COLOR,
        )

        ax.set_title(
            "Top Repos by Size",
            color=TEXT_COLOR, fontsize=16, fontweight="bold", pad=20,
        )

    ani = FuncAnimation(fig, update, frames=72, interval=80)
    fig.subplots_adjust(top=0.88)
    return ani


def main() -> None:
    """Generate animated donut chart of top repos by size."""
    username = read_username()
    repos = fetch_repos(username)
    names, sizes, total_count = extract_repo_data(repos)
    ani = create_animation(names, sizes, total_count)
    save_animation(ani, "top.gif")


if __name__ == "__main__":
    main()
