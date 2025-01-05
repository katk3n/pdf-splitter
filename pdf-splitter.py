import sys
import os
import csv
import pypdf


def run(path_to_pdf, path_to_toc, path_to_output):
    """
    format of the csv:
    --------
    Title,Page
    __OFFSET_IN__,<number of pages before the first section>
    __OFFSET_OUT__,<number of pages after the last section>
    "<title of the section>",<starting page of the section>
    "<title of the section>",<starting page of the section>
    ...
    --------
    """
    # number of pages before the first section
    offset_in = 0

    # number of pages after the last section
    offset_out = 0

    # list of dictionaries with format:
    # {'Title': '<title of the section>', 'Page': '<starting page of the section>'}
    sections = list()

    with open(path_to_toc, newline="") as toc:
        toc_reader = csv.DictReader(toc, delimiter=",", quotechar='"')
        for section in toc_reader:
            if section["Title"] == "__OFFSET_IN__":
                offset_in = int(section["Page"])
                continue

            if section["Title"] == "__OFFSET_OUT__":
                offset_out = int(section["Page"])
                continue

            sections.append(section)

    os.makedirs(path_to_output, exist_ok=True)
    pdf_reader = pypdf.PdfReader(path_to_pdf)

    for i in range(len(sections)):
        # the printed page number starts from 1, so we need "-1" to access the page from PdfReader.
        page_start = int(sections[i]["Page"]) + offset_in - 1
        page_end = (
            int(sections[i + 1]["Page"]) + offset_in - 1
            if i < len(sections) - 1
            else len(pdf_reader.pages) - offset_out  # for the last page
        )

        # in case 2 sections are on the same page
        if page_end == page_start:
            page_end = page_start

        writer = pypdf.PdfWriter()
        for page in range(page_start, page_end):
            writer.add_page(pdf_reader.pages[page])

        # format of the filenale: <No>-<title>.pdf
        # if the section contains '/', replace to '_'.
        filename = "-".join([str(i + 1), sections[i]["Title"], ".pdf"]).replace(
            "/", "_"
        )
        writer.write(os.path.join(path_to_output, filename))
        print(f"wrote {filename}")

    print("The split successfully completed!")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f""" Usage: {sys.argv[0]} [path_to_pdf.pdf] [path_to_toc.csv] [path_to_output/]
    path_to_pdf.pdf: path to the pdf to split
    path_to_toc.csv: path to the table of contents of the pdf in csv format
    path_to_output/: output directory for the splitted pdf files

    format of the csv:
    --------
    Title,Page
    __OFFSET_IN__,<number of pages before the first section>
    __OFFSET_OUT__,<number of pages after the last section>
    "<title of the section>",<starting page of the section>
    "<title of the section>",<starting page of the section>
    ...
    --------
              """)
        sys.exit(1)

    path_to_pdf = sys.argv[1]
    path_to_toc = sys.argv[2]
    path_to_output = sys.argv[3]
    run(path_to_pdf, path_to_toc, path_to_output)
