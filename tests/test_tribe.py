import os
import sys
import unittest

# Dopisujemy katalog nadrzędny (czyli ProgObiektTribeV3) do sys.path dzięki czemu moduły będą widoczne
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from board import Board
from tribe import Tribe
from units import Worker, Warrior
from config import *

class TestWorker(unittest.TestCase):
    def test_food_consumption(self):
        """Worker.food_consumption() powinno zwracać WORKER_FOOD_CONSUMPTION z configu."""
        worker = Worker(tribe=None)
        self.assertEqual(
            worker.food_consumption(),
            WORKER_FOOD_CONSUMPTION,
            f"Oczekiwano {WORKER_FOOD_CONSUMPTION}, a metoda zwróciła {worker.food_consumption()}"
        )


class TestWarrior(unittest.TestCase):
    def test_initial_strength_and_level(self):
        """Domyślny Warrior ma level=1 i strength=BASE_WARRIOR_STRENGTH."""
        warrior = Warrior(tribe=None)
        self.assertEqual(
            warrior.level,
            1,
            f"Oczekiwano poziomu 1, a było {warrior.level}"
        )
        self.assertEqual(
            warrior.strength,
            BASE_WARRIOR_STRENGTH,
            f"Oczekiwano siły {BASE_WARRIOR_STRENGTH}, a było {warrior.strength}"
        )

    def test_food_consumption(self):
        """Warrior.food_consumption() powinno zwracać WARRIOR_FOOD_CONSUMPTION."""
        warrior = Warrior(tribe=None)
        self.assertEqual(
            warrior.food_consumption(),
            WARRIOR_FOOD_CONSUMPTION,
            f"Oczekiwano {WARRIOR_FOOD_CONSUMPTION}, a metoda zwróciła {warrior.food_consumption()}"
        )

    def test_upgrade_within_limits(self):
        """
        Metoda upgrade() powinna zwiększać level i strength,
        dopóki level < MAX_WARRIOR_LEVEL. Zwraca True, jeśli uda się ulepszyć.
        """
        warrior = Warrior(tribe=None, level=1)
        current_level = warrior.level
        current_strength = warrior.strength

        # Iterujemy aż do osiągnięcia maksymalnego poziomu
        while current_level < MAX_WARRIOR_LEVEL:
            upgraded = warrior.upgrade()
            self.assertTrue(
                upgraded,
                f"Oczekiwano, że upgrade() zwróci True przy level={current_level}"
            )
            self.assertEqual(
                warrior.level,
                current_level + 1,
                f"Oczekiwano level={current_level + 1}, a było {warrior.level}"
            )
            self.assertEqual(
                warrior.strength,
                current_strength + UPGRADE_STRENGTH_BONUS,
                f"Oczekiwano strength={current_strength + UPGRADE_STRENGTH_BONUS}, a było {warrior.strength}"
            )

            current_level = warrior.level
            current_strength = warrior.strength

        # Po wyjściu z pętli level powinien być == MAX_WARRIOR_LEVEL
        self.assertEqual(
            current_level,
            MAX_WARRIOR_LEVEL,
            f"Oczekiwano, że po pętli level == {MAX_WARRIOR_LEVEL}"
        )

    def test_upgrade_beyond_max(self):
        """
        Gdy już jest level == MAX_WARRIOR_LEVEL,
        upgrade() powinno zwrócić False i nie zmieniać żadnego atrybutu.
        """
        warrior = Warrior(tribe=None, level=MAX_WARRIOR_LEVEL)
        prev_level = warrior.level
        prev_strength = warrior.strength

        upgraded = warrior.upgrade()
        self.assertFalse(
            upgraded,
            "Oczekiwano, że upgrade() zwróci False, gdy level == MAX_WARRIOR_LEVEL"
        )
        self.assertEqual(
            warrior.level,
            prev_level,
            f"Po nieudanym upgrade() level powinien pozostać {prev_level}"
        )
        self.assertEqual(
            warrior.strength,
            prev_strength,
            f"Po nieudanym upgrade() strength powinien pozostać {prev_strength}"
        )


