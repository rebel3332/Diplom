from flask import Flask
from datetime import datetime, timedelta
import pickle
import numpy as np
import pandas as pd
from mylib import *
import os
from dotenv import load_dotenv

class Model():
    def __init__(self):
        loging.INFO('Initialization model')
        self.isLoaded = self.loadRegressModel() and self.loadTimeSeriesModel() and self.loadScaler()

    def loadRegressModel(self):
        # Загрузка регрессионной модели
        try:
            with open('models/regressModel.md', 'rb') as file_model:
                self.regressModel = pickle.load(file_model)
            loging.INFO('The model regressModel is loaded')
            return True
        except Exception as ex:
            loging.WARM('The model regressModel was not found')
            loging.ERROR(ex.__str__())
            return False

    def loadTimeSeriesModel(self):
        # Загрузка модели Времянного ряда
        try:
            with open('models/timeSeriesModel.md', 'rb') as file_model:
                self.timeSeriesModel = pickle.load(file_model)
            loging.INFO('The model timeSeriesModel is loaded')
            return True
        except Exception as ex:
            loging.WARM('The model timeSeriesModel was not found')
            loging.ERROR(ex.__str__())
            return False
            
    def loadScaler(self):
        # Загрузка модели
        try:
            with open('models/scalers.md', 'rb') as file_model:
                self.scalers = pickle.load(file_model)
            self.isLoaded = True
            loging.INFO('The scalers is loaded')
            return True
        except Exception as ex:
            loging.WARM('The scalers was not found')
            loging.ERROR(ex.__str__())
            return False

    def predict_OneStep(self):
        """Возвращает кортеж data['Close'], predict"""
        data = loadData(weeks=10)
        X = data['Close'].dropna(axis=0).sort_index(ascending=False)[0:9].values.reshape(9,1)
        X = np.log2(X)
        X = self.scalers['Close'].transform(X)
        X = X.T# reshape(1,9)
        predict = self.regressModel.predict(X)
        predict = [predict] # формирую 2D массив
        print(predict)
        predict = self.scalers['Close'].inverse_transform(predict)
        predict = np.exp2(predict)
        # pred = 123
        return data['Close'].dropna(axis=0), predict[0][0] #распаковываю

    def predict_TimeSeries(self, weeks):
        if type(weeks)==str:
            weeks = int(weeks)
        predict_data = loadData(weeks=1) # Получаю последную свечу
        # predict_data
        index_list = [pd.to_datetime(predict_data['Date'][0])]
        while index_list[-1] < datetime.now() + timedelta(days=7*(weeks-1)):
            index_list.append(index_list[-1] + timedelta(days=7))
            pass
        dates_from_predict = [x.strftime('%Y-%m-%d') for x in index_list]
        dates_from_predict = pd.DataFrame(data=dates_from_predict, columns=['ds'])
        predict = self.timeSeriesModel.predict(dates_from_predict)
        predict = pd.DataFrame(data=predict['trend'].values,  
                               index=predict['ds'].values, 
                               columns=['trend'])
        predict = pd.DataFrame(data=self.scalers['Close'].inverse_transform(predict),
                               index=predict.index,
                               columns=['trend'])
        predict = np.exp2(predict)
        return predict

if __name__ == '__main__':
    if load_dotenv():
        loging.INFO("Read ENVIROMENTS from file .env")
    else:
        loging.WARM("File .env don't found. You can used ENVIROMENTS in your OS.")
        
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')

    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def index():
        return 'OK'

    @app.route('/predict/<period>w')
    @app.route('/predict/<period>W')
    def predict(period):
        global regresModel
        if period.lower() == '1':
            loging.INFO(f'Predict, period="{period}W"')
            if not regresModel.isLoaded:
                answer = f'Regres model is not loaded'
                loging.WARM(answer)
                return answer
            # target = datetime.now()
            # X = np.array([1,2,3,4,5,6,7,8,9]).reshape(1, 9)
            # rez = regresModel.model.predict(X)
            data, rez = regresModel.predict_OneStep()
            print(rez)
            return f'Predict 1W is {rez}'
        # else:
        #     text_error = f'"{period}" is not correct period. You can choose from "1W".'
        #     log('INFO', text_error)
        #     return text_error
        else:
            rez = regresModel.predict_TimeSeries(weeks=period)
            print(rez)
            # return f'Predict 1W is {rez}'
            return str(rez) #f'OK'

    

    loging.INFO('Program is starting')
    regresModel = Model()

    #     # Загрузка модели
    # with open('flask_predict/model_7.pkl', 'rb') as file_model:
    #     model = pickle.load(file_model)

    app.run(host=HOST, port=PORT)