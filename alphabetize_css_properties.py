"""
css properties sorting module
"""
import os
import sys
import re

#PROCESSING_TARGET CAN BE FILE OR DIRECTORY
#ACCEPTED AS CALLING ARGUMENT
PROCESSING_TARGET = "." if (len(sys.argv) < 2) else sys.argv[1]
FILE_EXT = ".css"
TEXT_BUFFER = []
PROPERTY_REGEX = r"^@?[a-zA-Z0-9\-]+:[#a-zA-Z0-9\s%\"\',\(\)\.\-]+;$"

def get_css_files(target):
    """get all css files in a directory"""
    css_files = []
    if target.endswith(FILE_EXT):
        css_files.append(target)
    else:
        dir_content = os.listdir(target)
        for file in dir_content:
            if file.endswith(FILE_EXT):
                css_files.append(file)
    return css_files


def write_alphabetized_css(line, new_file):
    """write lines in buffer"""
    if re.match(PROPERTY_REGEX, line.strip()) is not None:
        TEXT_BUFFER.append(line)
    elif line.strip() == "}" and len(TEXT_BUFFER) is not 0:
        TEXT_BUFFER.sort()
        TEXT_BUFFER.append(line)
        for sorted_line in TEXT_BUFFER:
            new_file.write(bytes(sorted_line, "UTF-8"))
        TEXT_BUFFER.clear()
    else:
        new_file.write(bytes(line, "UTF-8"))


def process_css_file(file_path):
    """process text from css document"""
    print("Processing %s..." % file_path)
    new_file = open(file_path.replace(".css", "-alphabetized.css"), "wb")
    with open(file_path, "r") as css_doc:
        for line in css_doc:
            write_alphabetized_css(line, new_file)


try:
    FILES = get_css_files(PROCESSING_TARGET)
    for FILE in FILES:
        process_css_file(FILE)
        print("File %s has properties alphabetized.")
    print("Script finished.")

except FileNotFoundError:
    print("No such file or directory.")
except PermissionError:
    print("Cannot execute script; do not have permission.")
