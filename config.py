# Stałe konfiguracyjne symulacji

"""Plik konfiguracyjny zawierający stałe używane w całym projekcie."""

# Ograniczenia planszy
MIN_BOARD_SIZE = 10
MAX_BOARD_SIZE = 100

# Ograniczenia liczby plemion
MIN_TRIBES = 2
MAX_TRIBES_RATIO = 10  # maks_plemion = (rozmiar_planszy^2) // MAX_TRIBES_RATIO

# Parametry surowcowe
FOOD_PER_TERRITORY = 25
BUILDING_MATERIAL_PER_WORKER = 4
STOLE_RESOURCES_MIN = 0.2
STOLE_RESOURCES_MAX = 0.6

# Konsumpcja
WORKER_FOOD_CONSUMPTION = 3
WARRIOR_FOOD_CONSUMPTION = 5

# Koszty rekrutacji
WORKER_RECRUITMENT_COST = 5
WARRIOR_RECRUITMENT_COST = 7
RECRUITMENT_MIN_PERCENT = 0.1
RECRUITMENT_MAX_PERCENT = 0.5

# Koszty akcji
EXPANSION_COST = 200
UPGRADE_COST = 15
MATERIALS_MIN_PERCENT = 0.1
MATERIALS_MAX_PERCENT = 0.75

# Parametry wojowników
BASE_WARRIOR_STRENGTH = 4
UPGRADE_STRENGTH_BONUS = 2
MAX_WARRIOR_LEVEL = 5

# Populacja
POPULATION_PER_TERRITORY = 5