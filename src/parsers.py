import json
from collections import Counter
import PyPDF2
import re

class Parser():
    def __init__(self) -> None:
        pass

    @staticmethod
    def json_parser(filename, stopwords=[]):
        f = open(filename)
        raw = json.load(f)
        text = raw['text']
        words = text.split(" ")
        wc = Counter(words)
        num = len(words)
        return {'wordcount': wc, 'numwords': num, 'fulltext': text}

    @staticmethod
    def pdf_parser(filename, stopwords=[]):
        print('opening file: %s' % filename)
        file = open(filename, mode='rb')
        print(f'opened {filename}')
        pdf = PyPDF2.PdfFileReader(file)

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
        text.lower()
        text = re.sub(r'\b[A-Z]+\b', '', text)
        text = re.sub("[^\w\s]", '', text)


        words =text.split(' ')

        for word in range(0, len(words)):
            print(words[word])
            if words[word].lower() in stopwords:
                words[word] = ''
        words = words[1:]
        wc = Counter(words)

        return {'wordcount': wc, 'numwords': num, 'fulltext': text}
