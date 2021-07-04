from abc import ABC, abstractmethod


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base
    
    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass



class AbstractPositive(AbstractEffect):


    def get_negative_effects(self):
        return self.base.get_negative_effects()


class AbstractNegative(AbstractEffect):
    def get_positive_effects(self):
        return self.base.get_positive_effects()


class Berserk(AbstractPositive):
    """Увеличивает характеристики: Сила, Выносливость, Ловкость, Удача на 7;
       уменьшает характеристики: Восприятие, Харизма, Интеллект на 3;
       количество единиц здоровья увеличивается на 50.
    """

    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Berserk']
    
    def get_stats(self):
        return_stats = self.base.get_stats()
        return_stats['Strength'] += 7
        return_stats['Endurance'] += 7
        return_stats['Agility'] += 7
        return_stats['Luck'] += 7

        return_stats['Perception'] -= 3
        return_stats['Intelligence'] -= 3
        return_stats['Charisma'] -= 3

        return_stats["HP"] += 50

        return return_stats


class Blessing(AbstractPositive):
    """увеличивает все основные характеристики на 2.
    К основным характеристикам относятся: Сила (Strength),
    Восприятие (Perception), Выносливость (Endurance), Харизма (Charisma),
    Интеллект (Intelligence), Ловкость (Agility), Удача (Luck).
    """

    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['Blessing']
    
    def get_stats(self):
        return_stats = self.base.get_stats()
        return_stats['Strength'] += 2
        return_stats['Endurance'] += 2
        return_stats['Agility'] += 2
        return_stats['Luck'] += 2
        return_stats['Perception'] += 2
        return_stats['Intelligence'] += 2
        return_stats['Charisma'] += 2

        return return_stats
    

class Weakness(AbstractNegative):
    """уменьшает характеристики: Сила, Выносливость, Ловкость на 4.
    """

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Weakness']
    
    def get_stats(self):
        return_stats = self.base.get_stats()
        return_stats['Strength'] -= 4
        return_stats['Endurance'] -= 4
        return_stats['Agility'] -= 4

        return return_stats


class Curse(AbstractNegative):
    """уменьшает все основные характеристики на 2.
    """

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['Curse']
    
    def get_stats(self):
        return_stats = self.base.get_stats()
        return_stats['Strength'] -= 2
        return_stats['Endurance'] -= 2
        return_stats['Agility'] -= 2
        return_stats['Luck'] -= 2
        return_stats['Perception'] -= 2
        return_stats['Intelligence'] -= 2
        return_stats['Charisma'] -= 2

        return return_stats


class EvilEye(AbstractNegative):
    """уменьшает  характеристику Удача на 10.
    """

    def get_negative_effects(self):
        return self.base.get_negative_effects() + ['EvilEye']
    
    def get_stats(self):
        return_stats = self.base.get_stats()
        return_stats['Luck'] -= 10

        return return_stats