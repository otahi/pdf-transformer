import PyPDF2
import argparse

def crop_pdf(input_pdf_path, output_pdf_path, margin, targets, excludes):
    with open(input_pdf_path, "rb") as input_pdf:
        pdf_reader = PyPDF2.PdfReader(input_pdf)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):

            page = pdf_reader.pages[page_num]
            width = page.mediabox.width
            height = page.mediabox.height

            isTargeted = targets == None or page_num + 1 in targets # Default: target all pages
            isExcluded = excludes != None and page_num + 1 in excludes # Defalt: no excluded pages

            if( isTargeted and not isExcluded ):
                cropbox = page.cropbox

                # TODO: set like css (top-margin right-margin bottom-margin left-margin)
                cropbox.upper_left = (margin, height - margin)
                cropbox.upper_right = (width - margin, height - margin)
                cropbox.lower_left = (margin, margin)
                cropbox.lower_right = (width - margin, margin)

            pdf_writer.add_page(page)

        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

def main():
    parser = argparse.ArgumentParser(description='Split a 2-in-1 PDF into individual pages.')
    parser.add_argument('-in', dest='input_pdf_path', required=True, help='The path to the input PDF.')
    parser.add_argument('-out', dest='output_pdf_path', required=True, help='The path to the output PDF.')
    parser.add_argument('-margin', dest='margin', required=True, help='Margin mm', type=int)
    parser.add_argument('-targets', dest='targets', nargs='+', required=False, help='The page numbers to extract. e.g. -target 1 3 5', type=int)
    parser.add_argument('-excludes', dest='excludes', nargs='+', required=False, help='The page numbers to extract. e.g. -exclude 1 3 5', type=int)
    args = parser.parse_args()

    crop_pdf(args.input_pdf_path, args.output_pdf_path, args.margin, args.targets, args.excludes)

if __name__ == "__main__":
    main()