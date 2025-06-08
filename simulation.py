import time
import csv
import random
from config import MIN_BOARD_SIZE, MAX_BOARD_SIZE, MIN_TRIBES, MAX_TRIBES_RATIO
from board import Board
from tribe import Tribe


class Simulation:
    """Główna klasa symulacji"""

    def __init__(self, board_size, tribes_count, time_per_turn):
        self.board_size = board_size
        self.tribes_count = tribes_count
        self.time_per_turn = time_per_turn
        self.board = None
        self.turn = 0
        self.simulation_data = []
        self.battle_log = []

    def initialize(self):
        """Inicjalizuj symulację"""
        # Walidacja parametrów
        if not MIN_BOARD_SIZE <= self.board_size <= MAX_BOARD_SIZE:
            raise ValueError(f"Board size must be between {MIN_BOARD_SIZE} and {MAX_BOARD_SIZE}")

        max_tribes = (self.board_size ** 2) // MAX_TRIBES_RATIO
        if not MIN_TRIBES <= self.tribes_count <= max_tribes:
            raise ValueError(f"Tribes count must be between {MIN_TRIBES} and {max_tribes}")

        # Stwórz planszę
        self.board = Board(self.board_size)

        # Umieść plemiona
        for _ in range(self.tribes_count):
            pos = self.board.get_random_empty_position()
            if pos:
                tribe = Tribe(self.board, pos[0], pos[1])
                self.board.place_tribe(tribe)

    def run(self):
        """Uruchom symulację"""
        self.initialize()

        while sum(1 for tribe in self.board.tribes if tribe.is_alive) > 1:
            self.turn += 1
            print(f"\n===== Tura {self.turn} =====")
            turn_data = []

            # Wykonaj turę dla każdego plemienia
            for tribe in list(self.board.tribes):
                if not tribe.is_alive:
                    continue

                # Faza zbierania surowców
                tribe.collect_resources()

                # Faza akcji
                tribe.perform_action()

                # Faza konsumpcji
                tribe.consume_food()

                # Zapisz dane
                turn_data.append({
                    'tribe_id': tribe.id,
                    'workers': len(tribe.workers),
                    'warriors': len(tribe.warriors),
                    'territory': len(tribe.territory),
                    'food': tribe.food,
                    'building_materials': tribe.building_materials,
                    'alive': tribe.is_alive
                })

            # Zapisz dane tury
            self.simulation_data.append({
                'turn': self.turn,
                'tribes': turn_data
            })

            # Sprawdź kolizje między plemionami
            self.check_collisions()

            # Wyświetl planszę i statystyki
            self.board.display_board()
            print("--- Statystyki Plemion ---")
            for tribe in self.board.tribes:
                print(tribe)
            print("------------------------\n")

            # Oczekiwanie między turami
            time.sleep(self.time_per_turn)

        # Zapisz dane po zakończeniu
        self.save_to_csv()

    def check_collisions(self):
        """Sprawdź kolizje między plemionami (walki)"""
        alive_tribes = [t for t in self.board.tribes if t.is_alive]
        if len(alive_tribes) < 2:
            return

        # Sprawdź każdą parę plemion, które mają wspólną granicę
        for i in range(len(alive_tribes)):
            tribe1 = alive_tribes[i]
            for j in range(i + 1, len(alive_tribes)):
                tribe2 = alive_tribes[j]
                if self.board.have_shared_border(tribe1, tribe2):
                    print(f"Plemiona {tribe1.id} i {tribe2.id} mają wspólną granicę. Rozpoczyna się walka!")
                    # Losowo wybierz atakującego i broniącego
                    if random.random() < 0.5:
                        attacker, defender = tribe1, tribe2
                    else:
                        attacker, defender = tribe2, tribe1

                    # Przeprowadź walkę
                    result = self.board.battle(attacker, defender)
                    if result[0] is not None:
                        winner, loser, winner_losses, loser_losses = result
                        print(f"Walka zakończona! Zwycięzca: Plemię {winner.id}, Przegrany: Plemię {loser.id}")
                        print(f"Straty zwycięzcy: {winner_losses}, Straty przegranego: {loser_losses}")
                        self.battle_log.append({
                            'turn': self.turn,
                            'attacker': attacker.id,
                            'defender': defender.id,
                            'winner': winner.id,
                            'attacker_losses': winner_losses if winner == attacker else loser_losses,
                            'defender_losses': loser_losses if winner == attacker else winner_losses
                        })
                    else:
                        print("Remis - brak wojowników po obu stronach.")


    def save_to_csv(self):
        """Zapisz dane symulacji do pliku CSV"""
        # Zapis stanów plemion
        with open('tribes_data.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['turn', 'tribe_id', 'workers', 'warriors', 'territory', 'food', 'building_materials', 'alive'])
            for turn_data in self.simulation_data:
                for tribe in turn_data['tribes']:
                    writer.writerow([
                        turn_data['turn'],
                        tribe['tribe_id'],
                        tribe['workers'],
                        tribe['warriors'],
                        tribe['territory'],
                        tribe['food'],
                        tribe['building_materials'],
                        1 if tribe['alive'] else 0
                    ])

        # Zapis logów walk
        with open('battles.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['turn', 'attacker', 'defender', 'winner', 'attacker_losses', 'defender_losses'])
            for battle in self.battle_log:
                writer.writerow([
                    battle['turn'],
                    battle['attacker'],
                    battle['defender'],
                    battle['winner'],
                    battle['attacker_losses'],
                    battle['defender_losses']
                ])