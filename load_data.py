import os

class LoadData(object):
	"""docstring for LoadData
	load train, validation and test set

	"""
	def __init__(self, train_path, test_path):
		super(LoadData, self).__init__()
		self.train_path = train_path
		self.test_path = test_path

	def load_train(self):
		list_file = os.listdir(self.train_path)

		train_X = []
		train_y = []
		for fi in list_file:
			with open(os.path.join(self.train_path, fi), "r") as f:
				content = f.readlines()
			for c in content:
				train_X.append(c.strip())
			train_y.extend([fi.split(".")[0] for _ in range(len(content))])

		return train_X, train_y

	def load_test(self):
		list_file = os.listdir(self.test_path)

		val_X = []
		val_y = []
		test_X = []
		test_y = []

		for fi in list_file:
			with open(os.path.join(self.test_path, fi), "r") as f:
				content = f.readlines()
			mid = int(len(content) / 4 +0.5)
			for i,c in enumerate(content):
				if i <= mid:
					val_X.append(c)
					val_y.append(fi.split(".")[0])
				else:
					test_X.append(c)
					test_y.append(fi.split(".")[0])

		return val_X, val_y, test_X, test_y