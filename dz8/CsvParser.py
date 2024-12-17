import csv

def parse_csv(path : str):
    with open(path, 'r') as csv_file:

        csv_reader = csv.reader(csv_file)
        next(csv_file)

        for row in csv_reader:
            #Указываем ФИО.
            result = f"Пользователь {row[0]}"

            #Указываем пол человека.
            if row[3].lower() == "female":
                result += " женского пола,"
            elif row[3].lower() == "male":
                result += " мужского пола,"
            else:
                result += " пол не указан,"

            #Указываем возраст.
            result += f" {row[4]} лет"

            #Указываем покупку.
            if row[3].strip().lower() == "female":
                result += f" совершила покупку на {row[5]} у.е."
            elif row[3].strip().lower() == "male":
                result += f" совершил покупку на {row[5]} у.е."
            else:
                result += f" совершил(а) покупку на {row[5]} у.е."

            #Указываем браузер и тип устройства.
            if row[1].strip().lower() == "mobile" or row[1].strip().lower() == "tablet":
                result += f" с мобильного браузера {row[2]}."
            elif row[1].strip().lower() == "laptop" or row[1].strip().lower() == "desktop":
                result += f" с десктопного браузера {row[2]}."
            else:
                result += f" с браузера {row[2]}"

            if row[6].strip().lower() == "" or row[6].strip().lower() == "-" or row[6].strip().lower() == "_":
                result += " Регион, из которого совершалась покупка: не указан."
            else:
                result += f" Регион, из которого совершалась покупка: {row[6]}."

            save_data_to_file(result)

def save_data_to_file(row : str = "", file : str = "Результат.txt"):
    with open(file, "a") as f:
        f.write(f"{row}\n")

def main():
    path = input("Введите путь к файлу: ")

    parse_csv(path)

main()