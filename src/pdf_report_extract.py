from typing import Any

import PyPDF2


def extract_text_from_pdf(fp: str) -> 'list[str]':
    pdfFileObj = open(fp, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    if pdfReader.numPages not in [1, 2]:
        raise IOError(f'Expected number of pages is 1, got {pdfReader.numPages}')
    if pdfReader.numPages == 2:
        print(f'File {fp} is a double pager - assuming 2nd page is duplicate')
    pageObj = pdfReader.getPage(0)
    # extracting text from page
    page_text = pageObj.extractText().split('\n')
    # closing the pdf file object
    pdfFileObj.close()
    # To debug, uncomment the bit below
    # for i, row in enumerate(page_text):
    #     print(i, row)
    return page_text


def values_from_pdf_using_keyword_lookup(text: 'list[str]'):
    try:
        farm_name = text[1]
        lat_lng = [float(val) for val in text[4].split(',')]

        date_string = [item for item in text if item.startswith('Date')][0]
        date = date_string[len('Date :'):].strip()

        field_name_string = [item for item in text if item.startswith('Field Name')][0]
        field_name = field_name_string[len('Field Name :'):].strip()

        # data fields
        organic_carbon = float(text[text.index('Organic Carbon') + 2])
        tot_nitrogen = float(text[text.index('Total Nitrogen') + 2])
        clay = float(text[text.index('Clay') + 2])
        ph = float(text[text.index('pH (water)') + 2])
    except ValueError as err:
        # print to debug
        for row_idx, row in enumerate(text):
            print(row_idx, row)
        raise ValueError(err)

    try:
        soil_moisture = float(text[text.index('Soil moisture') + 2])
    except ValueError:
        # Original pdf does not have soil_moisture
        soil_moisture = None

    return {
        'date': date,
        'lng': lat_lng[1],
        'lat': lat_lng[0],
        'farm_name': farm_name,
        'field_name': field_name,
        'organic_carbon': organic_carbon,
        'tot_nitrogen': tot_nitrogen,
        'clay': clay,
        'ph': ph,
        'soil_moisture': soil_moisture
    }


def get_data_from_pdf_text(text: 'list[str]') -> 'dict[str, Any]':
    if len(text) in [
        67,  # Original
        74,  # Added Moisture
        73   # Removed something superfluous
    ]:
        return values_from_pdf_using_keyword_lookup(text)
    else:
        raise IOError(f'The format of the pdf has changed again - new length {len(text)}!!!')
