from ui import *


class Scheduler(object):
    """电梯调度类 主要包含了内调度和外调度

    Args:
        object (object): The most base type
    """

    def __init__(self, main_window):
        self.main_window = main_window

        #  电梯状态的设置
        #  电梯门的状态
        self.elevator_door_status = [DOOR_CLOSED for i in range(ELEV_NUM)]
        #  电梯运行的状态
        self.elevator_movement_status = [HALT for i in range(ELEV_NUM)]
        #  电梯所处的楼层
        self.elevator_floor = [1 for i in range(ELEV_NUM)]
        #  电梯是否在播放动画 0为无 1为开门 2为关门
        self.elevator_playing_animation = [0 for i in range(ELEV_NUM)]

        #  队列的定义
        #  电梯内部顺路任务队列
        self.task_queue = [[] for i in range(ELEV_NUM)]

        #  电梯内部不顺路任务队列
        self.inverse_task_queue = [[] for i in range(ELEV_NUM)]

        #  定时器，用于控制更新电梯状态的间隔
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateSystemStatus)
        self.timer.start(1000)  #  单位为毫秒


    #  各种槽函数
    def responseDoorOpen(self, elevator_i:int):
        """响应电梯内部开门命令

        Args:
            elevator_i (int): 第elevator_i个电梯内部按下开门按钮
        """
        if self.elevator_movement_status[elevator_i]==    HALT:


    #  电梯内调度
    def innerScheduler(self, elevator_i):
        pass