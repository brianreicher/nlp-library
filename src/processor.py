from collections import defaultdict, Counter
import random
import matplotlib.pyplot as plt


class Processor:

    def __init__(self) -> None:
        """Constructor"""
        self.data = defaultdict(dict)  # extracted data

    @staticmethod
    def _default_parser(filename):
        return {
            'wordcount': Counter('my name is Jeff'.split(' ')),
            'numwords': random.randrange(10, 50)
        }

    def _save_results(self, label, text) -> None:
        for i, j in text.items():
            self.data[i][label] = j

    # label = A
    # results = {'wordcount': wcA. 'numwords': 25}
    # results = {'wordcount': wcB. 'numwords': 30}
    # data = {'wordcount': {'A': wcA, 'B':wcB}, 'numwords': {'A':25, 'B':30}}

    def load_text(self, file_name, label=None, parser=None) -> None:
        """
        Registers text file with NLP framework
        :param file_name:
        :param label:
        :param parser:
        :return:
        """
        if parser is None:
            text = Processor._default_parser(file_name)
        else:
            text = parser(file_name)

        if label is None:
            label = file_name

        self._save_results(label, text)
    
    def load_stop_words(self, file_name, label="", parser=None):
        pass
    
    def wordcount_sankey(self, word_list=None, k=5):
        pass

    def compare_num_words(self):
        """
        """
        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label ,nw)
        plt.show()

    
