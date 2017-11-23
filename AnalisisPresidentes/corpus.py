import os
from pathlib import Path

from string import punctuation
import pandas as pd
#nltk
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
#scikit
from sklearn.feature_extraction.text import CountVectorizer       
#from sklearn.cross_validation import cross_val_score
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

class CorpusHelper(object):
    """
    Class used to parse the corpus
    """

    def __init__(self, language='english'):
        pd.set_option('max_colwidth',1000)
        #download stopwords
        nltk.download('punkt')
        nltk.download("stopwords")
        self.stopwords = stopwords.words(language)
        self.non_words = list(punctuation)
        self.non_words.extend(['¿', '¡'])
        self.non_words.extend(map(str,range(10)))
        self.stemmer = SnowballStemmer(language)
        self.corpus = None

    def _read_corpus_file(self, filename=None):
        if filename is None:
            raise ValueError('filename cannot be None')
        filename = os.path.splitext(filename)[0]
        try:
            corpus = pd.read_csv('{}.csv'.format(filename), encoding='utf-8')
            return corpus
        except:
            from lxml import objectify
            xml = objectify.parse(open('{}.xml'.format(filename)))
            root = xml.getroot()
            corpus = pd.DataFrame(columns=('content', 'polarity'))
            tweets = root.getchildren()
            for i in range(0,len(tweets)):
                tweet = tweets[i]
                try:
                    row = dict(zip(['content', 'polarity', 'agreement'], [tweet.content.text, tweet.sentiments.polarity.value.text, tweet.sentiments.polarity.type.text]))
                except Exception as e:
                    row = dict(zip(['content', 'polarity', 'agreement'], [' '.join(list(tweet.itertext())), tweet.sentiment.get('polarity')]))
                row_s = pd.Series(row)
                row_s.name = i
                corpus = corpus.append(row_s)
            corpus.to_csv('{}.csv'.format(filename), index=False, encoding='utf-8')
            return corpus

    def load(self):
        if self.corpus is None:
            general_train = self._read_corpus_file('general-tweets-train-tagged.csv')
            #general_test = self._read_corpus_file('general-tweets-test-tagged.csv')
            stompol_train = self._read_corpus_file('stompol-tweets-train-tagged.csv')
            #stompol_test = self._read_corpus_file('stompol-tweets-test-tagged.csv')
            socialtv_train = self._read_corpus_file('socialtv-tweets-train-tagged.csv')
            #socialtv_test = self._read_corpus_file('socialtv-tweets-test-tagged.csv')
            self.corpus = pd.concat([
                socialtv_train,
                #socialtv_test,
                #stompol_test,
                stompol_train,
                #general_test,
                general_train
            ])
            #We will filter only those tweets where there is Agreement on the polarity. (And there is some polarity).
            self.corpus = self.corpus.query('agreement != "DISAGREEMENT" and polarity != "NONE"')
            #remove links
            self.corpus = self.corpus[-self.corpus.content.str.contains('^http.*$')]
            #remove neutral opinions and binarilize the rest (0 neg,1 pos)
            self.corpus = self.corpus[self.corpus.polarity != 'NEU']
            self.corpus['polarity_bin'] = 0
            self.corpus.polarity_bin[self.corpus.polarity.isin(['P', 'P+'])] = 1
            self.corpus.polarity_bin.value_counts(normalize=True)

    def stem_tokens(self, tokens):
        stemmed = []
        for item in tokens:
            stemmed.append(self.stemmer.stem(item))
        return stemmed

    def tokenize(self, text):
        # remove non letters
        text = ''.join([c for c in text if c not in self.non_words])
        # tokenize
        tokens =  word_tokenize(text)

        # stem
        try:
            stems = self.stem_tokens(tokens)
        except Exception as e:
            print(str(e))
            print(text)
            stems = ['']
        return stems

class CorpusModel(object):

    def __init__(self, corpus=None):
        self.corpus = corpus

    def fit(self):
        model_file = Path('grid_search.pkl')
        if model_file.is_file():
            grid_search = joblib.load('grid_search.pkl')
        else:
            vectorizer = CountVectorizer(
                            analyzer = 'word',
                            tokenizer = self.corpus.tokenize,
                            lowercase = True,
                            stop_words = self.corpus.stopwords)

            pipeline = Pipeline([
                ('vect', vectorizer),
                ('cls', LinearSVC()),
            ])

            parameters = {
                'vect__max_df': (0.5, 0.9),
                'vect__min_df': (10, 20, 50),
                'vect__max_features': (500, 1000),
                'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
                'cls__C': (0.2, 0.5, 0.7),
                'cls__loss': ('hinge', 'squared_hinge'),
                'cls__max_iter': (500, 1000)
            }
            grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1 , scoring='roc_auc')
            grid_search.fit(self.corpus.corpus.content, self.corpus.corpus.polarity_bin)
            joblib.dump(grid_search, 'grid_search.pkl')
        return grid_search.best_params_

    def vectorizer_from_params(self, params=None):
        if params is None:
            raise ValueError('params cannot be None')

        return CountVectorizer(
            analyzer = 'word',
            tokenizer = self.corpus.tokenize,
            lowercase = True,
            stop_words = self.corpus.stopwords,
            min_df = params['vect__min_df'],
            max_df = params['vect__max_df'],
            ngram_range = params['vect__ngram_range'],
            max_features = params['vect__max_features']
        )

    def model_from_params(self, params=None):
        if params is None:
            raise ValueError('params cannot be None')

        return LinearSVC(
            C=params['cls__C'],
            loss=params['cls__loss'],
            max_iter=params['cls__max_iter'],
            multi_class='ovr',
            random_state=None,
            penalty='l2',
            tol=0.0001
        )

    def x_validation(self, params=None):
        if params is None:
            raise ValueError('params cannot be None')

        vectorizer = self.vectorizer_from_params(params)
        model = self.model_from_params(params) 

        corpus_data_features = vectorizer.fit_transform(self.corpus.corpus.content)
        corpus_data_features_nd = corpus_data_features.toarray()

        scores = cross_val_score(
            model,
            corpus_data_features_nd[0:len(self.corpus.corpus)],
            y=self.corpus.corpus.polarity_bin,
            scoring='roc_auc',
            cv=5
            )

        return scores.mean()

    def predict(self, texts, params):
        if params is None:
            raise ValueError('params cannot be None')

        vectorizer = self.vectorizer_from_params(params)
        model = self.model_from_params(params) 
        pipeline = Pipeline([('vect',vectorizer), ('cls', model)])

        pipeline.fit(self.corpus.corpus.content, self.corpus.corpus.polarity_bin)
        return pipeline.predict(texts)
