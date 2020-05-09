from load_data import LoadData
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

TRAIN_DATA = "/home/tdtrinh11/code/craw_vietnamese_news/predata/Train"
TEST_DATA = "/home/tdtrinh11/code/craw_vietnamese_news/predata/Test"

X_train, y_train = LoadData(TRAIN_DATA, TEST_DATA).load_train()

class TFIDF(object):
	"""
	compute tf-idf
	"""
	def __init__(self, ngram_range=(1,1), max_df=1.0, vocabulary=None,
		min_df=1, max_features=None, analyzer='word'):
		self.ngram_range = ngram_range
		self.max_df = max_df
		self.min_df = min_df
		self.max_features = max_features
		self.analyzer=analyzer
		self.vacabulary=vocabulary
		self.vectorizer = TfidfVectorizer(vocabulary=self.vocabulary, analyzer=self.analyzer, max_df=self.max_df, min_df=self.min_df,
								max_features=self.max_features, ngram_range=self.ngram_range)

	def fit(self, X_train):
		self.vectorizer.fit(X_train)

	def save_vocab(self, path):
		try:
			pickle.dump(self.vectorizer.vocabulary_, open(path, "wb"))
		except Exception as e:
			print("error in save_vocab()\n")
			print(e)
			return False
		return True

	def load_model(self, path):
		self.vacabulary = pickle.load(open(path, "rb"))
		self.__init__(vocabulary=self.vocabulary, analyzer=self.analyzer, max_df=self.max_df, min_df=self.min_df,
								max_features=self.max_features, ngram_range=self.ngram_range)
		return True