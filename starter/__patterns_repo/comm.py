from typing import Optional
from abc import ABC, abstractmethod

class Command(ABC):

    @property
    def room(self):
        return self._room

    def __init__(self, room):
        self._room = room

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class LightOn(Command):

    def execute(self):
        self._room.light["status"] = 1

    def undo(self):
        self._room.light["status"] = 0

class LightOff(Command):
    def execute(self):
        self._room.light["status"] = 0

    def undo(self):
        self._room.light["status"] = 1

class LightUp(Command):
    def execute(self):
        if(self._room.light["status"] == 0):
            raise Exception("Light is off. Cannot increase brightness.")
        self._room.light["value"] += 1

    def undo(self):
        if(self._room.light["status"] == 0):
            raise Exception("Light is off. Cannot decrease brightness.")
        self._room.light["value"] -= 1


class LightDown(Command):
    def execute(self):
        if(self._room.light["status"] == 0):
            raise Exception("Light is off. Cannot decrease brightness.")
        self._room.light["value"] -= 1

    def undo(self):
        if(self._room.light["status"] == 0):
            raise Exception("Light is off. Cannot increase brightness.")
        self._room.light["value"] += 1




class FanOn(Command):
    def execute(self):
        self._room.fan["status"] = 1

    def undo(self):
        self._room.fan["status"] = 0


class FanOff(Command):
    def execute(self):
        self._room.fan["status"] = 0

    def undo(self):
        self._room.fan["status"] = 1



class FanUp(Command):
    def execute(self):
        if(self._room.fan["status"] == 0):
            raise Exception("Fan is off. Cannot increase speed.")
        self._room.fan["value"] += 1

    def undo(self):
        if(self._room.fan["status"] == 0):
            raise Exception("Fan is off. Cannot decrease speed.")
        self._room.fan["value"] -= 1

class FanDown(Command):
    def execute(self):
        if(self._room.fan["status"] == 0):
            raise Exception("Fan is off. Cannot decrease speed.")
        self._room.fan["value"] -= 1

    def undo(self):
        if(self._room.fan["status"] == 0):
            raise Exception("Fan is off. Cannot increase speed.")
        self._room.fan["value"] += 1



class Room:
    def __init__(self):
        self.light = {"status": 0, "value": 0}
        self.fan = {"status": 0, "value": 0}



class Controller:
    def __init__(self):
        self._history: list[Command] = []

    def execute_command(self, command: Command):
        command.execute()
        self._history.append(command)
        return self

    def undo_last_command(self):
        if self._history:
            last_command = self._history.pop()
            last_command.undo()

    def redo_last_command(self):
        if self._history:
            last_command = self._history[-1]
            last_command.execute()


