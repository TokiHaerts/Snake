# =============================================================================
# constants.py – Zentrale Konfigurationsdatei
# =============================================================================
# Alle Einstellungen, Farben und Richtungsvektoren sind hier gesammelt.
# So muss man Werte wie die Fenstergröße oder FPS nur an einer Stelle ändern,
# und die Änderung wirkt sich automatisch auf das gesamte Spiel aus.
# =============================================================================

# -----------------------------------------------------------------------------
# Spielfeldgröße
# -----------------------------------------------------------------------------
# Das Spielfeld besteht aus einem unsichtbaren Raster gleichgroßer Blöcke.
# WIDTH und HEIGHT sind die Pixelmaße des Fensters.
# BLOCK_SIZE legt fest, wie groß ein einzelnes Rasterfeld ist.
# → Das Feld hat WIDTH // BLOCK_SIZE = 40 Spalten und
# → Das Feld hat HEIGHT // BLOCK_SIZE = 30 Zeilen.

WIDTH = 1200            # Fensterbreite in Pixeln  (40 Blöcke × 30 Pixel)
HEIGHT = 900            # Fensterhöhe  in Pixeln   (30 Blöcke × 30 Pixel)
BLOCK_SIZE = 30         # Seitenlänge eines Rasterblocks in Pixeln

# FPS = Frames Per Second (Bilder pro Sekunde).
# Bei FPS = 8 bewegt sich die Snake 8 Mal pro Sekunde einen Block weiter.
# Höhere Werte → schnelleres Spiel; niedrigere Werte → langsameres Spiel.
FPS = 8

# -----------------------------------------------------------------------------
# Farben
# -----------------------------------------------------------------------------
# Pygame verwendet das RGB-Format: jede Farbe ist ein Tupel aus drei Werten
# für Rot, Grün und Blau, jeweils von 0 (kein Anteil) bis 255 (voller Anteil).
# Beispiel: (255, 0, 0) = reines Rot, (0, 0, 0) = Schwarz, (255,255,255) = Weiß

BLACK       = (0,   0,  0   )   # Hintergrundfarbe des Spielfelds
WHITE       = (255, 255, 255)   # Textfarbe, Button-Rahmen
GRAY        = (128, 128, 128)   # Erklärungstexte auf dem Startbildschirm
DARK_GRAY   = (40,  40,  40 )   # Rasterlinien (dezent, damit sie nicht ablenken)
RED         = (255, 0,   0  )   # Food und "Game Over"-Schrift
GREEN       = (0,   255, 0  )   # Snake-Körper (gerade Segmente)
DARK_GREEN  = (0,   180, 0  )   # Snake-Körper (ungerade Segmente, Kontrast)
YELLOW      = (255, 255, 0  )   # Snake-Kopf und Highscore-Text

# -----------------------------------------------------------------------------
# Richtungsvektoren
# -----------------------------------------------------------------------------
# Jede Richtung ist ein Tupel (dx, dy), das angibt, um wie viele Pixel
# sich die Snake pro Schritt in X- und Y-Richtung bewegt.
#
# Wichtig: In Pygame zeigt die Y-Achse nach UNTEN.
# Das heißt: Y kleiner werden → Bewegung nach oben (UP hat dy = -BLOCK_SIZE).
#            Y größer werden  → Bewegung nach unten (DOWN hat dy = +BLOCK_SIZE).
#
# Diese Vektoren werden in snake.py direkt auf die Kopfposition addiert,
# und in __main__.py als Tastaturbelegung verwendet.

UP      = (0,           -BLOCK_SIZE )   # Y nimmt ab → nach oben
DOWN    = (0,           BLOCK_SIZE  )   # Y nimmt zu → nach unten
LEFT    = (-BLOCK_SIZE, 0           )   # X nimmt ab → nach links
RIGHT   = (BLOCK_SIZE,  0           )   # X nimmt zu → nach rechts
