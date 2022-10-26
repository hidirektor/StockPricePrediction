import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

_VARS = {'window': False, 'fig': None}

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')

def draw(fileName, brandName, dayCount):
    readedData = pd.read_csv(fileName)

    sns.set()
    fig = plt.figure()
    readedData = readedData[["Close"]]
    readedData["Prediction"] = readedData[["Close"]].shift(-dayCount)

    x = np.array(readedData.drop(["Prediction"], axis=1))[:-dayCount]
    y = np.array(readedData["Prediction"])[:-dayCount]

    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.25)
    linear = LinearRegression().fit(xtrain, ytrain)

    featureVal = readedData.drop(["Prediction"], axis=1)[:-dayCount]
    featureVal = featureVal.tail(dayCount)
    featureVal = np.array(featureVal)

    linearPrediction = linear.predict(featureVal)

    predictions = linearPrediction
    valid = readedData[x.shape[0]:].copy()
    valid["Predictions"] = predictions
    plt.title("{bName}'ın Hisse Senedi Fiyatı Tahmin Modeli (Lineer Regresyon)".format(bName=brandName))
    plt.xlabel("Gün Sayısı")
    plt.ylabel("Kapanış Fiyatı USD ($)")
    plt.plot(readedData["Close"])
    plt.plot(valid[["Close", "Predictions"]])
    plt.legend(["Geçmiş Değerler", "Geçerli Değer", "Tahmin"])
    draw_figure(_VARS['window']['figCanvas'].TKCanvas, fig)

AppFont = 'Any 16'
sg.theme('LightGrey')

choices = ['Apple', 'Tesla', 'Microsoft']
layout = [[sg.Text('Şirket Seçin !', font=AppFont)],
          [sg.Combo(choices, default_value="Apple", key='-BRAND-')],
          [sg.Text('Gün Sayısı', font=AppFont)],
          [sg.InputText('Maksimum 30 girebilirsin !', key='-DAYCOUNT-')],
          [sg.Button('Grafiği Güncelle !', font=AppFont)],
          [sg.Canvas(key='figCanvas')],
          [sg.Button('Programı Kapat', font=AppFont)]]
_VARS['window'] = sg.Window('Stock Price Analysis',
                            layout,
                            finalize=True,
                            resizable=False,
                            element_justification="center")
#_VARS['window'].Maximize()
draw("AAPL.csv", "Apple", 30)
while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == ('Programı Kapat') or event is None:
        break
    if event == "Grafiği Güncelle !":
        if values['-BRAND-'] in choices:
            fileName = "test.csv"
            brandName = values['-BRAND-']
            if(brandName == "Apple"):
                fileName = "AAPL.csv"
            elif(brandName == "Tesla"):
                fileName = "TSLA.csv"
            dayCount = values['-DAYCOUNT-']
            if(_VARS['fig'] is not None):
                sg.Canvas.delete("all")
                _VARS['window'].refresh()
                draw(fileName, brandName, int(dayCount))
_VARS['window'].close()
