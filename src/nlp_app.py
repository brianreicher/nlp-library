from processor import Processor
import parsers


def main():
    p = Processor()  # init processor
    p.load_stop_words(file_name='../tests/stopwords.txt')  # load sample stopwords

    # add all sample paper files
    p.load_text(file_name='../tests/splitgan.pdf', label='computer_science', parser=parsers.Parser.pdf_parser)
    p.load_text(file_name='../tests/physics_paper.pdf', label='physics', parser=parsers.Parser.pdf_parser)
    p.load_text(file_name='../tests/computational_finance.pdf', label='finance', parser=parsers.Parser.pdf_parser)
    p.load_text(file_name='../tests/evolutionary_bio_paper.pdf', label='evolutionary_biology', parser=parsers.Parser.pdf_parser)
    p.load_text(file_name='../tests/genetics_paper.pdf', label='genetics', parser=parsers.Parser.pdf_parser)
    p.load_text(file_name='../tests/math_paper.pdf', label='math', parser=parsers.Parser.pdf_parser)

    # render and save all visualization tests
    p.compare_general_statistics(word_page='word')
    p.make_wordcloud()
    p.make_sankey()
    p.make_wordlength_histogram()


if __name__ == '__main__':
    main()