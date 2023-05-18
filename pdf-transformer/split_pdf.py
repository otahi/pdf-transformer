import PyPDF2
import argparse

def split_pdf(input_pdf_path, output_pdf_path, margin):
    with open(input_pdf_path, "rb") as input_pdf:
        pdf_reader = PyPDF2.PdfReader(input_pdf)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            width = page.mediabox.width
            height = page.mediabox.height

            # 左半分のページを作成
            left_page = page.cropbox
            left_page.upper_left = (margin, height)
            left_page.upper_right = (width / 2 - margin, height)
            pdf_writer.add_page(page)

            # 右半分のページを作成
            right_page = page.cropbox
            right_page.upper_left = (width / 2 + margin, height)
            right_page.upper_right = (width - margin , height)
            pdf_writer.add_page(page)

        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

def main():
    parser = argparse.ArgumentParser(description='Split a 2-in-1 PDF into individual pages.')
    parser.add_argument('-in', dest='input_pdf_path', required=True, help='The path to the input PDF.')
    parser.add_argument('-out', dest='output_pdf_path', required=True, help='The path to the output PDF.')
    parser.add_argument('-margin', dest='margin', required=False, help='Margin mm', type=int, default=0)
    args = parser.parse_args()

    split_pdf(args.input_pdf_path, args.output_pdf_path, args.margin)

if __name__ == "__main__":
    main()