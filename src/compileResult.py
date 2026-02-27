import csv
from typing import Dict

RAW_COLUMNS = [
    'p1_choice', 'p2_choice',
    'trick_ties', 'p1_trick_wins', 'p1_trick_loss',
    'card_ties', 'p1_card_wins', 'p1_card_loss'
]

FINAL_COLUMNS = [
    'p1_pattern', 'p2_pattern',
    'p1_choice', 'p2_choice',
    'p1_win%_tricks', 'p2_win%_tricks', 'tricks_tie%',
    'p1_win%_cards', 'p2_win%_cards', 'cards_tie%',
    'tricks_total', 'cards_total'
]


COLOR_LOOKUP = {
    '0': 'R',
    '1': 'B'
}


def normalize_choice(value: str) -> str:
    return str(value).strip().zfill(3)[:3]



def pattern_label(choice: str) -> str:
    clean_choice = normalize_choice(choice)
    return ''.join(COLOR_LOOKUP[digit] for digit in clean_choice)



def to_int(value: str) -> int:
    text = str(value).strip()
    if text == '':
        return 0
    return int(float(text))



def format_percent(part: int, whole: int) -> str:
    if whole == 0:
        return '0.0000%'
    return f'{part / whole * 100:.4f}%'



def build_output_row(row: Dict[str, str]) -> Dict[str, str]:
    p1_choice = normalize_choice(row['p1_choice'])
    p2_choice = normalize_choice(row['p2_choice'])

    trick_ties = to_int(row['trick_ties'])
    p1_trick_wins = to_int(row['p1_trick_wins'])
    p1_trick_loss = to_int(row['p1_trick_loss'])
    card_ties = to_int(row['card_ties'])
    p1_card_wins = to_int(row['p1_card_wins'])
    p1_card_loss = to_int(row['p1_card_loss'])

    total_tricks = trick_ties + p1_trick_wins + p1_trick_loss
    total_cards = card_ties + p1_card_wins + p1_card_loss

    return {
        'p1_pattern': pattern_label(p1_choice),
        'p2_pattern': pattern_label(p2_choice),
        'p1_choice': p1_choice,
        'p2_choice': p2_choice,
        'p1_win%_tricks': format_percent(p1_trick_wins, total_tricks),
        'p2_win%_tricks': format_percent(p1_trick_loss, total_tricks),
        'tricks_tie%': format_percent(trick_ties, total_tricks),
        'p1_win%_cards': format_percent(p1_card_wins, total_cards),
        'p2_win%_cards': format_percent(p1_card_loss, total_cards),
        'cards_tie%': format_percent(card_ties, total_cards),
        'tricks_total': str(total_tricks),
        'cards_total': str(total_cards),
    }



def compile_results(path_to_scores: str, path_to_output: str) -> None:
    with open(path_to_scores, 'r', newline='', encoding='utf-8') as source_file:
        reader = csv.DictReader(source_file, skipinitialspace=True)

        if reader.fieldnames is None:
            raise RuntimeError('scores.csv is empty.')

        cleaned_names = [name.strip() for name in reader.fieldnames if name is not None]
        if cleaned_names != RAW_COLUMNS:
            raise ValueError(f'Unexpected columns: {cleaned_names}')

        with open(path_to_output, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=FINAL_COLUMNS)
            writer.writeheader()

            for row in reader:
                if not any(str(value).strip() for value in row.values()):
                    continue
                writer.writerow(build_output_row(row))
