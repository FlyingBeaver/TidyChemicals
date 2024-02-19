from os import path, listdir


EXTENSIONS = {"vue", "css", "scss", "sass"}


def main():
    dir_path = input("Enter folder path:\n").strip()
    string_to_find = input("Enter string to find:\n").strip()
    paths = paths_to_files(dir_path)
    files_where_found = dict()
    for path_ in paths:
        with open(path_, "rt", encoding="utf-8") as file:
            content = file.read()
            if string_to_find in content:
                line_no = find_in_content(content, string_to_find)
                files_where_found[path_] = line_no
            else:
                continue
    if len(files_where_found) == 0:
        print("String was not found!")
    else:
        print_report(files_where_found, string_to_find)


def paths_to_files(directory_path):
    files, dirs = separate(directory_path)
    while dirs:
        dir_to_process = dirs.pop()
        new_files, new_dirs = separate(dir_to_process)
        files.extend(new_files)
        dirs.extend(new_dirs)
    return files


def separate(directory_path):
    common_list = listdir(directory_path)
    files = []
    dirs = []
    for item_name in common_list:
        item_path = path.join(directory_path, item_name)
        if has_right_extension(item_name) and path.isfile(item_path):
            files.append(item_path)
        elif path.isdir(item_path):
            dirs.append(item_path)
    return files, dirs


def has_right_extension(name):
    extension = name.lower().split(".")[-1]
    return extension in EXTENSIONS


def find_in_content(content, string_to_find):
    list_of_lines = content.split("\n")
    numbers_list = []

    for number, line in enumerate(list_of_lines):
        if string_to_find in line:
            numbers_list.append(number + 1)
    if len(numbers_list) == 1:
        return numbers_list[0]
    elif len(numbers_list) == 0:
        return None
    else:
        return numbers_list


def print_report(files_where_found, string_to_find):
    print("############")
    print(f"String '{string_to_find}' was found in these files:")
    for path_, line_no in files_where_found.items():
        if isinstance(line_no, list):
            plural = "s"
            line_numbers = ", #".join(list(map(str, line_no)))
        else:
            plural = ""
            line_numbers = line_no
        print(f"File '{path.basename(path_)}', line{plural} #{line_numbers}")
    print("############")


if __name__ == '__main__':
    main()
