from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

class SVM(object):
    def __init__(self, C=1.0, kernel='rbf', gamma='scale'):
        self.C = C
        self.kernel = kernel
        self.gamma = gamma
        self.model = SVC(C=self.C, kernel=self.kernel, 
                        gamma=self.gamma)

    def fit(self, X, y):
        self.model.fit(X, y)
    
    def predict(self, X):
        return self.model.predict(X)
    
    def save_model(self):
        pass

    def load_model(self):
        pass
    