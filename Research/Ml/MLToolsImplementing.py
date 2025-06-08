from RnP.Research.Ml.MLtools import LinearRegression

model=LinearRegression()
X_train = [2.3,2.3,5.7,86,34]
y = 2


predict = model.predict(X_train)
print(predict)


error = model.error(y,kind='mse')
print(error)

# Создание процессора
from eda import *
processor = CSVProcessor()

# Загрузка данных
data = processor.load_csv('Titanic Dataset.csv')

# Анализ данных
processor.print_summary()

# Очистка
processor.clean_data(remove_duplicates=True, handle_missing='fill')


# Визуализация
processor.create_visualizations()

# Экспорт
processor.export_data('result.xlsx', format='excel')