import json
from collections import Counter
import PyPDF2
import re


class Parser():
    """
        NLP parser class
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def json_parser(filename, stopwords=[]):
        """ 
            JSON parser and data extractor

            filename: file to parse
            stopwords: words to omit
        """
        f = open(filename)  # open and read file
        raw = json.load(f)
        text = raw['text']  # grab text element and split on spaces
        words = text.split(" ")

        # drop stopwords if they exist
        for word in range(0, len(words)):
            if words[word] in stopwords:
                words[word] = ''
        # init counter for word nums and capture the number of total words, return
        wc = Counter(words)
        num = len(words)
        return {'wordcount': wc, 'numwords': num, 'fulltext': text}

    @staticmethod
    def pdf_parser(filename, stopwords=[]):
        """
            PDF file parser and data extractor

            filename: file to parse
            stopwords: words to omit
        """

        # Use PyPDF2 to open and read the file
        print('opening file: %s' % filename)
        file = open(filename, mode='rb')
        print(f'opened {filename}')
        pdf = PyPDF2.PdfFileReader(file)

        num_pages = pdf.getNumPages() # return total page nums of file
        full_text = []  # full text list, one elemnt per page
        num = 0  # indexer for total word number

        # extract text from each page and append to full_text list
        for i in range(num_pages):
            page = pdf.getPage(i).extract_text()
            full_text.append(page)
        
        # join text list to a total string of page words on spaces
        full_text = ' '.join(full_text).lower()

        # use re to sub out characters, capital blocks (figure titles all caps) for empty strings
        full_text = re.sub(r'\b[A-Z]+\b', '', full_text)
        full_text = re.sub("[^\w\s]", '', full_text)
        #  sub out the new line characters for empty strings
        full_text = re.sub("\n", '', full_text)
        
        words = full_text.split(' ')  # split full text on spaces into word list

        # drop all stopwords, len(1) words, and words containing digits
        for word in range(0, len(words)):
            if words[word].lower() in stopwords:
                words[word] = ''
            if len(words[word]) == 1:
                words[word] = ''
            if any(map(str.isdigit, words[word])):
                words[word] = ''
        # remove any extra empty spaces from accidental double spaced sentences
        while '' in words:
            words.remove('')
        
        num = len(words)
        # init counter for each given word's number of occurances
        wc = Counter(words)

        # return desired statistics
        return {'wordcount': wc, 'numwords': num, 'fulltext': full_text, 'num_pages': num_pages}
