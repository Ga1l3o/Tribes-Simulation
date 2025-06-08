# tribe-simulation

**Symulacja rozwoju plemion na 2D-planszy w Pythonie (ekspansja, surowce, bitwy)**

---

## Spis treści

1. [Opis projektu](#opis-projektu)  
2. [Skład zespołu](#skład-zespołu)  
3. [Jak uruchomić](#jak-uruchomić)  
4. [Struktura projektu](#struktura-projektu)  
5. [Diagramy UML](#diagramy-uml)  
   - [Diagram klas](#diagram-klas)  
   - [Diagram obiektów (przykład)](#diagram-obiektów-przykład)  
   - [Diagram sekwencji](#diagram-sekwencji)  
   - [Diagram stanu (maszyna stanów)](#diagram-stanu-maszyna-stanów)  
6. [Dokumentacja docstrings](#dokumentacja-docstrings)  
7. [Generacja dokumentacji HTML (Sphinx / Doxygen)](#generacja-dokumentacji-html-sphinx--doxygen)  

---

## Opis projektu

Celem projektu jest stworzenie symulacji, w której na dwuwymiarowej, kwadratowej planszy rozstawione są osady (plemiona). Każde plemię (obiekt `Tribe`) posiada własne parametry:

- **Populacja** (liczba robotników i wojowników)  
- **Liczba wojowników** (z siłą bojową, którą można ulepszać)  
- **Liczba robotników** (którzy generują surowce)  
- **Zajęte terytorium** (zbiory współrzędnych pól na planszy, reprezentowane w `Board.grid`)  
- **Zapas surowców**:  
  - **Pożywienie** (food) – utrzymanie i rekrutacja nowych jednostek  
  - **Materiały budowlane** (building_materials) – potrzebne do ekspansji i ulepszania wojowników

Symulacja przebiega w turach synchronicznych:

1. **Wybór akcji**:  
   - Każde plemię, biorąc pod uwagę swoje aktualne zasoby i stan populacji, losuje dokładnie jedną z czterech akcji (lub „nic”):  
     - **Ekspansja** – rozszerzenie terytorium o jedno nowe, losowe, sąsiadujące puste pole (koszt: procent materiałów budowlanych).  
     - **Szkolenie robotników** – rekrutacja 1 – X nowych robotników (X zależy od dostępnego jedzenia, zostaje pobrany losowy procent z przedziału 10 %–50 %).  
     - **Szkolenie wojowników** – rekrutacja analogicznej liczby wojowników (koszt: jedzenie).  
     - **Ulepszanie wojowników** – zwiększenie siły wszystkich istniejących wojowników o stały bonus (koszt: procent materiałów budowlanych).  
     - **Brak akcji** – plemię „odpuszcza” turę (np. jeśli nie ma wystarczających surowców).

2. **Przydział surowców**:  
   - Za każdego robotnika plemię otrzymuje **4** jednostki materiałów budowlanych.  
   - Za każde zajęte pole w terytorium plemię otrzymuje **30** jednostek pożywienia.  

3. **Konsumpcja jedzenia**:  
   - Każda jednostka (robotnik lub wojownik) w tej turze potrzebuje 1 jednostki jedzenia.  
   - Jeśli zapas jedzenia jest niewystarczający, nadmiarowe jednostki są usuwane w kolejności: najpierw robotnicy, potem wojownicy.

4. **Maksymalna populacja**:  
   - Całkowita liczba jednostek (robotnicy + wojownicy) nie może przekroczyć `5 × (<liczba zajętych pól>)`.  
   - Jeśli jest zbyt wielu „ludków”, traci się nadmiar (pomniejszamy plemię do dopuszczalnej liczby).

5. **Bitwy**:  
   - Gdy dwa plemiona mają przynajmniej jeden wspólny bok na granicy (sąsiadują), a obaj mają przynajmniej jednego wojownika, dochodzi do **bitwy**.  
   - Każdy plemień oblicza swoją łączną siłę:  
     ```
     total_strength = sum(strength dla każdego wojownika z listy self.warriors)
     ```
   - Straty są proporcjonalne do siły przeciwnika – przykładowo:  
     - Jeśli siła Plemienia A = 50, Plemienia B = 30, to A straci `(30/50) * liczba_wojowników_A`, B straci `(50/30) * liczba_wojowników_B` (zaokrąglone w dół do najbliższej liczby całkowitej).  
   - Zwycięzca (ten, co ma większą siłę) **zbiera wszystkie surowce pokonanego plemienia** (jego jedzenie + materiały).  
   - Przegrany traci cały posterunek (usuwa się go z planszy, czyli z `Board.tribes` i `Board.grid`).

6. **Zakończenie symulacji**:  
   - Symulacja kończy się, gdy na planszy pozostanie tylko jedno plemię (zwycięskie) lub osiągniemy zdefiniowany w `main.py` (lub `config.py`) limit tur.

Kod jest podzielony na następujące pliki:

- `board.py`     – klasa `Board`, która trzyma siatkę, realizuje funkcje `place_tribe`, `battle`, `have_shared_border` itp.  
- `tribe.py`     – klasa `Tribe`, model plemienia, zarządza surowcami, listami robotników i wojowników, wykonuje akcje w turze (`perform_action`) oraz `consume_food`.  
- `units.py`     – (opcjonalnie) abstrakcyjna klasa `Unit` oraz podklasy `Worker` i `Warrior` ze statystykami.  
- `simulation.py` – klasa `Simulation`, orchestruje pętlę symulacji, wywołuje akcje plemion, sprawdza kolizje (bitwy) i zapisuje wyniki do CSV.  
- `main.py`      – punkt wejścia, pobiera parametry od użytkownika, uruchamia `Simulation` i (opcjonalnie) rysuje wykresy za pomocą `graf.py`.  
- `graf.py`      – klasa `WykresyPlemion`, wczytuje `tribes_data.csv` i generuje wykresy w Matplotlib.  
- `test_tribe.py` – testy jednostkowe dla klasy `Tribe` (np. sprawdzanie rekrutacji, kosztów, usuwania jednostek).

---

## Skład zespołu

- **Michał J.** – Lider projektu  
- **Mikołaj P.**

---

## Jak uruchomić

1. **Sklonuj repozytorium** (z terminala / PowerShell / WSL / Git Bash):
   ```bash
   git clone https://github.com/Ga1l3o/tribe-simulation.git
   cd tribe-simulation
