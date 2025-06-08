from simulation import Simulation
from config import *
from graf import TribeCharts

def get_validated_input(prompt, min_val, max_val, input_type=int):
    """
    Pobiera i waliduje dane wejściowe od użytkownika w pętli.
    prompt: Treść do wyświetlenia użytkownikowi.
    min_val: Minimalna dozwolona wartość.
    max_val: Maksymalna dozwolona wartość.
    input_type: Typ, na który ma być skonwertowana wartość (int lub float).
    """
    while True:
        try:
            value = input_type(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Błąd: Wartość musi być w zakresie od {min_val} do {max_val}.")
        except ValueError:
            print("Błąd: Wprowadzono niepoprawny format. Proszę wprowadzić liczbę.")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")


def main():
    """Główna funkcja uruchamiająca symulację"""
    print("=== Symulacja Walki Plemion ===")

    # Pobierz i waliduj rozmiar planszy
    board_size = get_validated_input(
        f"Rozmiar planszy ({MIN_BOARD_SIZE}-{MAX_BOARD_SIZE}): ",
        MIN_BOARD_SIZE,
        MAX_BOARD_SIZE,
        int
    )

    # Oblicz maksymalną liczbę plemion na podstawie walidowanego rozmiaru planszy
    max_tribes_calculated = (board_size ** 2) // MAX_TRIBES_RATIO

    # Pobierz i waliduj liczbę plemion
    tribes_count = get_validated_input(
        f"Liczba plemion ({MIN_TRIBES}-{max_tribes_calculated}): ",
        MIN_TRIBES,
        max_tribes_calculated,
        int
    )

    # Pobierz i waliduj czas trwania tury
    time_per_turn = get_validated_input(
        "Czas trwania tury (sekundy) (0.0-60.0): ",
        0.0,
        60.0,
        float
    )

    # Uruchom symulację
    sim = Simulation(board_size, tribes_count, time_per_turn)
    sim.run()
    print("Symulacja zakończona! Dane zapisano do tribes_data.csv i battles.csv")

    print("Czy chcesz zobaczyć wykresy plemion? (T/N)")
    userInput = input().strip().lower()
    if userInput == "t":
        print("\n")
        charts = TribeCharts("tribes_data.csv")
        charts.draw_charts()

if __name__ == "__main__":
    main()