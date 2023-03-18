# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 14:19:25 2021

@author: M Taha khan
"""

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QSizePolicy, QLineEdit, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QPixmap, QFont
from pandas import DataFrame
import numpy as np
import pandas as pd
import statistics
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'COVID-19 project'
        self.width = 1920
        self.height = 1080
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        
        self.layout = QVBoxLayout(self)

        #Tabs
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(1920, 1080)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"  Graphs    ")
        self.tabs.addTab(self.tab2,"  Image    ")
        
        #comboBox1
        self.cb1 = QComboBox(self.tab1)
        self.cb1.move(660, 160)
        self.cb1.resize(160, 20)
        self.cb1.currentIndexChanged.connect(self.comboBoxSelectionchange1)
        
        #QLabel vs
        self.qLabel = QLabel(self.tab1)
        self.qLabel.move(735, 200)
        self.qLabel.setText("VS")
        
        #comboBox2
        self.cb2 = QComboBox(self.tab1)
        self.cb2.move(660, 240)
        self.cb2.resize(160, 20)
        self.cb2.currentIndexChanged.connect(self.comboBoxSelectionchange2)

        self.button = QPushButton('Show Data', self.tab1)
        self.button.move(250,550)
        self.button.resize(160,30)
        
        self.getCountries()
        
        m = PlotCanvas(self.tab1, width=6, height=5)
        m.move(50,10)
        m.draw()
        
        self.button.clicked.connect(m.plotNoOfCasesPerDay)
        self.button.clicked.connect(self.calculateCovariance)
        self.button.clicked.connect(self.calculateCorrelation)
        
        m1 = PlotCanvas(self.tab1, width=6, height=5)
        m1.move(1000,10)
        m1.draw()
        
        button1 = QPushButton('Show Temperature', self.tab1)
        button1.move(1200,550)
        button1.resize(160,30)
        button1.clicked.connect(m1.plotNoOfCasesWithTemperature)
        

        
        #QLabel covariance
        self.covarianceLbl = QLabel(self.tab1)
        self.covarianceLbl.move(150, 755)
        self.covarianceLbl.setText("Covariance:")
        
        #QLineEdit covariance
        self.covarianceTxt = QLineEdit(self.tab1)
        self.covarianceTxt.move(230, 750)
        self.covarianceTxt.resize(120,25)
        self.covarianceTxt.setReadOnly(True)
        
        
        #QLabel correlation
        self.correlationLbl = QLabel(self.tab1)
        self.correlationLbl.move(400, 755)
        self.correlationLbl.setText("Correlation:")
        
        #QLineEdit correlation
        self.correlationTxt = QLineEdit(self.tab1)
        self.correlationTxt.move(480, 750)
        self.correlationTxt.resize(120,25)
        self.correlationTxt.setReadOnly(True)
        
        #QLabel image label
        self.imageLabel = QLabel(self.tab2)
        self.imageLabel.move(220, 10)
        self.imageLabel.setText("Normal vs Corona Lungs")
        self.imageLabel.setFont(QFont('Arial', 40))
        
        #QLabel image label
        self.imageLabel = QLabel(self.tab1)
        self.imageLabel.move(580, 10)
        self.imageLabel.setText("Data Visualisation of COVID-19")
        self.imageLabel.setFont(QFont('Arial', 30))
        
        #QLabel image
        self.pictureLabel = QLabel(self.tab2)
        self.pictureLabel.move(50, 70)
        self.pixmap = QPixmap('lungs_bilateralFilter.png')
        self.pictureLabel.setPixmap(self.pixmap)
        self.pictureLabel.resize(self.pixmap.width(),self.pixmap.height())
        
        #QLabel image2
        self.pictureLabel = QLabel(self.tab2)
        self.pictureLabel.move(30, 320)
        self.pixmap = QPixmap('lungs_noisy.png')
        self.pictureLabel.setPixmap(self.pixmap)
        self.pictureLabel.resize(self.pixmap.width(),self.pixmap.height())
        
        
        
        global countryText1
        countryText1 = str(self.cb1.currentText())
        global countryText2
        countryText2 = str(self.cb2.currentText())
        
        self.show()
        
    def calculateCovariance(self):
        global countryText1
        global countryText2
        cov = ''
        if(countryText2 != '-----'):
            self.df = pd.read_csv('new_cases.csv')
            df1 = self.df[countryText1]
            df2 = self.df[countryText2]
            cov = df2.cov(df1)
        self.covarianceTxt.setText(str(round(cov,5)))
        
        
    def calculateCorrelation(self):
        global countryText1
        global countryText2
        corr = ''
        corrStr = '0'
        if(countryText2 != '-----'):
            self.df = pd.read_csv('new_cases.csv')
            df1 = self.df[countryText1]
            df2 = self.df[countryText2]
            corr = (df2.cov(df1))/(statistics.stdev(df1)*statistics.stdev(df2))
        if(np.isnan(corr) == True):
            corrStr = '0'
        else:
            corrStr = str((round(corr,5)))
        self.correlationTxt.setText(corrStr)
        
    def comboBoxSelectionchange1(self):
        global countryText1
        countryText1 = str(self.cb1.currentText())
        
    def comboBoxSelectionchange2(self):
        global countryText2
        countryText2 = str(self.cb2.currentText())
        if(countryText2 == '-----'):
            self.button.setText('Show Data')
        else:
            self.button.setText('Compare Data')
        self.button.show()
            
        
    def getCountries(self):
        self.df = pd.read_csv('new_cases.csv')
        countriesList = list(self.df.columns.values)
        countriesList.pop(0)
        self.cb1.addItems(countriesList)
        countriesList.insert(0, '-----')
        self.cb2.addItems(countriesList)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        fig.tight_layout()
        self.setParent(parent)
        self.axes = fig.add_subplot(111)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
    def plotNoOfCasesPerDay(self):
        global countryText1
        global countryText2
        self.isCompare = countryText2 != '-----'
        self.df1 = pd.read_csv('new_cases.csv')
        self.data1 = ''
        self.df11 = ''
        
        if(self.isCompare == True):
            self.data1 = {countryText1: self.df1[countryText1].values.tolist(),
                      countryText2: self.df1[countryText2].values.tolist()}
            self.df11 = DataFrame(self.data1,columns=[countryText1,countryText2])
        else :
            self.data1 = {countryText1: self.df1[countryText1].values.tolist()}    
            self.df11 = DataFrame(self.data1,columns=[countryText1])
            
        ax = self.axes
        ax.cla()
        ax.set_xlabel("No. of Days")
        ax.set_ylabel("No. of Cases")
        self.df11.plot(kind='line', legend=True, ax=ax)
        self.title = ("Corona cases in " + countryText1 + " vs " + countryText2) if self.isCompare == True else ("Corona cases in " + countryText1)
        ax.set_title(self.title)
        self.draw()
        
        
    def plotNoOfCasesWithTemperature(self):
        self.df1 = pd.read_csv('new_cases.csv')
        self.df2 = pd.read_csv('temp_f.csv')
        
        self.data1 = {'France': self.df1['France'].values.tolist(),
                      'Temperature': self.df2['TAVG'][1:323].tolist()}
        self.df11 = DataFrame(self.data1)
        
        ax = self.axes
        ax.cla()
        ax.scatter(self.df1['France'],self.df2['TAVG'][1:323])
        ax.set_xlabel("No. of Cases in France")
        ax.set_ylabel("Temperature in France")
        ax.set_title("Temperature vs Cases in France")
        self.draw()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())