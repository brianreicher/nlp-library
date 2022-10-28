from collections import defaultdict
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import wordcloud as wc
import seaborn as sns


class Processor:
    """
        A class for the NLP of academic papers
    """
    
    def __init__(self) -> None:
        """Constructor"""
        self.data = defaultdict(dict)  # extracted data
        self.stopwords = []  # stopwords list to load from file

    @staticmethod
    def _default_parser(filename):
        """
            Default parser to load and read txt files
        """
        return Path(filename).read_text().replace('\n', '')

    def _save_results(self, label, text) -> None:
        """
            Save results from given labeled file to nested dict
            label: label of file
            text: parser extracte information
        """
        for i, j in text.items():
            self.data[i][label] = j

    def load_text(self, file_name, label=None, parser=None) -> None:
        """
        Registers text file with NLP framework and parses
        :param file_name: file name from directory path
        :param label: label for file (category)
        :param parser: parser to use (choose json_parser or pdf_parser)
        """
        if parser is None:  # if none, read as text file
            text = Processor._default_parser(file_name)
        else:  # use designated parser ot parse file, returning extracted feature list
            print(f'Using {parser}')
            text = parser(file_name, self.stopwords)

        if label is None: 
            label = file_name  # set label to the filename if there is no label

        self._save_results(label, text)  # save results
    
    def load_stop_words(self, file_name=None):
        """
            Load stop words from txt file, append them to the state variable stop_words

            file_name: file name from directory path
        """
        try: 
            with open(file_name) as file:  # open file from location
                for l in file:
                    split_list = l.split() # for each line, split data into a list
                    length = len(split_list)  # length of split data line
                    lw = split_list[length - 1] # grab final word
                    if l != '':
                        self.stopwords.append(lw.lower())  # append to stop_words list if not an empty string
        except FileExistsError as e:
            raise e  #throw error if no such file exists

    def code_mapping(self, df, src, targ):
        """ 
            Function from class/hw1 --> sankey code mapping
        """

        labels = list(df[src]) + list(df[targ])  # concatenate src and targ list to labels
        codes = list(range(len(labels)))  # render code range list

        lcmap = dict(zip(labels, codes))  # zip labels, codes into dict
        df = df.replace({src: lcmap, targ: lcmap})  # replace in dataframe

        return df, labels  # return updated dataframe and labels
    

    def make_sankey(self, k=10, save_as='academic_keywords_sankey.png'):
        """
            Creates dataframe for creating sankey visualizations given text extracted data on the frequency of specific words

            k: number of most-often occruing words to draw nodes between
            save_as: name to save output image as in img directory
        """
        df = pd.DataFrame(self.data['wordcount'])  # create dataframe from Counter dict for most often occruing words
        df = df.fillna(0)  # fill values with 0 occurances if the file was missing data for a given word
        df.reset_index(inplace=True)
        df["word"] = df["index"].values  
        
        # set words to the index, shifting the 'word' column to the front of the df for ease-of-processing
        df = df[['word'] + [c for c in df.columns if c != 'word']]
        df = df.drop(['index'], axis=1)  # drop index

        # init sum column for total occurances of words across files, sort
        df['sum'] = df.sum(axis=1)  
        df = df.sort_values(by=['sum'], ascending=False)
        df = df.head(k)  # filter to k-most occuring words

        df.drop('sum', inplace=True, axis=1)
        df.reset_index(inplace=True)
        df.drop('index', inplace=True, axis=1)

        cols = list(df.columns)  # list of df columns to index 

        file= [] 
        words = []
        nums = []  # file, word, and nums for concatenation into complete comparison dataframe

        for obj, row in df.iterrows():  # iterate over rows and append counts, words, and given file names to respective lists
            w = row[0]
            for word_count in range(1, len(row)):
                words.append(w)  # give specific word to word list
                nums.append(row[word_count])  # give respecive count to the count at the same index
            for col in range(1, len(cols)):
                file.append(cols[col])  # add respecitve file name for each word's number of occurances

        # create sankey dict for name, word, and nums to make final dataframe
        sk = {'filename':file, 'words':words, 'nums': nums}
        df_final = pd.DataFrame(sk)

        # apply code mapping to final df
        df, lbls = self.code_mapping(df=df_final, src='words', targ='filename')    

        # set values of sankey to the number of counts
        value = df['nums']

        # init sankey elements, namely the link and node dicts (as in HW1)
        link = {'source': df['words'], 'target': df['filename'], 'value': value}
        node = {'label': lbls, 'pad': 60, 'thickness': 20,
                                'line': {'color': 'blue', 'width': 10}}

        # create sankey obejct, add title, show, and save fig as a png
        sankey = go.Sankey(link=link, node=node)
        fig = go.Figure(sankey)
        fig.update_layout(title='Academic Paper Joint Sankey Analaysis Across Disciplines')
        fig.show()
        fig.write_image(f'../img/{save_as}')
    
    def compare_general_statistics(self, word_page='page', save_as='summary_statistics.png'):
        """
            Display general page count or word count for individual academic papers.

            word_page: 'page' or 'word', to chose statistics
            save_as: name to save output image as in img directory
        """
        plt.figure(figsize=(12, 7))  # init fig, set size
        plt.rcParams.update({'font.size': 10})

        if word_page.lower() == 'page':  # if word_page is page, create page num bar chart
            plt.title('General Page Length Statistics of Academic Papers', loc='center')
            plt.ylabel('Number of Pages')
            num_pages = self.data['num_pages']
            
            # loop throuh page num dict items and graph respectively
            for label, np in num_pages.items():
                plt.bar(label, np)

        elif word_page.lower() == 'word':  # if word_page is word, create word count bar chart
            plt.title('General Word Count Statistics of Academic Papers', loc='center')
            plt.ylabel('Number of Words')

            # loop through word count dict items and graph respectively
            num_words = self.data['numwords']
            print(num_words)
            for label, nw in num_words.items():
                print(nw)
                plt.bar(label, nw)
        # show fig, save as png file
        plt.show()
        plt.savefig(f'../img/{save_as}')
        plt.close()

    def make_wordcloud(self, save_as='academic_wordcloud'):
        """
            Make wordcloud subplots for all given academic papers 

            save_as: name to save output image as in img directory
        """
        text = self.data['fulltext']  # extract full text string from all files

        # set the subplot array to a square if num papers is even
        if len(text)%2 == 0:
            nrows = int(len(text)/2)
            ncols = int(len(text)/2)
        # else, set to rectangle with one more col than row 
        else:
            nrows=int(len(text)/2)
            ncols= int((len(text)/2)+1)


        plt.figure(dpi=150)  # init fig
        index = str(nrows) + str(ncols) + str(1)  # set subplot index 

        for label, txt in text.items():
            cloud = wc.WordCloud().generate(txt)  # generate wordcloud for each full-text
            index = int(index)
            plt.subplot(index)
            plt.imshow(cloud)  # plot and show fig at given index
            plt.axis('off')
            plt.title(f'{label} wordcloud!', fontdict={'fontsize': 9})
            index += 1  # increment index to populate subplot array
        
        # show and save fig as png file
        plt.show()
        plt.savefig(f'../img/{save_as}')
        plt.close()

    def make_wordlength_histogram(self, save_as='wordlen_histogram.png'):
        """
            Make word length historgram subplots for all given academic papers 

            save_as: name to save output image as in img directory
        """

        text = self.data['fulltext']  # extract element only to analyze for subplot array shape (number of files)

        # set the subplot array to a square if num papers is even
        if len(text)%2 == 0:
            nrows = int(len(text)/2)
            ncols = int(len(text)/2)
        # else, set to rectangle with one more col than row 
        else:
            nrows=int(len(text)/2)
            ncols= int((len(text)/2)+1)
        
        # init list for histogram word length (from counter words) and file_averages
        individual_wl = []
        file_averages = []
        # loop through counter words, add length of each counted word to a default dict 
        for t, data in self.data['wordcount'].items():

            # init counters to get runnnng length total and number of words with countable length
            file_average = 0 
            num_counted = 0
            wl = defaultdict()
            for word, occ in data.items():
                wl[word] = len(word)
                file_average += len(word)
                num_counted += 1

            # calculate average
            file_average = round(file_average/num_counted, 2)
            file_averages.append(file_average)

            # translate between datatype --> dict to DF for ease of processing histogram, need from_dict func because our object is a default dict
            df = pd.DataFrame.from_dict(wl, columns=['wordlen'], orient='index')

            # sort by word lenght, drop index colum
            df.sort_index(inplace=True)
            df.reset_index(inplace=True)

            # append individual dataframes to list
            individual_wl.append(df)

        # init subplots, index for iterating
        plt.figure(figsize=(15, 7))
        index = str(nrows) + str(ncols) + str(1)  # set subplot index 

        # create list of file name using list comprehension
        file = [filename for filename, txt in text.items()]

        # loop through each dataframe in individual_wl
        file_count_indexer = 0 # index to set titles for each file
        for item in range(0, len(individual_wl)):
                index = int(index)  # set subplot index as an integer
                plt.subplot(index)  # init subplot at index

                num_bins = int(max(individual_wl[item]['wordlen'])/2)  # set bin num to half the max number of words
                sns.histplot(data=individual_wl[item], x='wordlen', bins=num_bins)  # create seaborn histogram, was easier than pyplot (dataframe got ugly, wanted to split with autobins)
                
                # set subplot title with individual filename and average
                plt.title(f'{file[file_count_indexer]} word-length histogram: avg = {file_averages[file_count_indexer]}', fontdict={'fontsize': 7})

                index += 1  # increment subplot index
                file_count_indexer += 1  # index file_count_indexer
        
        # display, save figure as png
        plt.tight_layout(pad=1.5)
        plt.show()
        plt.savefig(f'../img/{save_as}')
        plt.close()