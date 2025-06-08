import random
from config import STOLE_RESOURCES_MIN, STOLE_RESOURCES_MAX


class Board:
    """Klasa reprezentująca planszę"""

    # Lista kodów kolorów ANSI, które będziemy cyklicznie przypisywać plemionom
    COLOR_CODES = [
        '\033[31m',  # czerwony
        '\033[32m',  # zielony
        '\033[33m',  # żółty
        '\033[34m',  # niebieski
        '\033[35m',  # magenta
        '\033[36m',  # cyjan
        '\033[91m',  # jasny czerwony
        '\033[92m',  # jasny zielony
        '\033[93m',  # jasny żółty
        '\033[94m',  # jasny niebieski
        '\033[95m',  # jasny magenta
        '\033[96m',  # jasny cyjan
    ]
    RESET_CODE = '\033[0m'  # reset koloru (przywrócenie domyślnego)


    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.tribes = []  # agregacja - plemiona

    def place_tribe(self, tribe):
        """Umieść plemię na planszy"""
        self.tribes.append(tribe)

    def get_random_empty_position(self):
        """Znajdź losowe puste pole na planszy"""
        empty_positions = []
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] is None:
                    empty_positions.append((x, y))
        return random.choice(empty_positions) if empty_positions else None

    def remove_tribe(self, tribe):
        """Usuń plemię z planszy"""
        if tribe in self.tribes:
            self.tribes.remove(tribe)
            tribe.is_alive = False
            for x, y in tribe.territory:
                self.grid[x][y] = None

    def have_shared_border(self, tribe1, tribe2):
        """Sprawdź czy dwa plemiona mają wspólną granicę"""
        for x1, y1 in tribe1.territory:
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x1 + dx, y1 + dy
                if (nx, ny) in tribe2.territory:
                    return True
        return False

    def battle(self, attacker, defender):
        """Rozstrzygnij walkę między plemionami"""
        strength_attacker = attacker.total_strength()
        strength_defender = defender.total_strength()

        # Jeśli obie siły są zerowe, to remis - nie ma walki
        if strength_attacker == 0 and strength_defender == 0:
            return None, None, 0, 0

        # Określenie zwycięzcy na podstawie siły
        if strength_attacker > strength_defender:
            winner, loser = attacker, defender
            winner_strength, loser_strength = strength_attacker, strength_defender
        else:
            winner, loser = defender, attacker
            winner_strength, loser_strength = strength_defender, strength_attacker

        # Oblicz straty zwycięzcy zgodnie z wzorem
        winner_losses = 0
        if winner_strength > 0:
            # Wzór: (W_wyg / S_wyg) * (S_przeg / S_wyg) * W_wyg
            winner_losses = int((len(winner.warriors) / winner_strength) * (loser_strength / winner_strength) * len(winner.warriors))


        # Zastosuj straty zwycięzcy - usuń wojowników
        # Uwaga: min(winner_losses, len(winner.warriors)) aby nie przekroczyć
        for _ in range(min(winner_losses, len(winner.warriors))):
            if winner.warriors:
                winner.warriors.pop()

        # Przegrany traci WSZYSTKICH wojowników
        loser_losses = len(loser.warriors)
        loser.warriors = []

        # Przejęcie zasobów
        winner.building_materials += loser.building_materials * random.uniform(STOLE_RESOURCES_MIN, STOLE_RESOURCES_MAX)
        winner.food += loser.food * random.uniform(STOLE_RESOURCES_MIN, STOLE_RESOURCES_MAX)

        # Usuń przegranego z planszy
        self.remove_tribe(loser)

        return winner, loser, winner_losses, loser_losses

    def display_board(self):
        """Wyświetl planszę w konsoli."""
        # Maksymalna szerokość
        max_id = 0
        for row in self.grid:
            for cell in row:
                if cell is not None and cell > max_id:
                    max_id = cell
        # min 2, max 3 (zależnie od długości maksymalnej ID plemienia)
        cell_width = max(2, len(str(max_id)))

        print("\n--- Plansza ---")
        for row in self.grid:
            for cell in row:
                if cell is not None:
                    color_code = self.COLOR_CODES[cell % len(self.COLOR_CODES)]
                    # rjust dopełnia spacji z lewej, więc ' 10' zamiast '10'
                    cell_str = str(cell).rjust(cell_width)
                    print(f"{color_code}{cell_str}{self.RESET_CODE}", end=' ')
                else:
                    # analogicznie do pustego pola: kropka w położeniu wycentrowanym
                    print(f"{'.'.rjust(cell_width)}", end=' ')
            print()
        print("---------------\n")