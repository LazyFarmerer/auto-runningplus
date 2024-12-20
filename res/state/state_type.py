from enum import Enum, auto

class 러닝플러스StateType(Enum):
        초기세팅 = auto()
        나의학습실 = auto()
        중간창 = auto()
        학습중_넘기기 = auto()
        학습중_퀴즈 = auto()
        학습중_대기하기 = auto()