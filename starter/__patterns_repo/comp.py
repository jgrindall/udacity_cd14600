from abc import ABC, abstractmethod

class FSEntry(ABC):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    @abstractmethod
    def get_size(self):
        pass


class FSLeaf(FSEntry):
    def __init__(self, name, size):
        super().__init__(name)
        self.size = size

    def get_size(self):
        return self.size


class FSFolder(FSEntry):
    def __init__(self, name):
        super().__init__(name)
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def get_size(self):
        total_size = 0
        for entry in self.entries:
            total_size += entry.get_size()
        return total_size