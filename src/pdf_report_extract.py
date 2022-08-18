from typing import Any

import PyPDF2


def extract_text_from_pdf(fp: str) -> 'list[str]':
    pdfFileObj = open(fp, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    if(pdfReader.numPages != 1):
        raise IOError(f'Expected number of pages is 1, got {pdfReader.numPages}')
    pageObj = pdfReader.getPage(0)
    # extracting text from page
    page_text = pageObj.extractText().split('\n')
    # closing the pdf file object
    pdfFileObj.close()
    # To debug, uncomment the bit below
    # for i, row in enumerate(page_text):
    #     print(i, row)
    return page_text


def get_data_from_pdf_text(text: 'list[str]') -> 'dict[str, Any]':
    if len(text) != 67:
        raise IOError('The text format differs to the trial doc')
    farm_name = text[1]
    lat_lng = [float(val) for val in text[4].split(',')]
    date = text[8][len('Date :'):].strip()
    field_name = text[10][len('Field Name :'):].strip()

    # data fields
    organic_carbon = float(text[24])
    tot_nitrogen = float(text[29])
    clay = float(text[34])
    pH = float(text[39])

    return {
        'date': date,
        'lng': lat_lng[1],
        'lat': lat_lng[0],
        'farm_name': farm_name,
        'field_name': field_name,
        'organic_carbon': organic_carbon,
        'tot_nitrogen': tot_nitrogen,
        'clay': clay,
        'pH': pH
    }
