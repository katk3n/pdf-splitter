import sys
import os
import csv
import pypdf


def run(path_to_pdf, path_to_toc, path_to_output):
    """
    format of the csv:
    --------
    No,Title,Page
    0,__OFFSET_IN__,<number of pages before the first tune>
    0,__OFFSET_OUT__,<number of pages after the last tune>
    1,"<title of the tune>",<starting page of the tune>
    2,"<title of the tune>",<starting page of the tune>
    ...
    --------
    """
    # number of pages before the first tune
    offset_in = 0

    # number of pages after the last tune
    offset_out = 0

    # list of dictionaries with format:
    # {'No': '<tune No>', 'Title': '<title of the tune>', 'Page': '<starting page of the tune>'}
    tunes = list()

    with open(path_to_toc, newline="") as toc:
        toc_reader = csv.DictReader(toc, delimiter=",", quotechar='"')
        for tune in toc_reader:
            if tune["Title"] == "__OFFSET_IN__":
                offset_in = int(tune["Page"])
                continue

            if tune["Title"] == "__OFFSET_OUT__":
                offset_out = int(tune["Page"])
                continue

            tunes.append(tune)

    os.makedirs(path_to_output, exist_ok=True)
    pdf_reader = pypdf.PdfReader(path_to_pdf)

    for i in range(len(tunes)):
        # the printed page number starts from 1, so we need "-1" to access the page from PdfReader.
        page_start = int(tunes[i]["Page"]) + offset_in - 1
        page_end = (
            int(tunes[i + 1]["Page"]) + offset_in - 1
            if i < len(tunes) - 1
            else len(pdf_reader.pages) - offset_out  # for the last page
        )

        writer = pypdf.PdfWriter()
        for page in range(page_start, page_end):
            writer.add_page(pdf_reader.pages[page])

        # format of the filenale: <No>-<tune>.pdf
        # if the tune contains '/', replace to '_'.
        filename = "-".join([tunes[i]["No"], tunes[i]["Title"], ".pdf"]).replace(
            "/", "_"
        )
        writer.write(os.path.join(path_to_output, filename))
        print(f"wrote {filename}")

    print("The split successfully completed!")


if __name__ == "__main__":
    path_to_pdf = sys.argv[1]
    path_to_toc = sys.argv[2]
    path_to_output = sys.argv[3]
    run(path_to_pdf, path_to_toc, path_to_output)
