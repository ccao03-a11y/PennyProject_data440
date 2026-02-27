import os
import numpy as np
import re

_BIN_RE = re.compile(r"^(?:scored_)?bytes_(\d+)_d+\.bin$")

def new_batch_index(data_dir: str) -> int:
    max_idx = 0
    for name in os.listdir(data_dir):
        m = _BIN_RE.match(name)
        if m:
            max_idx = max(max_idx, int(m.group(1)))
    return max_idx + 1

def build_base_deck(half_deck: int) -> np.ndarray:
    first_half = np.zeros(shape=half_deck, dtype='u1')
    second_half = np.ones(shape=half_deck, dtype='u1')
    return np.concatenate((first_half, second_half))



def save_deck_batch(deck_batch: list, batch_index: int, data_dir: str) -> None:
    batch_bytes = np.array(deck_batch).tobytes()
    file_name = f'bytes_{batch_index}_{len(deck_batch)}.bin'
    file_path = os.path.join(data_dir, file_name)

    with open(file_path, 'wb') as file:
        file.write(batch_bytes)



def generate_decks(half_deck: int, total_decks: int, decks_per_file: int, data_dir: str, seed: int = 42) -> None:
    if total_decks < decks_per_file:
        decks_per_file = total_decks

    rng = np.random.default_rng(seed)
    base_deck = build_base_deck(half_deck)
    file_count = int(np.ceil(total_decks / decks_per_file))
    start_idx = new_batch_index(data_dir)

    for batch_index in range(file_count):
        deck_batch = []
        remaining_decks = total_decks - batch_index * decks_per_file
        current_batch_size = min(decks_per_file, remaining_decks)

        for _ in range(current_batch_size):
            shuffled_deck = base_deck.copy()
            rng.shuffle(shuffled_deck)
            deck_batch.append(shuffled_deck)
        
        save_deck_batch(deck_batch, start_idx + batch_index, data_dir)
