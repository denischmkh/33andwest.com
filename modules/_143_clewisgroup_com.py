import requests
import pdfplumber

url = "https://img1.wsimg.com/blobby/go/fdfd814d-d08c-47e3-b4cd-77afd89ca8f9/CLG%20ROSTER%202025.pdf"
response = requests.get(url)

with open("file.pdf", "wb") as f:
    f.write(response.content)

with pdfplumber.open("file.pdf") as pdf:
    first_page = pdf.pages[0]

    words = first_page.extract_words()  # получаем слова с координатами
    left_column = []
    right_column = []

    for w in words:
        # x0 меньше 300 — левая колонка, больше или равно — правая
        if w['x0'] < 300:
            left_column.append((w['top'], w['text']))
        else:
            right_column.append((w['top'], w['text']))

    # сортируем по вертикали (top) и группируем строки
    def group_by_line(column):
        column.sort(key=lambda x: x[0])
        lines = []
        current_top = None
        current_line = []
        for top, text in column:
            if current_top is None or abs(top - current_top) < 5:  # считаем как одна строка
                current_line.append(text)
                current_top = top if current_top is None else current_top
            else:
                lines.append(" ".join(current_line))
                current_line = [text]
                current_top = top
        if current_line:
            lines.append(" ".join(current_line))
        return lines

    left_lines = group_by_line(left_column)
    right_lines = group_by_line(right_column)

    print("Левая колонка:")
    for line in left_lines:
        print(line)

    print("\nПравая колонка:")
    for line in right_lines:
        print(line)