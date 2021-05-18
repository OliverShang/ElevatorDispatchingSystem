import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

from scheduler import Scheduler


# 定义电梯门状态
DOOR_CLOSED = 0  # 电梯门关闭
DOOR_OPENED = 1  # 电梯门打开

# 定义电梯运行状态
HALT = 0  # 电梯静止
ASCENDING = 1  # 电梯上升
DESCENDING = 2  # 电梯下降
MALFUNCTION = 3  # 电梯故障

# 外部按钮状态
UP = 0  # 上行
DOWN = 1  # 下行

# 数量
ELEV_NUM = 5
FLOOR_NUM = 20

#  楼层按钮大小
FLOOR_BUTTON_X = 40
FLOOR_BUTTON_Y = 23

#  内部开关门按钮大小
DOOR_BUTTON_X = 20
DOOR_BUTTON_Y = 20

#  电梯动画大小
ELEV_ANIME_X = 220
ELEV_ANIME_Y = 220

#  上下行状态动画大小
ELEV_STATUS_X = 40
ELEV_STATUS_Y = 40

#  电梯序号图标大小
ELEV_ENUM_X = 40
ELEV_ENUM_Y = 40

#  电梯修理按钮大小
ELEV_REPAIR_SIZE = 40

#  外部控制图标大小
EXT_CTRL_SIZE = 25


