from pathlib import Path
import numpy as np
import pandas as pd

ORDER = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
PERCENT_COLS = ['p1_win%_tricks', 'tricks_tie%', 'p1_win%_cards', 'cards_tie%']

def _percent_remove(s: str) -> float:
    return float(str(s).strip().replace('%', ''))

def create_heatmap_arrays(output_csv: str, out_dir: str) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(output_csv)

    for c in PERCENT_COLS:
        df[c] = df[c].map(_percent_remove)

    tricks_win = (df.pivot(columns='p1_pattern', index='p2_pattern', values='p1_win%_tricks').reindex(index=ORDER, columns=ORDER).to_numpy())
    cards_win = (df.pivot(columns='p1_pattern', index='p2_pattern', values='p1_win%_cards').reindex(index=ORDER, columns=ORDER).to_numpy())
    tricks_draw = (df.pivot(columns='p1_pattern', index='p2_pattern', values='tricks_tie%').reindex(index=ORDER, columns=ORDER).to_numpy())
    cards_draw = (df.pivot(columns='p1_pattern', index='p2_pattern', values='cards_tie%').reindex(index=ORDER, columns=ORDER).to_numpy())

    np.save(out_dir / 'tricks_win.npy', tricks_win)
    np.save(out_dir / 'tricks_draw.npy', tricks_draw)
    np.save(out_dir / 'cards_win.npy', cards_win)
    np.save(out_dir / 'cards_draw.npy', cards_draw)