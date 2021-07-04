from abc import ABC, abstractmethod

# ObservableEngine, AbstractObserver , ShortNotificationPrinter, FullNotificationPrinter
class ObservableEngine(Engine):
    def __init__(self): 
        self.__subscribers = set() # При инициализации множество подписчиков задается пустым
    
    def subscribe(self, subscriber):
        self.__subscribers.add(subscriber) # Для того чтобы подписать пользователя, он добавляется во множество подписчиков
        
    def unsubscribe(self, subscriber):
        self.__subscribers.remove(subscriber) # Удаление подписчика из списка
        
    def notify(self, message):
        for subscriber in self.__subscribers:
            subscriber.update(message) # Отправка уведомления всем подписчикам


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, achievment):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set([])
    
    def update(self, achievment):
        self.achievements.add(achievment['title'])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list([])
    
    def update(self, achievment):
        if achievment not in self.achievements:
            self.achievements.append(achievment)

