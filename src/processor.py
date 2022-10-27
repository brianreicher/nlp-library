from collections import defaultdict, Counter
import random
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import wordcloud as wc

class Processor:

    def __init__(self) -> None:
        """Constructor"""
        self.data = defaultdict(dict)  # extracted data
        self.stopwords = []
        self.file_dfs = []

    @staticmethod
    def _default_parser(filename):
        return Path(filename).read_text().replace('\n', '')

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
        if parser is None:  # if none, read as text file
            text = Processor._default_parser(file_name)
        else:
            print(f'Using {parser}')
            text = parser(file_name, self.stopwords)

        if label is None:
            label = file_name

        self._save_results(label, text)
    
    def load_stop_words(self, file_name=None):
        try: 
            with open(file_name) as file:
                for line in file:
                    split_list = line.split()
                    length = len(split_list)
                    last_word = split_list[length - 1]
                    if line != '':
                        self.stopwords.append(last_word.lower())
        except FileExistsError as e:
            raise e

    @staticmethod
    def code_mapping(dataframe):
        l = list(set(sorted(list(dataframe['src'])) + sorted(list(dataframe['targ']))))
        
        c = list(range(len(list)))
        lc = dict(zip(l, c))

        dataframe = dataframe.replace({'src': lc, 'targ': lc})
        return dataframe, l

    def wordcount_sankey(self, word_list=None, k=10, **kwargs):
        # Process **kwargs
        pad = kwargs.get('pad', 50)  # get - grabs dict value if it exists, otherwise returns defined value
        thickness = kwargs.get('thickness', 30)
        line_color = kwargs.get('line_color', 'black')
        line_width = kwargs.get('line_width', 1)

        df = pd.DataFrame(self.data['wordcount'])
        # df = df.fillna(0)
        df.reset_index(inplace=True)
        df["word"] = df["index"].values
        df = df.drop(['index'], axis=1)
        
        dat_cols = list(df.columns)
        dat_cols = dat_cols[:len(dat_cols)-1]
        print(dat_cols)
        for cols in dat_cols:
            self.file_dfs.append(df.filter([cols, 'word'], axis=1))
        for item in range(0, len(self.file_dfs)):
            self.file_dfs[item] = self.file_dfs[item].dropna()
            self.file_dfs[item].reset_index(inplace=True)
            self.file_dfs[item] = self.file_dfs[item].drop(['index'], axis=1)
            
            df = self.file_dfs[item]
            for i, row in df.iterrows():
                pass
            # TODO Finish sankey diagram
            # sankey_df, labels = self.code_mapping(sankey_df, src, targ)

            # if vals:
            #     value = sankey_df[vals]
            # else:
            #     value = [1] * sankey_df.shape[0]
    
            # link = {'source': sankey_df[src], 'target': sankey_df[targ], 'value': value}

            # sk = go.Sankey(link=link, node=node)
            # fig = go.Figure(sk)
            # fig.show()

    def compare_num_words(self):
        """
        """
        num_words = self.data['numwords']
        for label, nw in num_words.items():
            plt.bar(label, nw)
        plt.show()

    def make_wordcloud(self):
        text = self.data['fulltext']
        for label, txt in text.items():
            cloud = wc.WordCloud()
            print('Geneating WC)')
            img = cloud.generate(txt)
            print('WC Generated')
            plt.imshow(img)
            plt.show()

    
