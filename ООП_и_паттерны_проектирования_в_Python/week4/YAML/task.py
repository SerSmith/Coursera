Описание задания
Важное замечание! В материалах лекции и тестовой системе используется версия PyYaml 3.13. Использование более поздних версий приведет к ошибкам при запуске кода из материалов лекции и при проверке решения грейдером.

Вам необходимо модифицировать приложенный код так, чтобы  два следующих кода были эквивалентны (приводили к одинаковому результату)

Levels = yaml.load(
'''
levels:
    - !easy_level {}
    - !medium_level
        enemy: ['rat']
    - !hard_level
        enemy:
            - rat
            - snake
            - dragon
        enemy_count: 10
''')

Levels = {'levels':[]}
_map = EasyLevel.Map()
_obj = EasyLevel.Objects()
Levels['levels'].append({'map': _map, 'obj': _obj})

_map = MediumLevel.Map()
_obj = MediumLevel.Objects()
_obj.config = {'enemy':['rat']}
Levels['levels'].append({'map': _map, 'obj': _obj})

_map = HardLevel.Map()
_obj = HardLevel.Objects()
_obj.config = {'enemy': ['rat', 'snake', 'dragon'], 'enemy_count': 10}
Levels['levels'].append({'map': _map, 'obj': _obj})

То есть в

Исходный код:

import random
import yaml
from abc import ABC


class AbstractLevel(yaml.YAMLObject):

    @classmethod
    def get_map(cls):
        return cls.Map()

    @classmethod
    def get_objects(cls):
        return cls.Objects()

    class Map(ABC):
        pass

    class Objects(ABC):
        pass


class EasyLevel(AbstractLevel):
    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(5)] for _ in range(5)]
            for i in range(5):
                for j in range(5):
                    if i == 0 or j == 0 or i == 4 or j == 4:
                        self.Map[j][i] = -1  # граница карты
                    else:
                        self.Map[j][i] = random.randint(0, 2)  # случайная характеристика области

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = [('next_lvl', (2, 2))]
            self.config = {}

        def get_objects(self, _map):
            for obj_name in ['rat']:
                coord = (random.randint(1, 3), random.randint(1, 3))
                intersect = True
                while intersect:
                    intersect = False
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(1, 3), random.randint(1, 3))

                self.objects.append((obj_name, coord))

            return self.objects


class MediumLevel(AbstractLevel):
    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(8)] for _ in range(8)]
            for i in range(8):
                for j in range(8):
                    if i == 0 or j == 0 or i == 7 or j == 7:
                        self.Map[j][i] = -1  # граница карты
                    else:
                        self.Map[j][i] = random.randint(0, 2)  # случайная характеристика области

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = [('next_lvl', (4, 4))]
            self.config = {'enemy': []}

        def get_objects(self, _map):
            for obj_name in self.config['enemy']:
                coord = (random.randint(1, 6), random.randint(1, 6))
                intersect = True
                while intersect:
                    intersect = False
                    for obj in self.objects:
                        if coord == obj[1]:
                            intersect = True
                            coord = (random.randint(1, 6), random.randint(1, 6))

                self.objects.append((obj_name, coord))

            return self.objects


class HardLevel(AbstractLevel):
    class Map:
        def __init__(self):
            self.Map = [[0 for _ in range(10)] for _ in range(10)]
            for i in range(10):
                for j in range(10):
                    if i == 0 or j == 0 or i == 9 or j == 9:
                        self.Map[j][i] = -1  # граница карты :: непроходимый участок карты
                    else:
                        self.Map[j][i] = random.randint(-1, 8)  # случайная характеристика области

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = [('next_lvl', (5, 5))]
            self.config = {'enemy_count': 5, 'enemy': []}

        def get_objects(self, _map):
            for obj_name in self.config['enemy']:
                for tmp_int in range(self.config['enemy_count']):
                    coord = (random.randint(1, 8), random.randint(1, 8))
                    intersect = True
                    while intersect:
                        intersect = False
                        if _map[coord[0]][coord[1]] == -1:
                            intersect = True
                            coord = (random.randint(1, 8), random.randint(1, 8))
                            continue
                        for obj in self.objects:
                            if coord == obj[1]:
                                intersect = True
                                coord = (random.randint(1, 8), random.randint(1, 8))

                    self.objects.append((obj_name, coord))

            return self.objects



