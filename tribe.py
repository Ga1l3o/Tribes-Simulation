import random
from config import *
from units import Worker, Warrior


class Tribe:
    """Klasa reprezentująca plemię"""
    tribe_count = 0  # licznik plemion

    def __init__(self, board, x, y):
        self.id = Tribe.tribe_count
        Tribe.tribe_count += 1
        self.board = board  # agregacja - plansza
        self.territory = set()  # kompozycja - zajęte pola
        self.workers = []  # kompozycja - robotnicy
        self.warriors = []  # kompozycja - wojownicy
        self.building_materials = 0
        self.food = 0
        self.is_alive = True

        # Początkowe umieszczenie na planszy
        self.add_territory(x, y)

        # Początkowa populacja
        for _ in range(2):
            self.add_worker()
        self.add_warrior()

    def add_territory(self, x, y):
        """Dodaj nowe terytorium dla plemienia"""
        self.territory.add((x, y))
        self.board.grid[x][y] = self.id

    def add_worker(self):
        """Dodaj robotnika jeśli populacja pozwala"""
        if self.can_add_population():
            self.workers.append(Worker(self))

    def add_warrior(self):
        """Dodaj wojownika jeśli populacja pozwala"""
        if self.can_add_population():
            self.warriors.append(Warrior(self))

    def can_add_population(self):
        """Sprawdź, czy można dodać nową jednostkę"""
        current_population = len(self.workers) + len(self.warriors)
        return current_population < len(self.territory) * POPULATION_PER_TERRITORY

    def collect_resources(self):
        """Zbierz surowce w turze"""
        # Budulec z robotników
        self.building_materials += len(self.workers) * BUILDING_MATERIAL_PER_WORKER
        # Jedzenie z terytorium
        self.food += len(self.territory) * FOOD_PER_TERRITORY

    def consume_food(self):
        """Konsumuj jedzenie i redukuj populację jeśli ilość jedzenia jest niewystarczająca"""
        total_consumption = sum(unit.food_consumption() for unit in self.workers + self.warriors)

        if self.food < total_consumption:
            self.reduce_population(total_consumption - self.food)
            self.food = 0
        else:
            self.food -= total_consumption

    def reduce_population(self, deficit):
        """Redukuj populację z powodu braku jedzenia (najpierw wojownicy)"""
        # Polimorfizm - różne jednostki mają różne koszty konsumpcji
        while deficit > 0 and (self.warriors or self.workers):
            if self.warriors:
                warrior = self.warriors.pop()
                deficit -= warrior.food_consumption()
            elif self.workers:
                worker = self.workers.pop()
                deficit -= worker.food_consumption()

    def train_workers(self):
        """Szkol nowych robotników, zużywając procent dostępnego jedzenia"""
        if self.food < WORKER_RECRUITMENT_COST:
            return 0

        # Procent jedzenia, który plemię chce wydać na rekrutację
        spend_percent = random.uniform(RECRUITMENT_MIN_PERCENT, RECRUITMENT_MAX_PERCENT)
        food_to_spend = int(self.food * spend_percent)

        # Maksymalna liczba robotników, jaką można zrekrutować za tę ilość jedzenia
        recruits_from_food = food_to_spend // WORKER_RECRUITMENT_COST

        # Maksymalna liczba robotników, jaką można zrekrutować, uwzględniając limit populacji
        max_possible_recruits = len(self.territory) * POPULATION_PER_TERRITORY - self.total_population()

        recruits = min(recruits_from_food, max_possible_recruits)

        if recruits > 0:
            cost = recruits * WORKER_RECRUITMENT_COST
            self.food -= cost
            for _ in range(recruits):
                self.add_worker()
            return recruits
        return 0

    def train_warriors(self):
        """Szkol nowych wojowników, zużywając procent dostępnego jedzenia"""
        if self.food < WARRIOR_RECRUITMENT_COST:
            return 0

        # Procent jedzenia, który plemię chce wydać na rekrutację
        spend_percent = random.uniform(RECRUITMENT_MIN_PERCENT, RECRUITMENT_MAX_PERCENT)
        food_to_spend = int(self.food * spend_percent)

        # Maksymalna liczba wojowników, jaką można zrekrutować za tę ilość jedzenia
        recruits_from_food = food_to_spend // WARRIOR_RECRUITMENT_COST

        # Maksymalna liczba wojowników, jaką można zrekrutować, uwzględniając limit populacji
        max_possible_recruits = len(self.territory) * POPULATION_PER_TERRITORY - self.total_population()

        recruits = min(recruits_from_food, max_possible_recruits)

        if recruits > 0:
            cost = recruits * WARRIOR_RECRUITMENT_COST
            self.food -= cost
            for _ in range(recruits):
                self.add_warrior()
            return recruits
        return 0

    def expand(self):
        """Rozszerz terytorium, zużywając procent dostępnego budulca"""
        if self.building_materials < EXPANSION_COST:
            return False

        # Szukaj sąsiednich wolnych pól
        neighbors = set()
        for x, y in self.territory:
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.board.size and 0 <= ny < self.board.size: # Warunek zabezpieczający przed wyjściem poza planszę
                    if self.board.grid[nx][ny] is None:
                        neighbors.add((nx, ny))

        if not neighbors:
            return False

        # Oblicz, ile ekspansji można przeprowadzić
        # Chcemy wydać procent materiałów
        spend_percent = random.uniform(RECRUITMENT_MIN_PERCENT, RECRUITMENT_MAX_PERCENT)  # Używamy tych samych % co dla rekrutacji dla spójności
        materials_to_spend = int(self.building_materials * spend_percent)

        possible_expansions = min(materials_to_spend // EXPANSION_COST, len(neighbors))

        if possible_expansions == 0:
            return False

        expanded_count = 0
        # Wybierz losowe pola do rozszerzenia spośród dostępnych
        chosen_neighbors = random.sample(list(neighbors), min(possible_expansions, len(neighbors)))

        for nx, ny in chosen_neighbors:
            if self.building_materials >= EXPANSION_COST:
                self.building_materials -= EXPANSION_COST
                self.add_territory(nx, ny)
                expanded_count += 1
            else:
                break  # Brak materiałów na dalszą ekspansję

        return expanded_count > 0

    def upgrade_warriors(self):
        """Ulepsz wojowników, zużywając procent dostępnego budulca"""
        if self.building_materials < UPGRADE_COST:
            return 0

        # Procent budulca, który plemię chce wydać na ulepszenia
        spend_percent = random.uniform(MATERIALS_MIN_PERCENT, MATERIALS_MAX_PERCENT)
        materials_to_spend = int(self.building_materials * spend_percent)

        # Maksymalna liczba ulepszeń, jaką można przeprowadzić za tę ilość materiałów
        possible_upgrades = materials_to_spend // UPGRADE_COST

        # Limit ulepszeń do tych, które mogą być jeszcze ulepszone
        upgradable_warriors = [w for w in self.warriors if w.level < MAX_WARRIOR_LEVEL]
        possible_upgrades = min(possible_upgrades, len(upgradable_warriors))

        if possible_upgrades == 0:
            return 0

        upgraded = 0
        # Ulepsz losowo wybranych wojowników, którzy mogą być ulepszeni
        random.shuffle(upgradable_warriors)  # Losowa kolejność ulepszania
        for warrior in upgradable_warriors:
            if upgraded >= possible_upgrades:
                break
            if warrior.upgrade():
                self.building_materials -= UPGRADE_COST
                upgraded += 1

        return upgraded

    def total_strength(self):
        """Oblicz całkowitą siłę wojowników danego plemienia"""
        return sum(warrior.strength for warrior in self.warriors)

    def total_population(self):
        """Oblicz całkowitą populację danego plemienia"""
        return len(self.workers) + len(self.warriors)

    def perform_action(self):
        """Oblicz wagi dla poszczególnych akcji oraz wykonaj akcję w turze z wagą zależną od stanu plemienia."""
        actions_with_weights = {
            'expand': 0,
            'train_workers': 0,
            'train_warriors': 0,
            'upgrade_warriors': 0,
            'nothing': 0
        }

        # Wagi dla jedzenia
        if self.food > FOOD_PER_TERRITORY * len(self.territory) * 2:  # Jeśli mamy dużo jedzenia (2x więcej niż produkujemy)
            actions_with_weights['train_workers'] += 0.5
            actions_with_weights['train_warriors'] += 0.5
        elif self.food < FOOD_PER_TERRITORY * len(self.territory) * 0.5:  # Jeśli mamy mało jedzenia
            actions_with_weights['train_workers'] -= 0.5  # Mniej chętnie rekrutuj robotników
            actions_with_weights['train_warriors'] -= 0.5  # Mniej chętnie rekrutuj wojowników
            actions_with_weights['nothing'] += 0.5  # Skup się na gromadzeniu

        # Wagi dla budulca
        if self.building_materials > EXPANSION_COST * 2:  # Jeśli mamy dużo budulca
            actions_with_weights['expand'] += 0.5
            actions_with_weights['upgrade_warriors'] += 0.5
        elif self.building_materials < EXPANSION_COST * 0.5:  # Jeśli mamy mało budulca
            actions_with_weights['expand'] -= 0.5
            actions_with_weights['upgrade_warriors'] -= 0.5
            actions_with_weights['nothing'] += 0.5

        # Wagi dla populacji/terytorium
        if self.total_population() < len(self.territory) * POPULATION_PER_TERRITORY * 0.8:  # Jeśli jest miejsce na populację
            actions_with_weights['train_workers'] += 0.5
            actions_with_weights['train_warriors'] += 0.5
        else:  # Jeśli populacja jest blisko limitu
            actions_with_weights['expand'] += 0.5  # Bardziej chętnie rozszerzaj terytorium

        # Wagi dla siły bojowej (mniej wojowników => chęć rekrutacji)
        if len(self.warriors) < len(self.territory) * (POPULATION_PER_TERRITORY / 4):  # Jeśli wojowników jest relatywnie mało
            actions_with_weights['train_warriors'] += 0.5
            actions_with_weights['upgrade_warriors'] += 0.3

        # Upewnij się, że wagi nie są ujemne
        for action in actions_with_weights:
            actions_with_weights[action] = max(0, actions_with_weights[action] + 1)  # Dodajemy 1, żeby każda akcja miała jakąś bazową wagę

        # Wybierz akcję na podstawie wag, tworzymy
        actions = list(actions_with_weights.keys())
        weights = list(actions_with_weights.values())

        # Jeśli wszystkie wagi są 0 (np. po tym jak zmieniliśmy na max(0, ...)), domyślnie wybierz 'nothing'
        if sum(weights) == 0:
            action = 'nothing'
        else:
            action = random.choices(actions, weights=weights, k=1)[0] # Wybieramy k (1) elementów z listy actions z szansą określoną w weights

        # Wykonaj wybraną akcję
        if action == 'expand':
            return self.expand()
        elif action == 'train_workers':
            return self.train_workers()
        elif action == 'train_warriors':
            return self.train_warriors()
        elif action == 'upgrade_warriors':
            return self.upgrade_warriors()
        return True  # akcja 'nothing' zawsze udana

    def __str__(self):
        """Wyświetl podstawowe statystyki plemienia"""
        status = "Żywe" if self.is_alive else "Wyeliminowane"
        return (f"Plemię {self.id} ({status}): Robotnicy={len(self.workers)}, "
                f"Wojownicy={len(self.warriors)} (Siła:{int(self.total_strength())}), "
                f"Terytorium={len(self.territory)}, Pożywienie={int(self.food)}, "
                f"Materiały={int(self.building_materials)}")