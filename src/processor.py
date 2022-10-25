from collections import defaultdict, Counter
import random
import matplotlib.pyplot as plt
import plotly.graph_objects as go


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
            text = parser(file_name, self.load_stop_words())

        if label is None:
            label = file_name

        self._save_results(label, text)
    
    def load_stop_words(self, file_name=None, label="", parser=None):
        if file_name is not None:
            pass
        else:
            return [' the ', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'for', ' i ']

    def wordcount_sankey(self, word_list=None, k=5, **kwargs):
        # Process **kwargs
        pad = kwargs.get('pad', 50)  # get - grabs dict value if it exists, otherwise returns defined value
        thickness = kwargs.get('thickness', 30)
        line_color = kwargs.get('line_color', 'black')
        line_width = kwargs.get('line_width', 1)

        for key, value in self.data['wordcount'].items():
            targ_list = []
            val_list = []

            for keys, vals in value.items():
                targ_list.append(keys)
                val_list.append(vals)

            link = {'source': [key]*len(self.data['wordcount'][key]),
                                    'target': targ_list,
                                    'value': val_list}
            print(link)
            node = {'label': None, 'pad': pad, 'thickness': thickness, 'line': {'color': line_color, 'width': line_width}}
            print(node)
            sankey: go.Sankey = go.Sankey(link=link, node=node)
            fig: go.Figure = go.Figure(sankey)
            # fig.update_layout(title_text=f'{self.src} vs {self.targ}')
            fig.show()

    def compare_num_words(self):
        """
        """
        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()

    
