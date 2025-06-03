from RnP.Research.Ml.MLtools import LinearRegression

model=LinearRegression()
X_train = [2.3,2.3,5.7,86,34]
y = 2


predict = model.predict(X_train)
print(predict)


error = model.error(y,kind='mse')
print(error)

