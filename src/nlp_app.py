import pprint as pp
from processor import Processor
import parsers

def main():
    p = Processor()
    p.load_text(file_name='../tests/resume_101122.pdf', label='resume_101122', parser=parsers.Parser.pdf_parser)
    p.load_text(file_name='../tests/cyclegan.pdf', label='splitgan', parser=parsers.Parser.pdf_parser)
    print(pp.pprint(p.data))
    p.compare_num_words()


if __name__ == '__main__':
    main()