AQ. Частые вопросы, возникающие при решении задания "Парсинг YAML-файла".
Valeriy ShagurTeaching StaffAssignment: Парсинг YAML-файла · 2 years ago · Edited
FAQ. Частые вопросы, возникающие при решении задания "Парсинг YAML-файла".

(прикреплено, обновляемая ветка)

1. Какие дополнительные материалы могут помочь при решении данного задания?

1). Документация PyYAML 2). Статья с описанием синтаксиса Yaml 3). Статья на хабре "Некоторые приемы YAML."

2. Почему код решения падает, если установлена более поздняя версия библиотеки PyYaml?

Потому что изменилось API самой библиотеки, подробности -  здесь и здесь.

3. Не очень понимаю, что надо сделать: исправить первые два кода или дописать третий? 

Вам необходимо отредактировать третий блок кода (добавить возможность создания объектов с помощью yaml). Во втором блоке кода описаны действия по созданию объектов, из него можно понять какие объекты должны создаваться и какой тип данных должен быть возвращен. В первом блоке кода указана строка и способ создания объектов с использованием yaml. Ваше решение должно возвращать одинаковый результат при выполнении первого и второго блока. 

4. Нужно ли загружать приведенный в примере yaml? 

Нет не нужно, решение должно содержать только модифицированную версию кода из блока 3. 

5. У меня проблемы с пониманием процесса создания объектов с использованием yaml, не могли бы вы пояснить? А то совсем запутался.

Постараюсь коротко пояснить. Когда происходит загрузка (по существу создание объектов на основании yaml), используются уже определенные конструкторы типов данных (например: для списков, чисел , словарей). Если мы определили свой класс в коде, то мы не сможем использовать указание на него в yaml файле, так конструктор для него отсутствует.  Для исправления этой ситуации возможны два варианта:

первый - не изменяя определения пользовательского класса (не внося изменения в код нашего класса), определить функцию конструктор, которая будет загружать данные и на основе их создавать экземпляр необходимого типа данных и возвращать его. Далее, эту созданную функцию нужно зарегистрировать (добавить к существующим конструкторам) с помощью функции add_constructor.

второй - добавить в реализацию класса нужного нам типа данных (в код нашего класса), атрибут класса yaml_tag и метод класса с названием from_yaml, который по существу делает тоже самое, что и функция конструктор из первого варианта. При этом нужно соблюсти еще одно условие - класс должен наследоваться от  yaml.YAMLObject.

Вот пара примеров:

# демонстрация загрузки yaml по первому варианту
# важное замечание версия PyYAML - 3.13
import yaml


# класс определяющий пользовательский тип данных
class ExampleClass:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'ExampleClass, value - {self.value}'


# функция конструктор для типа данных ExampleClass
def constuctor_example_class(loader, node):
    # получаем данные из yaml
    value = loader.construct_mapping(node)
    # необходимо выбрать из полученные данных необходимые
    # для создания экземпляра класса ExampleClass
    return ExampleClass(*value)


# регистрируем конструктор
yaml.add_constructor('!example_class', constuctor_example_class)
# yaml строка
document = """!example_class {5}"""
# выполняем загрузку
obj = yaml.load(document)
# выведем полученный объект, ожидаем строку
# ExampleClass, value - 5


# демонстрация загрузки yaml по второму варианту
# важное замечание версия PyYAML - 3.13
import yaml


# класс определяющий пользовательский тип данных
class ExampleClass(yaml.YAMLObject):  # <-- добавим родительский класс yaml.YAMLObject
    yaml_tag = '!example_class'  # <-- добавим тег

    @classmethod
    def from_yaml(cls, loader, node):  # <-- добавим метод класса from_yaml
        # получаем данные из yaml
        value = loader.construct_mapping(node)
        # необходимо выбрать из полученные данных необходимые
        # для создания экземпляра класса ExampleClass
        return ExampleClass(*value)

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'ExampleClass, value - {self.value}'


# yaml строка
document = """!example_class {7}"""
# выполняем загрузку
obj = yaml.load(document)
# выведем полученный объект, ожидаем строку
# ExampleClass, value - 7
print(obj)
