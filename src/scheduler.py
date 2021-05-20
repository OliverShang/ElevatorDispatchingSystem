from PyQt5.QtWidgets import QFileIconProvider
from ui import *
import ui


class Scheduler(object):
    """电梯调度类 主要包含了内调度和外调度

    Args:
        object (object): The most base type
    """

    def __init__(self, main_window):
        self.main_window = main_window

        #  电梯状态的设置
        #  电梯门的状态
        self.elevator_door_status = [ui.DOOR_CLOSED for i in range(ui.ELEV_NUM)]
        #  电梯运行的状态
        self.elevator_movement_status = [ui.HALT for i in range(ui.ELEV_NUM)]
        #  电梯所处的楼层
        self.elevator_floor = [1 for i in range(ui.ELEV_NUM)]
        #  电梯是否在播放动画 0为无 1为开门 2为关门
        self.elevator_playing_animation = [0 for i in range(ui.ELEV_NUM)]

        #  队列的定义
        #  电梯内部顺路任务队列
        self.task_queue = [[] for i in range(5)]

        #  电梯内部不顺路任务队列
        self.inverse_task_queue = [[] for i in range(5)]

        #  定时器，用于控制更新电梯状态的间隔
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateSystemStatus)
        self.timer.start(1000)  #  单位为毫秒

    #  各种槽函数
    #  TODO 修复开关门卡动画
    def responseDoorOpen(self, elevator_i: int):
        """响应电梯内部开门命令

        Args:
            elevator_i (int): 电梯编号
        """
        if (
            self.elevator_movement_status[elevator_i] == ui.HALT
            or self.elevator_movement_status[elevator_i] == ui.MALFUNCTION
        ) and self.elevator_door_status[
            elevator_i
        ] == ui.DOOR_CLOSED:  #  如果故障只能开门不能关上
            self.main_window.playDoorOpenAnimation(elevator_i)
            self.elevator_door_status[elevator_i] = ui.DOOR_OPENED
            #  1s后自动关门
            #  Timers cannot be started from another thread,在updateSystemStatus完成自动关门
            # thread = threading.Timer(1, self.responseDoorClose, args=(elevator_i,))
            # thread.start()

    def responseDoorClose(self, elevator_i: int):
        """相应电梯内部关门命令

        Args:
            elevator_i (int): [description]
        """
        if (
            self.elevator_movement_status[elevator_i] == ui.HALT
            and self.elevator_door_status[elevator_i] == ui.DOOR_OPENED
        ):
            self.main_window.playDoorCloseAnimation(elevator_i)
            self.elevator_door_status[elevator_i] = ui.DOOR_CLOSED

    def responseAlarm(self, elevator_i: int):
        """响应电梯触发警报命令

        Args:
            elevator_i (int): 电梯编号
        """
        if self.elevator_movement_status[elevator_i] == ui.HALT:
            self.elevator_movement_status[elevator_i] = ui.MALFUNCTION
            for button in self.main_window.elevator_floor_button[elevator_i]:
                button.setEnabled(False)
            self.main_window.playDoorOpenAnimation(elevator_i)
            ui.ELEV_NUM -= 1

    def responseRepair(self, elevator_i: int):
        """响应电梯修复命令

        Args:
            elevator_i (int): 电梯编号
        """
        if self.elevator_movement_status[elevator_i] == ui.MALFUNCTION:
            self.elevator_movement_status[elevator_i] = ui.HALT
            for button in self.main_window.elevator_floor_button[elevator_i]:
                button.setEnabled(True)
            ui.ELEV_NUM += 1
        else:
            print("第" + str(elevator_i) + "号电梯正常，无需修复")

    def responseFloorButton(self, elevator_i: int, floor_j: int):
        """电梯内调度函数

        Args:
            elevator_i (int): 电梯编号
            floor_j (int): 楼层编号
        """
        if self.elevator_movement_status[elevator_i] == ui.MALFUNCTION:
            print("第" + str(elevator_i + 1) + "号电梯出现故障无法前往！")

        elif self.elevator_movement_status[elevator_i] == ui.HALT:
            if self.elevator_floor[elevator_i] != floor_j:
                self.task_queue[elevator_i].append(floor_j)
            else:  #  当前楼层
                if self.elevator_door_status[elevator_i] == ui.DOOR_CLOSED:
                    self.main_window.playDoorOpenAnimation(elevator_i)
        elif self.elevator_floor[elevator_i] > floor_j:
            if self.elevator_movement_status[elevator_i] == ui.ASCENDING:
                self.inverse_task_queue[elevator_i].append(floor_j)
                self.inverse_task_queue[elevator_i].sort(reverse=True)
            elif self.elevator_movement_status[elevator_i] == ui.DESCENDING:
                self.task_queue[elevator_i].append(floor_j)
                self.task_queue[elevator_i].sort(reverse=True)
        elif self.elevator_floor[elevator_i] < floor_j:
            if self.elevator_movement_status[elevator_i] == ui.ASCENDING:
                self.task_queue[elevator_i].append(floor_j)
                self.task_queue[elevator_i].sort()
            elif self.elevator_movement_status[elevator_i] == ui.DESCENDING:
                self.inverse_task_queue[elevator_i].append(floor_j)
                self.inverse_task_queue[elevator_i].sort()

    def calculateDistance(self, floor_j: int, direction: int):

        """计算外调度最优距离

        Args:
            floor_j (int): 楼层编号
            direction (int): 方向为向上or向下

        Returns:
            tuple: (距离最优的电梯编号-1代表所有电梯都故障,最优距离)
        """
        distance = [999 for i in range(ui.ELEV_NUM)]
        for elevator_i in range(ui.ELEV_NUM):
            if self.elevator_movement_status[elevator_i] != ui.MALFUNCTION:
                #  上升电梯
                if (
                    self.elevator_movement_status[elevator_i] == ui.ASCENDING
                    and floor_j > self.elevator_floor[elevator_i]
                    and direction == ui.UP
                ):
                    distance[elevator_i] = floor_j - self.elevator_floor[elevator_i]
                #  下降or静止电梯
                elif (
                    self.elevator_movement_status[elevator_i] == ui.DESCENDING
                    and floor_j < self.elevator_floor[elevator_i]
                    and direction == ui.DOWN
                ) or self.elevator_movement_status[elevator_i] == ui.HALT:
                    distance[elevator_i] = abs(
                        self.elevator_floor[elevator_i] - floor_j
                    )
            else:
                distance[elevator_i] = 9999
        res = distance.index(min(distance))
        if res == 9999:
            return (-1, distance[res])
        return (res, distance[res])

    def responseExternalButton(self, floor_j: int, direction: int):
        """电梯外部调度函数

        Args:
            floor_j (int): 楼层
            direction (int): 上行or下行
        """
        elevator_i, distance = self.calculateDistance(floor_j, direction)
        if elevator_i != -1:
            if distance == 0:
                # self.responseDoorOpen(elevator_i)
                # self.elevator_movement_status[elevator_i] = ui.HALT
                self.main_window.playDoorOpenAnimation(elevator_i)
                # self.main_window.
                if direction == ui.UP:
                    self.main_window.external_up_button[floor_j].setEnabled(True)
                elif direction == ui.DOWN:
                    self.main_window.external_down_button[floor_j].setEnabled(True)
            else:
                self.task_queue[elevator_i].append(floor_j)
                #  TODO 设置成不同的样式，disable按钮

        else:
            print("所有电梯都出现故障，无法进行调度！")

    def updateSystemStatus(self):
        """每秒更新系统状态"""
        #  自动关门
        for elevator_i in range(ui.ELEV_NUM):
            if (
                self.elevator_playing_animation[elevator_i] == 0
                and self.elevator_door_status[elevator_i] == ui.DOOR_OPENED
                and self.elevator_movement_status[elevator_i] != ui.MALFUNCTION
            ):
                self.main_window.playDoorCloseAnimation(elevator_i)

            self.main_window.playArrowAnimation(
                elevator_i, self.elevator_movement_status[elevator_i]
            )

            #  处理任务队列
            if len(self.task_queue[elevator_i]) > 0:
                if self.elevator_movement_status[elevator_i] == ui.HALT:
                    if self.elevator_floor[elevator_i] > self.task_queue[elevator_i][0]:
                        self.elevator_movement_status[elevator_i] = ui.DESCENDING
                    elif (
                        self.elevator_floor[elevator_i] < self.task_queue[elevator_i][0]
                    ):
                        self.elevator_movement_status[elevator_i] = ui.ASCENDING
                else:
                    if self.elevator_floor[elevator_i] < self.task_queue[elevator_i][0]:
                        self.elevator_movement_status[elevator_i] = ui.ASCENDING
                        self.elevator_floor[elevator_i] = (
                            self.elevator_floor[elevator_i] + 1
                        )
                        self.main_window.elevator_floor[elevator_i].setProperty(
                            "intValue", self.elevator_floor[elevator_i]
                        )
                    elif (
                        self.elevator_floor[elevator_i] > self.task_queue[elevator_i][0]
                    ):
                        self.elevator_movement_status[elevator_i] = ui.DESCENDING
                        self.elevator_floor[elevator_i] = (
                            self.elevator_floor[elevator_i] - 1
                        )
                        self.main_window.elevator_floor[elevator_i].setProperty(
                            "intValue", self.elevator_floor[elevator_i]
                        )
                    #  电梯到达目的地的
                    else:
                        self.elevator_movement_status[elevator_i] = ui.HALT
                        print("第" + str(elevator_i + 1) + "号电梯已到达目的地")
                        self.main_window.playDoorOpenAnimation(elevator_i)
                        # self.responseDoorOpen(elevator_i)
                        self.main_window.elevator_floor[elevator_i].setProperty(
                            "intValue", self.elevator_floor[elevator_i]
                        )
                        self.task_queue[elevator_i].pop(0)
            else:
                if len(self.inverse_task_queue[elevator_i]) > 0:
                    self.task_queue = list(self.inverse_task_queue)
                    self.inverse_task_queue.clear()
