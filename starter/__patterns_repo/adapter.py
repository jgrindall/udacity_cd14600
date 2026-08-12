from typing import Optional
from abc import ABC, abstractmethod
class ESocket:
    def plug_in(self):
        print("plugging in ESocket")
        return 120


class APlug(ABC):
    @abstractmethod
    def connect(self):
        pass

class USPlug(APlug):
    def connect(self):
        print("connecting USPPlug")
        pass


class Adapter(APlug):
    adaptee: Optional[ESocket] = None

    def __init__(self, adaptee: Optional[ESocket] = None):
        self.adaptee = adaptee

    def set_adaptee(self, adaptee: ESocket):
        self.adaptee = adaptee

    def connect(self):
        if self.adaptee is not None:
            return self.adaptee.plug_in()


