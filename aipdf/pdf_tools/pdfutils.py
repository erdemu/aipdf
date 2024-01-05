from PyPDF2 import PdfReader
from io import BufferedReader


def read_whole_text(pdf_file: BufferedReader):
    """
    Reads the whole text from a PDF file.

    Parameters:
    ----------
    pdf_file: BufferedReader
        The PDF file that is read.

    Returns:
    ----------
    str
        The text that is extracted from the PDF file.
    """
    reader = PdfReader(pdf_file)
    text_pages = []

    for page in reader.pages:
        text_pages.append(page.extract_text())

    # Concatenate all the text pages into a single string
    text_pages = "".join(text_pages)

    return text_pages


def split_text_into_sections(text: str, section_headers: list):
    """
    Splits the text into sections using the section headers.

    Parameters:
    ----------

    text: str
        The text that is split into sections.
    section_headers: list
        The section headers that are used to split the text.

    Returns:
    ----------
    dict of str, str
        The sections that are extracted from the text.
    """
    sections = dict()

    for i in range(len(section_headers)):
        if i < len(section_headers) - 1:
            first_division = text.split(section_headers[i])[1]
            second_division = first_division.split(section_headers[i + 1])[0]
            sections[section_headers[i]] = second_division
        else:
            first_division = text.split(section_headers[i])[1]
            sections[section_headers[i]] = first_division

    return sections
