import pandas as pd

from src.pdf_report_extract import extract_text_from_pdf, get_data_from_pdf_text


if __name__ == '__main__':
    # main()
    file_path = 'data/test-report.pdf'
    output_csv_path = 'data/test-output.csv'
    pdf_text = extract_text_from_pdf(file_path)
    pdf_output = get_data_from_pdf_text(pdf_text)
    print(pdf_output)
    df = pd.DataFrame.from_dict([pdf_output])
    df.to_csv(output_csv_path, header=True, index=False)
