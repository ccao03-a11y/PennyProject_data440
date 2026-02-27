from pathlib import Path

from src.deckGeneration import generate_decks
from src.scoring import score_all_files
from src.compileResult import compile_results

HALF_DECK_SIZE = 26
DECKS_PER_FILE = 10000
TOTAL_DECKS = 1000000
RANDOM_SEED = 42

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
SCORES_PATH = PROCESSED_DIR / 'scores.csv'
FINAL_OUTPUT_PATH = PROCESSED_DIR / 'output.csv'

def _additional_decks_prompt() -> int:
    s = input("Number of additional decks to generate: ").strip()
    if s == "":
        return 0
    try:
        n = int(s)
    except ValueError:
        return 0
    return n

def run_pipeline() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    additional = _additional_decks_prompt()

    print('generating decks...')
    if additional > 0:
        generate_decks(
            half_deck=HALF_DECK_SIZE,
            total_decks=additional,
            decks_per_file=DECKS_PER_FILE,
            data_dir=str(RAW_DIR),
            seed=RANDOM_SEED,
        )

    print('scoring...')
    score_all_files(path_to_data=str(RAW_DIR), path_to_scores=str(SCORES_PATH))

    print('compiling results...')
    compile_results(path_to_scores=str(SCORES_PATH), path_to_output=str(FINAL_OUTPUT_PATH))


if __name__ == '__main__':
    run_pipeline()
