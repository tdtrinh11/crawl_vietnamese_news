from load_data import LoadData
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class TFIDF(object):
	"""
	compute tf-idf
	"""
	def __init__(self, vectorizer=None, ngram_range=(1,1), max_df=1.0,
				min_df=1, max_features=None, analyzer='word'):
		self.ngram_range = ngram_range
		self.max_df = max_df
		self.min_df = min_df
		self.max_features = max_features
		self.analyzer=analyzer
		self.vectorizer = vectorizer

	def fit(self, data):
		self.vectorizer = TfidfVectorizer(analyzer=self.analyzer, 
								max_df=self.max_df, min_df=self.min_df,
								max_features=self.max_features, ngram_range=self.ngram_range)
		self.vectorizer.fit(data)
		print("Fit data success")

	def transform(self, data):
		try:
			return self.vectorizer.transform(data)
		except Exception as e:
			print("error in transform")
			print(e)

	def save_model(self, path):
		try:
			pickle.dump(self.vectorizer, open(path, "wb"))
		except Exception as e:
			print("error in save_vocab()")
			print(e)
			return False
		return True

	def load_model(self, path):
		self.vectorizer = pickle.load(open(path, "rb"))
		self.__init__(vectorizer=self.vectorizer, analyzer=self.analyzer, max_df=self.max_df, min_df=self.min_df,
								max_features=self.max_features, ngram_range=self.ngram_range)
		
		return True

TRAIN_DATA = "/home/tdtrinh11/code/crawl_vietnamese_news/predata/Train"
TEST_DATA = "/home/tdtrinh11/code/crawl_vietnamese_news/predata/Test"

X_train, y_train = LoadData(TRAIN_DATA, TEST_DATA).load_train()

def main():
	tfidf = TFIDF()
	tfidf.fit(data=X_train)
	data = tfidf.transform(X_train)
	print(data[:5])
	tfidf.save_vocab("./Model/tfidf1.pkl")

if __name__ == '__main__':
	main()