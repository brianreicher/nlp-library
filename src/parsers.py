import json
from collections import Counter, defaultdict
import PyPDF2
import pprint as pp

class Parser():
# CAN TOTALLY IMPLEMENT WITH SOME ABSTRACTION
    def __init__(self) -> None:
        pass

    @staticmethod
    def json_parser(filename):
        f =  open(filename)
        raw = json.load(f)
        text = raw['text']
        words = text.split(" ")
        wc = Counter(words)
        num = len(words)
        return {'wordcount':wc, 'numwords':num}

    @staticmethod
    def pdf_parser(filename):
        print('opening file: %s' % filename)
        file = open(filename, mode='rb')
        print(f'opened {filename}')
        pdf = PyPDF2.PdfFileReader(file)
        pdf_dict:defaultdict = {}

        num_pages = pdf.getNumPages()

        text = []
        num = 0
        for i in range(num_pages):
            page = pdf.getPage(i).extract_text()
            page_split = page.split(' ')

            for j in range(len(page_split) - 1):
                page_split[j] = page_split[j].replace('\n', ' ')
        
            num += len(page_split)
            text.append(page_split)
        
        text = ' '.join(str(e) for e in text)
        text = text.lower()
        text = text.replace("'", "")
        text = text.replace(", ", ' ')
        text = text.replace('[', '')
        text = text.replace(']', '')  # TODO CLEAN
        text = text.replace('  ', '')
        text = text.replace('-', '')

        words = text.split(' ')
        wc = Counter(words)

        return {'wordcount': wc, 'numwords': num}
