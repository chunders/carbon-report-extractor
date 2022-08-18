import os

import pandas as pd

from src.pdf_report_extract import extract_text_from_pdf, get_data_from_pdf_text


def FilesInFolder(DirectoryPath, fileType, starts = ""):
    files = os.listdir(DirectoryPath)
    selected_files = []
    for file in files:
        if not file.startswith('.') and file.endswith(fileType) and file.startswith(starts):
            selected_files.append(file)
    return selected_files


def get_formatted_data(file_path):
    pdf_text = extract_text_from_pdf(file_path)
    return get_data_from_pdf_text(pdf_text)


if __name__ == '__main__':
    folder_path = 'data'
    output_csv_path = 'data/test-multiple.csv'
    pdf_outputs = [
        get_formatted_data(os.path.join(folder_path, fp))
        for fp in FilesInFolder(folder_path, '.pdf')
    ]
    df = pd.DataFrame.from_dict(pdf_outputs)
    df.to_csv(output_csv_path, header=True, index=False)