class UI_MainWindow(object):
    def __init__(self):
        self.scheduler = Scheduler(self)

        #  电梯序号icon
        self.elevator_enumerate_image = []
        self.elevator_repair_enumerate_image = []
        #  电梯修理序号icon
        #  同上，直接调用
        #  电梯开关门animation
        self.elevator_open_animation = []
        self.elevator_close_animation = []
        #  电梯开关门完毕后的图像
        self.elevator_open_image = []
        self.elevator_close_image = []
        #  电梯状态指示animation
        self.elevator_ascending_animation = []
        self.elevator_descending_animation = []
        #  电梯报警与修理按钮
        self.elevator_alarm_button = []
        self.elevator_repair_button = []
        #  电梯开门关门按钮
        self.elevator_door_open_button = []
        self.elevator_door_close_button = []
        #  电梯楼层数码管显示
        self.elevator_floor = []
        #  每部电梯的楼层按钮
        self.elevator_floor_button = []
        #  外部控制的楼层按钮
        self.external_floor_button = []

    #  各模块的位置

    def setupUI(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1757, 900)
        MainWindow.setStyleSheet("")
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("CentralWidget")
        MainWindow.setCentralWidget(self.central_widget)

        #  加载样式qss文件
        #  按钮读入图片

        #  位置信息
        #  电梯的坐标
        elevator_pos_x = []
        elevator_pos_y = []
        #  电梯状态指示灯的坐标
        elevator_status_pos_x = []
        elevator_status_pos_y = []
        #  电梯楼层显示数码管坐标
        elevator_floor_pos_x = []
        elevator_floor_pos_y = []
        #  电梯序号图像坐标
        elevator_enumerate_pos_x = []
        elevator_enumerate_pos_y = []
        #  电梯开关门按钮坐标
        elevator_open_pos_x = []
        elevator_open_pos_y = []
        elevator_close_pos_x = []
        elevator_close_pos_y = []
        #  电梯内部楼层按钮的坐标
        elevator_button_pos_x = []
        elevator_button_pos_y = []
        #  外部控制按钮的坐标
        external_up_button_pos_x = []
        external_up_button_pos_y = []
        external_down_button_pos_x = []
        external_down_button_pos_y = []
        #  电梯报警和修理按钮的坐标
        elevator_alarm_pos_x = []
        elevator_alarm_pos_y = []
        elevator_repair_x = []
        elevator_repair_y = []
        #  电梯修理序号图像坐标
        elevator_enumerate_repair_pos_x = []
        elevator_enumerate_repair_pos_y = []

        #  设置各模块的位置
        for i in range(ELEV_NUM):
            elevator_pos_x.append(30 + i * (220 + 60))
            elevator_pos_y.append(630)
            elevator_status_pos_x.append(255 + i * (220 + 60))
            elevator_status_pos_y.append(elevator_pos_y[i] + 40)
            elevator_floor_pos_x.append(255 + i * (220 + 60))
            elevator_floor_pos_y.append(elevator_pos_y[i] + 40 * 2)
            elevator_enumerate_pos_x.append(255 + i * (220 + 60))
            elevator_enumerate_pos_y.append(elevator_pos_y[i])
            elevator_open_pos_x.append(255 + i * (220 + 60))  #  以下三个按钮20x20
            elevator_close_pos_x.append(255 + 20 + i * (220 + 60))
            elevator_open_pos_y.append(770)
            elevator_close_pos_y.append(770)
            elevator_alarm_pos_x.append(elevator_open_pos_x[i] + int(DOOR_BUTTON_X / 2))
            elevator_alarm_pos_y.append(
                elevator_open_pos_y[i] + int(DOOR_BUTTON_X / 2) + 20
            )
            elevator_button_pos_x.append(
                elevator_pos_x[i] + int(ELEV_ANIME_X / 2) - int(FLOOR_BUTTON_X / 2)
            )  #  此按钮40x23，只是一楼按钮的位置，其他19层使用相对位置即可计算
            elevator_button_pos_y.append(elevator_pos_y[i] - 40)
            elevator_enumerate_repair_pos_x.append(1450 + i * 60)
            elevator_enumerate_repair_pos_y.append(710)
            elevator_repair_x.append(elevator_enumerate_repair_pos_x[i])
            elevator_repair_y.append(elevator_enumerate_repair_pos_y[i] + 50)

        #  设置外部楼层按钮的位置
        for i in range(FLOOR_NUM - 1):  #  注意第一层没有向下按钮
            external_up_button_pos_x.append(1420)
            external_up_button_pos_y.append(600 - i * 30)
            external_down_button_pos_x.append(1480)
            external_down_button_pos_y.append(570 - i * 30)

        #  设置动画、文字等
        #  以下设置位置以及放入动画的代码有大量重复
        for i in range(ELEV_NUM):
            #  开门动画
            self.elevator_open_animation.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_open_animation[i].setGeometry(
                QtCore.QRect(
                    elevator_pos_x[i], elevator_pos_y[i], ELEV_ANIME_X, ELEV_ANIME_Y
                )
            )
            self.elevator_open_animation[i].setMovie(
                QtGui.QMovie("resources/doorOpen.gif")
            )
            self.elevator_open_animation[i].movie().setPaused(True)
            self.elevator_open_animation[i].setVisible(False)
            self.elevator_open_animation[i].setObjectName(
                "open_animation_" + str(i + 1)
            )  #  从1开始编号

            #  关门动画，同上
            self.elevator_close_animation.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_close_animation[i].setGeometry(
                QtCore.QRect(
                    elevator_pos_x[i], elevator_pos_y[i], ELEV_ANIME_X, ELEV_ANIME_Y
                )
            )
            self.elevator_close_animation[i].setMovie(
                QtGui.QMovie("resources/dpprClose.gif")
            )
            self.elevator_close_animation[i].movie().setPaused(True)
            self.elevator_close_animation[i].setVisible(False)
            self.elevator_close_animation[i].setObjectName(
                "close_animation_" + str(i + 1)
            )  #  从1开始编号

            #  开门后的静态图片
            self.elevator_open_image.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_open_image[i].setGeometry(
                QtCore.QRect(
                    elevator_pos_x[i], elevator_pos_y[i], ELEV_ANIME_X, ELEV_ANIME_Y
                )
            )
            self.elevator_open_image[i].setPixmap(QtGui.QPixmap("resources/opened.png"))
            self.elevator_open_image[i].setVisible(True)  #  除了播放动画的时候均为静态图像显示
            self.elevator_open_image[i].setObjectName(
                "open_image_" + str(i + 1)
            )  #  从1开始编号

            #  关门后的静态图片
            self.elevator_close_image.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_close_image[i].setGeometry(
                QtCore.QRect(
                    elevator_pos_x[i], elevator_pos_y[i], ELEV_ANIME_X, ELEV_ANIME_Y
                )
            )
            self.elevator_close_image[i].setPixmap(
                QtGui.QPixmap("resources/closed.png")
            )
            self.elevator_close_image[i].setVisible(True)
            self.elevator_close_image[i].setObjectName(
                "close_image_" + str(i + 1)
            )  #  从1开始编号

            #  电梯状态上行
            self.elevator_ascending_animation.append(
                QtWidgets.QLabel(self.central_widget)
            )
            self.elevator_ascending_animation[i].setGeometry(
                QtCore.QRect(
                    elevator_status_pos_x[i],
                    elevator_status_pos_y[i],
                    ELEV_STATUS_X,
                    ELEV_STATUS_Y,
                )
            )
            self.elevator_ascending_animation[i].setMovie(
                QtGui.QMovie("resources/upArrow.gif")
            )
            self.elevator_ascending_animation[i].movie().setPaused(False)
            self.elevator_ascending_animation[i].setVisible(False)
            self.elevator_ascending_animation[i].setObjectName(
                "ascending_animation_" + str(i + 1)
            )  #  从1开始编号

            #  电梯状态下行
            self.elevator_descending_animation.append(
                QtWidgets.QLabel(self.central_widget)
            )
            self.elevator_descending_animation[i].setGeometry(
                QtCore.QRect(
                    elevator_status_pos_x[i],
                    elevator_status_pos_y[i],
                    ELEV_STATUS_X,
                    ELEV_STATUS_Y,
                )
            )
            self.elevator_descending_animation[i].setMovie(
                QtGui.QMovie("resources/downArrow.gif")
            )
            self.elevator_descending_animation[i].movie().setPaused(False)
            self.elevator_descending_animation[i].setVisible(False)
            self.elevator_descending_animation[i].setObjectName(
                "descending_animation_" + str(i + 1)
            )  #  从1开始编号

            #  电梯序号icon
            self.elevator_enumerate_image.append(QtWidgets.QLabel(self.central_widget))
            self.elevator_enumerate_image[i].setGeometry(
                QtCore.QRect(
                    elevator_enumerate_pos_x[i],
                    elevator_enumerate_pos_y[i],
                    ELEV_ENUM_X,
                    ELEV_ENUM_Y,
                )
            )
            filename = "resources/enumerate" + str(i + 1) + ".png"
            self.elevator_enumerate_image[i].setPixmap(QtGui.QPixmap(filename))
            self.elevator_enumerate_image[i].setVisible(True)
            self.elevator_enumerate_image[i].setObjectName(
                "enumerate_image_" + str(i + 1)
            )  #  从1开始编号

            #  同电梯序号icon，在repair处标识
            self.elevator_repair_enumerate_image.append(
                QtWidgets.QLabel(self.central_widget)
            )
            self.elevator_repair_enumerate_image[i].setGeometry(
                QtCore.QRect(
                    elevator_enumerate_repair_pos_x[i],
                    elevator_enumerate_repair_pos_y[i],
                    ELEV_ENUM_X,
                    ELEV_ENUM_Y,
                )
            )
            filename = "resources/enumerate" + str(i + 1) + ".png"
            self.elevator_repair_enumerate_image[i].setPixmap(QtGui.QPixmap(filename))
            self.elevator_repair_enumerate_image[i].setVisible(True)
            self.elevator_repair_enumerate_image[i].setObjectName(
                "repair_enumerate_image_" + str(i + 1)
            )  #  从1开始编号

            #  电梯楼层数码管
            self.elevator_floor.append(QtWidgets.QLCDNumber(self.central_widget))
            self.elevator_floor[i].setStyleSheet("")  # TODO 添加qss
            self.elevator_floor[i].setGeometry(
                QtCore.QRect(
                    elevator_floor_pos_x[i],
                    elevator_floor_pos_y[i],
                    ELEV_ENUM_X,
                    ELEV_ENUM_X,
                )
            )  #  同样的大小，不额外定义了
            self.elevator_floor[i].setFrameShadow(QtWidgets.QFrame.Raised)
            self.elevator_floor[i].setFrameShape(QtWidgets.QFrame.Box)
            self.elevator_floor[i].setDigitCount(2)
            self.elevator_floor[i].setMode(QtWidgets.QLCDNumber.Dec)
            self.elevator_floor[i].setSmallDecimalPoint(False)
            self.elevator_floor[i].setProperty("intValue", 1)
            self.elevator_floor[i].setObjectName("floor_" + str(i + 1))  #  从1开始编号

            #  设置电梯内部的楼层按钮
            self.elevator_floor_button.append([])
            for j in range(FLOOR_NUM):
                self.elevator_floor_button[i].append(
                    QtWidgets.QPushButton(self.central_widget)
                )

            #  电梯开门按钮
            self.elevator_door_open_button.append(
                QtWidgets.QPushButton(self.central_widget)
            )
            self.elevator_door_open_button[i].setStyleSheet("")  # TODO 加入qss
            self.elevator_door_open_button[i].setGeometry(
                QtCore.QRect(
                    elevator_open_pos_x[i],
                    elevator_open_pos_y[i],
                    DOOR_BUTTON_X,
                    DOOR_BUTTON_Y,
                )
            )
            self.elevator_door_open_button[i].setObjectName(
                "door_open_button_" + str(i + 1)
            )
            self.elevator_door_open_button[i].clicked.connect(
                MainWindow.doorOpenClicked
            )

            #  电梯关门按钮
            self.elevator_door_close_button.append(
                QtWidgets.QPushButton(self.central_widget)
            )
            self.elevator_door_close_button[i].setStyleSheet("")  #  TODO 加入qss
            self.elevator_door_close_button[i].setGeometry(
                QtCore.QRect(
                    elevator_close_pos_x[i],
                    elevator_close_pos_y[i],
                    DOOR_BUTTON_X,
                    DOOR_BUTTON_Y,
                )
            )
            self.elevator_door_close_button[i].setObjectName(
                "door_close_button_" + str(i + 1)
            )
            self.elevator_door_close_button[i].clicked.connect(
                MainWindow.doorCloseClicked
            )

            #  电梯报警按钮
            self.elevator_alarm_button.append(
                QtWidgets.QPushButton(self.central_widget)
            )
            self.elevator_alarm_button[i].setStyleSheet  #  TODO 加入qss
            self.elevator_alarm_button[i].setGeometry(
                QtCore.QRect(
                    elevator_alarm_pos_x[i],
                    elevator_alarm_pos_y[i],
                    DOOR_BUTTON_X,
                    DOOR_BUTTON_Y,
                )
            )
            self.elevator_alarm_button[i].setObjectName("elevator_alarm_" + str(i + 1))
            self.elevator_alarm_button[i].clicked.connect(MainWindow.alarmClicked)

            #  电梯修理按钮
            self.elevator_repair_button.append(
                QtWidgets.QPushButton(self.central_widget)
            )
            self.elevator_repair_button[i].setStyleSheet(loadQSS(""))  #  TODO 加入qss
            self.elevator_repair_button[i].setGeometry(
                QtCore.QRect(
                    elevator_repair_x[i],
                    elevator_repair_y[i],
                    ELEV_REPAIR_SIZE,
                    ELEV_REPAIR_SIZE,
                )
            )
            self.elevator_repair_button[i].setObjectName(
                "repair_button_" + str(i + 1)
            )  #  从1开始编号
            #  链接槽函数
            self.elevator_repair_button[i].clicked.connect(MainWindow.repairClicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    def doorOpenClicked(self):
        """电梯内部开门按钮触发"""
        _object = self.sender()
        elevator_i = int(_object.objectName()[-1])
        self.scheduler.responseDoorOpen(elevator_i)
        print("电梯" + str(elevator_i) + "内部开门")

    def doorCloseClicked(self):
        """电梯内部关门按钮触发"""
        _object = self.sender()
        elevator_i = int(_object.objectName()[-1])
        self.scheduler.responseDoorClose(elevator_i)
        print("电梯" + str(elevator_i) + "内部关门")

    def alarmClicked(self):
        """电梯报警按钮触发"""
        _object = self.sender()
        elevator_i = int(_object.objectName()[-1])
        self.scheduler.responseAlarm(elevator_i)
        print("电梯" + str(elevator_i) + "警报触发！")

    def repairClicked(self):
        """电梯修复触发"""
        _object = self.sender()
        elevator_i = int(_object.objectName()[-1])
        # self.scheduler.responseRepair(elevator_i)
        print("电梯" + str(elevator_i) + "已恢复正常！")


def loadQSS(path):
    """将读入的qss文件转为字符串

    Args:
        path (str): qss文件路径

    Returns:
        str: 字符串格式的StyleSheet
    """
    if len(path):
        with open(path, "r") as f:
            return f.read()