# =============================================================================
# food.py – Die Food-Klasse
# =============================================================================
# Verantwortlich für das Essen, das die Snake fressen kann.
# Das Food erscheint immer zufällig auf dem Raster, aber nie auf einem
# Körperteil der Snake – damit es sofort erreichbar ist.
# =============================================================================

import pygame
import random
import constants

class Food:
    # -------------------------------------------------------------------------
    # __init__: Konstruktor – wird aufgerufen, wenn ein Food-Objekt erstellt wird
    # -------------------------------------------------------------------------
    # snake_body wird übergeben, damit das Food nicht auf der Snake erscheint.
    # Wir setzen die Position zunächst auf [0, 0] als Platzhalter, und rufen
    # dann sofort randomize() auf, um eine echte Startposition zu berechnen.
    def __init__(self, snake_body):
        self.position = [0, 0]
        self.randomize(snake_body)

    # -------------------------------------------------------------------------
    # randomize: Sucht eine neue, freie Position auf dem Raster
    # -------------------------------------------------------------------------
    def randomize(self, snake_body):
        # Zuerst berechnen wir, wie viele Felder das Raster hat.
        # WIDTH // BLOCK_SIZE ergibt die Anzahl der Spalten (z.B. 1200 // 30 = 40).
        # HEIGHT // BLOCK_SIZE ergibt die Anzahl der Zeilen  (z.B.  900 // 30 = 30).
        cols = constants.WIDTH // constants.BLOCK_SIZE
        rows = constants.HEIGHT // constants.BLOCK_SIZE

        # Die while-True-Schleife läuft so lange, bis wir eine freie Position gefunden haben.
        # Im schlimmsten Fall (Snake füllt fast das ganze Feld) kann das viele Versuche brauchen.

        while True:
            # random.randint(0, cols - 1) wählt eine zufällige Spalte aus (0 bis 39).
            # Multipliziert mit BLOCK_SIZE ergibt das die Pixel-X-Koordinate des Felds.
            # Dasselbe passiert für die Y-Koordinate (Zeile).
            x = random.randint(0, (constants.WIDTH // constants.BLOCK_SIZE) -1) * constants.BLOCK_SIZE
            y = random.randint( 0, (constants.HEIGHT // constants.BLOCK_SIZE) -1) * constants.BLOCK_SIZE
            self.position = [x, y]

            # Prüfen ob diese Position bereits von der Snake belegt ist.
            # snake_body ist eine Liste von [x, y]-Paaren aller Segmente.
            # Falls die neue Position NICHT in der Liste ist, verlassen wir die Schleife.
            if self.position not in snake_body:
                break

    # -------------------------------------------------------------------------
    # draw: Zeichnet das Food auf den Bildschirm
    # -------------------------------------------------------------------------

    def draw(self, screen):
        x, y = self.position        # Position entpacken (x- und y-Koordinate)
        s = constants.BLOCK_SIZE    # Kurzname für die Blockgröße (spart Tipparbeit)

        # Zuerst den vollen roten Block als Hintergrund zeichnen.
        pygame.draw.rect(screen, constants.RED, (x,y,s,s))

        # Dann einen kleineren, helleren Block mittig darüber zeichnen.
        # Die 4 Pixel Einrückung von allen Seiten erzeugen einen Rahmeneffekt,
        # der dem Food etwas mehr Tiefe verleiht.
        # (x + 4, y + 4) = eingerückte Startposition
        # (s - 8, s - 8) = Breite und Höhe 8 Pixel kleiner als der äußere Block
        pygame.draw.rect(screen, (255, 80, 80), (x + 4, y + 4 , s -8, s - 8))
