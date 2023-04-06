# -*- coding: utf-8 -*-
import time
import traceback

import matplotlib
from PyQt5.QtCore import pyqtSignal, QThread, QTimer

import numpy as np
from Windows import Ui_MainWindow
from fuzzy import *
from drawplot import drawPlot
import os
from toolkit import toolkit
# 导入程序运行必须模块
import sys
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
matplotlib.use('Qt5Agg')

# 設定gui的功能
class MyMainWindow(QMainWindow, Ui_MainWindow):

    step=0#用來判斷要不要創建plotpicture

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.inputfilepath_btn_2.clicked.connect(self.choosefileDialog)
        self.pushButton_2.clicked.connect(self.startCar)
        self.canva = drawPlot()
        self.plot_layout.addWidget(self.canva)

    def readMapFile(mapFile):
        goal_points = list()
        boarder_points = list()
        with open(mapFile, 'r') as f:
            lines = f.readlines()
            for i,line in enumerate(lines):
                line = list(map(float, line.strip('\n').split(',')))
                if i == 0 :
                    original_point = line
                elif i == 1 or i == 2 :
                    goal_points.append(line)
                else:
                    boarder_points.append(line)
        original_point = np.array(original_point)
        goal_points = np.array(goal_points)
        boarder_points = np.array(boarder_points)
        return original_point, goal_points, boarder_points

    def choosefileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if filename:
            self.inputfilepath_edit.setText(filename)
        else:
            self.inputfilepath_edit.setText("")

    def startCar(self):
        mapFilePath = self.mapfilepath_edit.text()
        original_point, self.goal_points, self.boarder_points = readMapFile(mapFilePath)
        self.canva.drawMap(self.goal_points,self.boarder_points)

        self.currentPoint = original_point[:-1]
        self.currentPhi = original_point[-1]
        self.currentVector = np.array([100, 0])

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.updatePlot)
        self.timer.start()

    def updatePlot(self):
        try:
            phi = self.currentPhi
            point = self.currentPoint
            self.canva.drawPoint(point)
            sensor_vectors = drawPlot.getSensorVector(self.currentVector, phi)
            sensor_distances = []
            cross_points = []
            for sensor_vector in sensor_vectors:
                cross_point = drawPlot.findCrossPoint(self.boarder_points, point, sensor_vector)
                #self.canva.drawPoint(cross_point, 'r')
                distance = toolkit.euclid_distance(cross_point, point)
                cross_points.append(cross_point)
                sensor_distances.append(distance)
            sensor_distances = np.array(sensor_distances).flatten()
            self.canva.drawSensor(cross_points)
            theta = fuzzy_system(sensor_distances)
            # theta = answers[i]
            print('distance = ', sensor_distances)
            print('point = ', point)
            print('phi =', phi)
            print('theta = ', theta)
            print('---------------')
            if np.min(sensor_distances) < 3:
                raise Exception("touch the wall of map")
            self.canva.updatePlot()
            self.currentPoint, self.currentPhi = drawPlot.findNextState(point, phi, theta)
            if self.currentPoint[1] > min(self.goal_points[:,1]):
                self.timer.stop()
        except Exception as e:
            print(e)
            traceback_output = traceback.format_exc()
            print(traceback_output)
            self.timer.stop()
            sys.exit(app.exec_())

if __name__ == "__main__":
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainWindow()

    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())

