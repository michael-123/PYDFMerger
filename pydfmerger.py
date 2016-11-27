from PyPDF2 import PdfFileMerger
from os import listdir

page_entry_delimiter = ";"
from_to_delimiter = "-"
output_file = "XX_merge.pdf"


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def handle_pages(path):
    """
    Gets the page information of a PDF file
    :param path:
    :return:
    """
    pages_list = []

    # Check if there is page information
    if "[" in path and "]" in path:
        page_information = path[path.find("[") + 1:path.find("]")]
        page_entries = page_information.split(page_entry_delimiter)

        # Create "from to" tuple for every page entry
        for page_entry in page_entries:
            if page_entry is not "":
                from_to = page_entry.split(from_to_delimiter)
                from_page = num(from_to[0])
                to_page = num(from_to[1])
                pages_list.append((from_page, to_page))


    return pages_list


def handle_number(path):
    """
    Gets the leading number of a PDF file
    :param path:
    :return: number
    """
    return num(path[:path.find("_")])


def parse_file(path):
    """
    Parses a file path to receive merge information
    :param path:
    :return:
    """
    p = handle_pages(path)
    n = handle_number(path)
    return path, n, p


def main():
    # Read file list in root folder
    file_list = listdir(".")
    files = []
    for file in file_list:
        if file.endswith(".pdf") and not file == output_file:
            files.append(parse_file(file))

    # Sort file list
    files = sorted(files, key=lambda x: x[1])

    # Merge PDF files
    merger = PdfFileMerger()

    # Append PDF files
    for file in files:
        # If there is page information
        if file[2]:
            for information in file[2]:
                file_object = open(file[0], "rb")
                print(information)
                merger.append(fileobj=file_object, pages=(information[0]-1, information[1]))
        else:
            file_object = open(file[0], "rb")
            merger.append(fileobj=file_object)

    # Write merged PDF
    output = open(output_file, "wb")
    merger.write(output)

if __name__ == '__main__':
    main()
