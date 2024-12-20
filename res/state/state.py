from typing import Dict, TypeVar, Generic
from enum import Enum
from abc import ABCMeta, abstractmethod

from ..util.util import Util

# 안써도 되는 제네릭 굳이 쓰는이유
# 서로가 서로를 참조하니 순환참조 오류가 발생해서 -_ -;

T = TypeVar("T")

class State(Generic[T], metaclass=ABCMeta):
    def __init__(self, obj: T) -> None:
        self.obj = obj
        self.util = Util()

    @abstractmethod
    def enter(self) -> None:
        pass
    @abstractmethod
    def execute(self) -> None:
        pass
    @abstractmethod
    def exit(self) -> None:
        pass

T1 = TypeVar("T1", bound=Enum)

class StateMachine(Generic[T1]):
    def __init__(self, state_dic: Dict[T1, State]) -> None:
        self.__state_dic = state_dic
        self.curr_state: State
        for state_type in state_dic:
            self.curr_state = state_dic[state_type]
            self.curr_state.enter()
            break

    def setState(self, state_type: T1):
        self.curr_state.exit()
        self.curr_state = self.__state_dic[state_type]
        self.curr_state.enter()

    def execute(self):
        self.curr_state.execute()

    def changeState(self, state_type: T1, state: State):
        self.__state_dic[state_type] = state