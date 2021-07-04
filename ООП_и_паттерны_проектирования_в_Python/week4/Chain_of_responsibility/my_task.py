from abc import ABC, abstractmethod


class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class Event(ABC):
    @abstractmethod
    def get_action(self):
        pass


class EventGet(Event):
    def __init__(self, type_):
        self.type = type_

    def get_action(self):
        return 'get'


class EventSet(Event):
    def __init__(self, value):
        self.type = type(value)
        self.value = value

    def get_action(self):
        return 'set'


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)

    def base_action(self, type, obj, event):
        if event.get_action() == 'get':
            return value
        elif event.get_action() == 'set':
            value = event.value


class IntHandler(NullHandler):
    def handle(self, obj, event):
        if event.type == int:
            if event.get_action() == 'get':
                return obj.integer_field
            elif event.get_action() == 'set':
                obj.integer_field = event.value
        else:
            print("Передаю обработку дальше")
            return super().handle(obj, event)


class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if event.type == float:
            if event.get_action() == 'get':
                return obj.float_field
            elif event.get_action() == 'set':
                obj.float_field = event.value
        else:
            print("Передаю обработку дальше")
            return super().handle(obj, event)


class StrHandler(NullHandler):
    def handle(self, obj, event):
        if event.type == str:
            if event.get_action() == 'get':
                return obj.string_field
            elif event.get_action() == 'set':
                obj.string_field = event.value
        else:
            print("Передаю обработку дальше")
            return super().handle(obj, event)
