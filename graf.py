import pandas as pd  # import biblioteki pandas do manipulacji danymi
import matplotlib.pyplot as plt  # import biblioteki matplotlib do tworzenia wykresów

class TribeCharts:
    def __init__(self, filename):
        """
        Konstruktor klasy WykresyPlemion.
        filename: ścieżka do pliku CSV zawierającego dane plemion.
        """
        self.filename = filename  # zapisanie nazwy pliku jako atrybut obiektu
        self.df = pd.read_csv(self.filename)  # wczytanie danych z pliku CSV do DataFrame
        # lista unikalnych identyfikatorów plemion, posortowana rosnąco
        self.tribes_to_compare = sorted(self.df['tribe_id'].unique())
        # kolumny, które chcemy przedstawić na wykresach
        self.columns_of_interest = ['food', 'building_materials', 'workers', 'warriors']

    def draw_charts(self):
        """
        Metoda rysująca wykresy dla każdej z wybranych kolumn,
        porównująca wartości dla poszczególnych plemion w kolejnych turach.
        """
        # iteracja po każdej z kolumn zainteresowania
        for col in self.columns_of_interest:
            plt.figure(figsize=(12, 7))  # utworzenie nowej figury o rozmiarze 12x7 cali (w Matplotlib musimy w calach)

            # dla każdego plemienia narysuj osobną linię na wykresie
            for tribe_id in self.tribes_to_compare:
                # wyfiltrowanie danych tylko dla bieżącego plemienia
                tribe_data = self.df[self.df['tribe_id'] == tribe_id]
                # narysowanie linii: oś X = 'turn', oś Y = wartość kolumny col
                plt.plot(tribe_data['turn'], tribe_data[col], label=f'Tribe {tribe_id}')

            # ustawienie tytułu wykresu, w zależności od analizowanej kolumny
            plt.title(f'Porównanie plemion: {col}')
            plt.xlabel('Tura')  # etykieta osi X
            # etykieta osi Y: zamiana podkreśleń na spacje i kapitalizacja
            plt.ylabel(col.replace('_', ' ').capitalize())
            # legenda wyświetlająca etykiety dla poszczególnych plemion
            plt.legend(ncol=3, fontsize='small')
            plt.grid(True)  # włączenie siatki na wykresie
            plt.tight_layout()  # dopasowanie marginesów, aby nic nie było obcięte
            plt.show()  # wyświetlenie wykresu