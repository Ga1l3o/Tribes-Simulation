from abc import ABC, abstractmethod
from config import *

class Unit(ABC):
    """Abstrakcyjna klasa bazowa dla jednostek (wojowników oraz robotników)"""

    def __init__(self, tribe):
        self._tribe = tribe  # hermetyzacja - plemię przypisane do jednostki

    # Property ukrywa, że jest to wywołanie metody dla klas wywołujących tribe
    @property
    def tribe(self):
        return self._tribe

    @abstractmethod
    def food_consumption(self):
        pass


class Worker(Unit):
    """Klasa robotnika dziedzicząca z klasy Unit"""

    def food_consumption(self):
        return WORKER_FOOD_CONSUMPTION


class Warrior(Unit):
    """Klasa wojownika z mechanizmem ulepszania dziedzicząca z klasy Unit"""

    def __init__(self, tribe, level=1):
        super().__init__(tribe)
        self._level = level  # hermetyzacja - poziom wojownika
        self._strength = BASE_WARRIOR_STRENGTH + (level - 1) * UPGRADE_STRENGTH_BONUS

    @property
    def level(self):
        return self._level

    @property
    def strength(self):
        return self._strength

    def food_consumption(self):
        return WARRIOR_FOOD_CONSUMPTION

    def upgrade(self):
        """Ulepsz wojownika jeśli to możliwe"""
        if self._level < MAX_WARRIOR_LEVEL:
            self._level += 1
            self._strength += UPGRADE_STRENGTH_BONUS
            return True
        return False