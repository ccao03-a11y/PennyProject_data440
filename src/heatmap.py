import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ORDER = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

def _make_labels(win: np.ndarray, tie: np.ndarray) -> np.ndarray:
    # turn NaN into 0.0
    win2 = np.nan_to_num(win, nan=0.0)
    tie2 = np.nan_to_num(tie, nan=0.0)
    # round to the neareast integer
    w = np.rint(win2).astype(int)
    t = np.rint(tie2).astype(int)

    labels = np.full(win.shape,"", dtype=object)

    rows, cols = win.shape
    for i in range(rows):
        for j in range(cols):
            # leave blank if choices are the same
            if i != j:
                labels[i, j] = f"{w[i, j]}({t[i, j]})"
    return labels

cmap = plt.cm.Blues.copy()
cmap.set_bad(color="#C4C4C4")

def plot_heatmap(win: np.ndarray, tie: np.ndarray, title: str, out_path: Path) -> None:
    plt.figure(figsize=(8, 8))
    labels = _make_labels(win, tie)
    ax = sns.heatmap(
        win,
        cmap=cmap,
        xticklabels=ORDER,
        yticklabels=ORDER,
        annot=labels,
        fmt="",
        linewidths=0.5,
        cbar=False
    )
    ax.set_title(title)
    ax.set_xlabel("My Choice")
    ax.set_ylabel("Opponent Choice")
    plt.savefig(out_path.with_suffix(".svg"))
    plt.close()

def plot_heatmaps(array_dir: str, out_dir: str, n_total: int) -> None:
    array_dir = Path(array_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    tricks_win = np.load(array_dir / "tricks_win.npy")
    tricks_tie = np.load(array_dir / "tricks_draw.npy")
    cards_win = np.load(array_dir / "cards_win.npy")
    cards_tie = np.load(array_dir / "cards_draw.npy")

    plot_heatmap(
        tricks_win,
        tricks_tie,
        f"My Chance of Win(Draw)\nby Tricks\nN={n_total:,}",
        out_dir / "heatmap_by_tricks.svg"
    )

    plot_heatmap(
        cards_win,
        cards_tie,
        f"My Chance of Win(Draw)\nby Cards\nN={n_total:,}",
        out_dir / "heatmap_by_cards.svg"
    )