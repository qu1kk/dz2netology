import json
import xml.etree.ElementTree as xmlTree

def xml_to_jsondict(root_data):
    result = {}

    for elem in root_data:
        if len(elem) > 0:
            value = xml_to_jsondict(elem)
        else:
            value = elem.text

        key = elem.tag

        if key in result:
            if not isinstance(result[key], list):
                result[key] = [result[key]]
            result[key].append(value)
        else:
            result[key] = value

    return result


def convert_file(file_path : str):
    file_path_arr = file_path.split('.')

    file = open(file_path, 'r')

    if file_path_arr[-1] == 'json':
        print("TODO")
    elif file_path_arr[-1] == 'xml':
        root = xmlTree.fromstring(file.read().strip())
        json_data = json.dumps(xml_to_jsondict(root))

        new_file = open(f"result.json", 'w')
        new_file.write(json_data)
    elif file_path_arr[-1] == 'yml' or file_path_arr[-1] == 'yaml':
        print("TODO")
    else:
        print("Неизвестный формат входного файла. Невозможно обработать.")

def main():
    file_path = input("Введите путь до файла: ")

    convert_file(file_path)

main()