from processor import Processor
import parsers


def main():
    p = Processor()
    p.load_text(file_name='../tests/resume_101122.pdf', label='resume_101122', parser=parsers.Parser.pdf_parser)
    p.load_text(file_name='../tests/splitgan.pdf', label='splitgan', parser=parsers.Parser.pdf_parser)
    # p.compare_num_words()
    p.wordcount_sankey()


if __name__ == '__main__':
    main()