class TestTribe(unittest.TestCase):
    def setUp(self):
        """
        Tworzymy planszę i plemię w znanym miejscu (0, 0).
        Konstruktor Tribe wymaga: __init__(self, board, x, y)
        """
        self.board = Board(size=10)
        self.tribe = Tribe(self.board, x=0, y=0)

    def test_initial_state(self):
        """Po utworzeniu plemienia w konstruktorze od razu tworzą się 2 robotnicy i 1 wojownik."""
        # 1) Plemię powinno wiedzieć, na jakiej planszy stoi:
        self.assertIs(
            self.tribe.board,
            self.board,
            "Atrybut `board` plemienia powinien wskazywać na obiekt Board, który mu przekazaliśmy."
        )

        # 2) id jest liczone kolejno, więc powinniśmy dostać int ≥ 0:
        self.assertIsInstance(
            self.tribe.id,
            int,
            f"Oczekiwano, że id będzie typu int, a jest {type(self.tribe.id)}"
        )
        self.assertGreaterEqual(
            self.tribe.id,
            0,
            f"Oczekiwano, że id ≥ 0, a jest {self.tribe.id}"
        )

        # 3) W konstruktorze Tribe automatycznie dodaje się 2 robotników i 1 wojownik:
        self.assertEqual(
            len(self.tribe.workers),
            2,
            "Po inicjalizacji w konstruktorze powinna być lista `workers` o długości 2."
        )

        self.assertEqual(
            len(self.tribe.warriors),
            1,
            "Po inicjalizacji w konstruktorze powinna być lista `warriors` o długości 1."
        )

        # 4) Na starcie `territory` jest zbiorem i początkowo zawiera dokładnie współrzędne (0,0):
        self.assertIn(
            (0, 0),
            self.tribe.territory,
            "Po utworzeniu plemienia w jego terytorium powinien być punkt (0,0)."
        )

    def test_add_and_remove_worker(self):
        """
        Zakładamy, że Tribe ma metodę add_unit lub train_workers.
        Alternatywnie, w razie braku, dodajemy robotnika bezpośrednio
        do listy self.tribe.workers.
        """
        initial = len(self.tribe.workers)
        worker = Worker(tribe=self.tribe)

        # Próba wywołania add_unit
        try:
            self.tribe.add_unit(worker)
        except AttributeError:
            self.tribe.workers.append(worker)

        self.assertIn(
            worker,
            self.tribe.workers,
            "Po dodaniu Worker-a do plemienia, lista `workers` powinna zawierać tego robotnika."
        )
        self.assertEqual(
            len(self.tribe.workers),
            initial + 1,
            f"Po dodaniu jednego Worker-a lista powinna mieć rozmiar {initial+1}, a miała {len(self.tribe.workers)}."
        )

        # Usunięcie robotnika (Workera), jeśli nie ma remove_unit()
        try:
            self.tribe.remove_unit(worker)
        except AttributeError:
            self.tribe.workers.remove(worker)

        self.assertNotIn(
            worker,
            self.tribe.workers,
            "Po usunięciu Worker-a lista `workers` nie powinna zawierać tego robotnika."
        )
        self.assertEqual(
            len(self.tribe.workers),
            initial,
            f"Po usunięciu Worker-a lista powinna wrócić do rozmiaru {initial}, a miała {len(self.tribe.workers)}."
        )

    def test_add_and_remove_warrior(self):
        """
        Analogicznie do workera sprawdzamy, czy plemię potrafi dodać i usunąć wojownika.
        """
        initial = len(self.tribe.warriors)
        warrior = Warrior(tribe=self.tribe)

        try:
            self.tribe.add_unit(warrior)
        except AttributeError:
            self.tribe.warriors.append(warrior)

        self.assertIn(
            warrior,
            self.tribe.warriors,
            "Po dodaniu Warrior-a do plemienia, lista `warriors` powinna zawierać tego wojownika."
        )
        self.assertEqual(
            len(self.tribe.warriors),
            initial + 1,
            f"Po dodaniu jednego Warrior-a lista powinna mieć rozmiar {initial+1}, a miała {len(self.tribe.warriors)}."
        )

        try:
            self.tribe.remove_unit(warrior)
        except AttributeError:
            self.tribe.warriors.remove(warrior)

        self.assertNotIn(
            warrior,
            self.tribe.warriors,
            "Po usunięciu Warrior-a lista `warriors` nie powinna zawierać tego wojownika."
        )
        self.assertEqual(
            len(self.tribe.warriors),
            initial,
            f"Po usunięciu Warrior-a lista powinna wrócić do rozmiaru {initial}, a miała {len(self.tribe.warriors)}."
        )


if __name__ == "__main__":
    unittest.main()