from PyPDF2 import PdfReader


def extract_fontmap_from_pdf(pdf_file):
    """
    Extracts the different fonts of text from a PDF file.
    """

    reader = PdfReader(pdf_file)
    fonts = dict()

    def visitor_function(text, cm, tm, fontDict, fontsize):
        """
        This is a local function that is used to extract the fonts from the PDF file,
        and store them in a dictionary.
        pypdf2 has a visitor pattern, which is used here.
        for details, see: https://pypdf2.readthedocs.io/en/3.0.0/user/extract-text.html#using-a-visitor

        Parameters:
        ----------
        text: str
            The text that is extracted from the PDF file.
        cm: list
            The current transformation matrix.
        tm: list
            The text matrix.
        fontDict: dict
            The font dictionary.
        fontsize: float
            The font size.
        """
        if fontDict and fontsize and not text.isspace():
            if fontDict["/BaseFont"] in fonts:
                fonts[fontDict["/BaseFont"]]["fontsizes"].add(fontsize)
            else:
                fonts[fontDict["/BaseFont"]] = dict()
                fonts[fontDict["/BaseFont"]]["fontsizes"] = set()
                fonts[fontDict["/BaseFont"]]["texts"] = dict()
                fonts[fontDict["/BaseFont"]]["fontsizes"].add(fontsize)

            if fontsize in fonts[fontDict["/BaseFont"]]["texts"].keys():
                fonts[fontDict["/BaseFont"]]["texts"][fontsize].append(text)
            else:
                fonts[fontDict["/BaseFont"]]["texts"][fontsize] = []
                fonts[fontDict["/BaseFont"]]["texts"][fontsize].append(text)

    for page in reader.pages:
        page.extract_text(visitor_text=visitor_function)

    return fonts
