from os import path, listdir
from sys import argv
from time import sleep
import sass


SCSS_DIR = "./scss"
MAIN_SCSS_FILE = "./scss/style.scss"
OUTPUT_COMPONENT_FILE = "./form-vue/src/App.vue"
PERIOD = 3
PRINT_ERROR = False


def main():
    files_dict = dict()
    while True:
        new_files_set = set(paths_to_scss_files(SCSS_DIR))
        old_files_set = set(files_dict)
        if new_files_set != old_files_set:
            created_files = new_files_set - old_files_set
            removed_files = old_files_set - new_files_set

            for file_path in removed_files:
                del files_dict[file_path]
            for file_path in created_files:
                modification_time = path.getmtime(file_path)
                files_dict[file_path] = modification_time
            update_css()
        
        changes_happened = False

        for file_path in files_dict:
            old_modification_time = files_dict[file_path]
            new_modification_time = path.getmtime(file_path)
            if new_modification_time != old_modification_time:
                changes_happened = True
                files_dict[file_path] = new_modification_time
        
        if changes_happened:
            update_css()

        sleep(PERIOD)


def paths_to_scss_files(directory_path):
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
        if item_name.lower().endswith(".scss") and path.isfile(item_path):
            files.append(item_path)
        elif path.isdir(item_path):
            dirs.append(item_path)
    return files, dirs


def update_css():
    with open(MAIN_SCSS_FILE, "rt", encoding="utf-8") as file:
        content = file.read()
    try:
        css = sass.compile(string=content)
    except Exception:
        print("ERROR IN PROCESS OF COMPILATION")
        if PRINT_ERROR:
            css = sass.compile(string=content)
    else:
        with open(OUTPUT_COMPONENT_FILE, "rt", encoding="utf-8") as file:
            component_content = file.read()
        end_of_css_pos = component_content.rfind("</style>")
        if end_of_css_pos == -1:
            SyntaxError("Can't find </style> closing tag")
        start_of_css1 = component_content.rfind("<style>")
        start_of_css2 = component_content.rfind("<style scoped>")
        if start_of_css1 > start_of_css2:
            opening_tag = "<style>"
            tag_start = start_of_css1
        elif start_of_css1 < start_of_css2:
            opening_tag = "<style scoped>"
            tag_start = start_of_css2
        elif start_of_css1 == start_of_css2:
            raise SyntaxError("Can't find <style> or <style scoped> tag")
        else:
            raise SyntaxError("Undefined parsing error")
        true_css_start = tag_start + len(opening_tag)
        new_component_content = (component_content[0:true_css_start] + 
                                 "\n\n" + css + "\n</style>")
        with open(OUTPUT_COMPONENT_FILE, "wt", encoding="utf-8") as file:
            file.write(new_component_content)
        print("Component updated successfully!")


if __name__ == '__main__':
    if "-p" in argv or "--print" in argv:
        PRINT_ERROR = True
    main()
