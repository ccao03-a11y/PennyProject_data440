import os


POSSIBLE_CHOICES = ['000', '001', '010', '011', '100', '101', '110', '111']
SCORE_FIELDS = ['trick_ties', 'p1_trick_wins', 'p1_trick_loss', 'card_ties', 'p1_card_wins', 'p1_card_loss']



def create_score_table() -> dict:
    all_scores = {}
    for p1_choice in POSSIBLE_CHOICES:
        all_scores[p1_choice] = {}
        for p2_choice in POSSIBLE_CHOICES:
            if p1_choice == p2_choice:
                continue
            all_scores[p1_choice][p2_choice] = {field: 0 for field in SCORE_FIELDS}
    return all_scores



def get_result_row(deck: bytes, p1_choice: str, p2_choice: str) -> list:
    p1_tricks, p1_cards, p2_tricks, p2_cards = score_single_deck(deck, p1_choice, p2_choice)
    return [p1_choice, p2_choice, p1_tricks, p1_cards, p2_tricks, p2_cards]



def score_file(file_path: str) -> list:
    result_rows = []

    with open(file_path, 'rb') as file:
        deck = file.read(52)
        while deck:
            for p1_choice in POSSIBLE_CHOICES:
                for p2_choice in POSSIBLE_CHOICES:
                    if p1_choice == p2_choice:
                        continue
                    result_rows.append(get_result_row(deck, p1_choice, p2_choice))
            deck = file.read(52)

    return result_rows



def score_all_files(path_to_data: str, path_to_scores: str) -> None:
    all_scores = create_score_table()
    processed_any = False

    for file_name in os.listdir(path_to_data):
        if file_name.startswith('s'):
            continue
        processed_any = True

        file_path = os.path.join(path_to_data, file_name)
        file_results = score_file(file_path)
        merge_scores(file_results, all_scores)
        os.rename(file_path, os.path.join(path_to_data, 'scored_' + file_name))
    if processed_any:
        write_scores(path_to_scores, all_scores)



def score_single_deck(deck: bytes, p1_choice: str, p2_choice: str) -> tuple[int, int, int, int]:
    card_count = 0
    p1_tricks = 0
    p1_cards = 0
    p2_tricks = 0
    p2_cards = 0

    first_card = None
    second_card = None

    for third_card in deck:
        card_count += 1

        if first_card is None:
            first_card = third_card
            continue

        if second_card is None:
            second_card = third_card
            continue

        current_pattern = f'{first_card}{second_card}{third_card}'

        if current_pattern == p1_choice:
            p1_tricks += 1
            p1_cards += card_count
            card_count = 0
            first_card = None
            second_card = None
            continue

        if current_pattern == p2_choice:
            p2_tricks += 1
            p2_cards += card_count
            card_count = 0
            first_card = None
            second_card = None
            continue

        first_card = second_card
        second_card = third_card

    return p1_tricks, p1_cards, p2_tricks, p2_cards



def merge_scores(results: list, score_table: dict) -> dict:
    for result in results:
        p1_choice = result[0]
        p2_choice = result[1]
        p1_tricks = result[2]
        p1_cards = result[3]
        p2_tricks = result[4]
        p2_cards = result[5]

        if p1_tricks == p2_tricks:
            score_table[p1_choice][p2_choice]['trick_ties'] += 1
        elif p1_tricks > p2_tricks:
            score_table[p1_choice][p2_choice]['p1_trick_wins'] += 1
        else:
            score_table[p1_choice][p2_choice]['p1_trick_loss'] += 1

        if p1_cards == p2_cards:
            score_table[p1_choice][p2_choice]['card_ties'] += 1
        elif p1_cards > p2_cards:
            score_table[p1_choice][p2_choice]['p1_card_wins'] += 1
        else:
            score_table[p1_choice][p2_choice]['p1_card_loss'] += 1

    return score_table



def write_scores(path: str, scores: dict) -> None:
    extracted_fields = [field for field in scores['000']['001']]
    header = 'p1_choice, p2_choice, ' + ', '.join(extracted_fields)

    output_lines = []
    for p1_choice in scores:
        for p2_choice in scores[p1_choice]:
            row_items = [p1_choice, p2_choice]
            for field in scores[p1_choice][p2_choice]:
                row_items.append(str(scores[p1_choice][p2_choice][field]))
            output_lines.append(','.join(row_items))

    with open(path, 'w') as file:
        file.write(header + '\n')
        file.write('\n'.join(output_lines) + '\n')

