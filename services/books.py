import csv


def parse_answers(csv_file_path):
    results = []
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            results.append({
                "book_id": int(row["book_id"]),
                "file_id": row["file_id"]
            })
    return results


book_datas = []

book_ids = []
