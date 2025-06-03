import numpy as np

class LinearRegression:
    def __init__(self):
        self.X_values = None
        self.y = None

    def predict(self,X_values,weights=None):
        self.X_values = X_values
        predict = 0
        weights = [1.0 for i in range(len(X_values))]

        for index,value in enumerate(X_values):
            predict += value*weights[index]

        return predict

    def error(self,y,kind='mae'):
        self.y = y
        predict = self.predict(self.X_values)
        error = self.mae(y)
        if kind == 'mae':
            return f"mae_error:{error}"
        if kind == 'mse':
            return f"mse_error:{np.square(error)}"






    def mae(self,y):
        predict = self.predict(self.X_values)
        return abs(y - predict)

