# =============================================================================
# snake.py – Die Snake-Klasse
# =============================================================================
# Steuert alles, was die Schlange betrifft:
#   - Wie sie sich bewegt
#   - Wie sie ihre Richtung ändert (ohne sich selbst zu überfahren)
#   - Wie sie wächst, wenn sie Essen frisst
#   - Wie sie auf dem Bildschirm gezeichnet wird
#   - Wie Kollisionen mit der Wand oder sich selbst erkannt werden
# =============================================================================

import pygame
import constants

class Snake:
    # -------------------------------------------------------------------------
    # __init__: Startzustand der Snake festlegen
    # -------------------------------------------------------------------------
    def __init__(self):
        # Die Startposition soll in der Mitte des Spielfelds liegen.
        # WIDTH // BLOCK_SIZE // 2 gibt uns den mittleren Spaltenindex.
        # Multipliziert mit BLOCK_SIZE ergibt das die Pixelkoordinate des Felds.
        # So starten wir immer exakt auf einem Rasterpunkt, egal wie groß das Fenster ist.
        start_x = (constants.WIDTH  // constants.BLOCK_SIZE // 2) * constants.BLOCK_SIZE
        start_y = (constants.HEIGHT // constants.BLOCK_SIZE // 2) * constants.BLOCK_SIZE

        # Die Snake besteht aus einer Liste von Segmenten.
        # Jedes Segment ist eine [x, y]-Liste mit der Pixelposition des Blocks.
        # Index 0 ist immer der Kopf, der Rest ist der Körper.
        # Die Snake startet mit 3 Segmenten, die horizontal nebeneinander liegen.
        self.body = [
            [start_x,                            start_y],   # Kopf (vorne)
            [start_x -     constants.BLOCK_SIZE, start_y],   # Segment 2
            [start_x - 2 * constants.BLOCK_SIZE, start_y],   # Segment 3 (hinten)
        ]

        # Startrichtung ist nach rechts – passend, weil die Segmente links vom Kopf liegen.
        self.direction = constants.RIGHT

        # grow_status ist ein Merker (Flag), ob die Snake beim nächsten Schritt wachsen soll.
        # Er wird auf True gesetzt, wenn die Snake Essen frisst (in __main__.py),
        # und in move() wieder auf False zurückgesetzt, nachdem das Wachstum verarbeitet wurde.
        self.grow_status = False

    # -------------------------------------------------------------------------
    # change_direction: Richtung wechseln – aber keine direkte Umkehrung erlauben
    # -------------------------------------------------------------------------
    def change_direction(self, new_direction):
        # Ein Dictionary, das jeder Richtung ihre entgegengesetzte Richtung zuordnet.
        # Damit prüfen wir, ob die gewünschte Richtung die aktuelle Richtung umkehren würde.
        # Beispiel: Wenn die Snake nach rechts fährt, darf sie nicht sofort nach links.
        # Das würde dazu führen, dass der Kopf direkt ins zweite Segment fährt → sofortiger Tod.
        opposites = {
            constants.UP: constants.DOWN,
            constants.DOWN: constants.UP,
            constants.LEFT: constants.RIGHT,
            constants.RIGHT: constants.LEFT,
        }

        # Richtung nur wechseln, wenn es nicht die direkte Gegenrichtung ist.
        # opposites.get(self.direction) gibt die verbotene Richtung zurück.
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction

    # -------------------------------------------------------------------------
    # move: Snake einen Schritt in die aktuelle Richtung bewegen
    # -------------------------------------------------------------------------
    def move(self):
        # Den aktuellen Kopf auslesen (Index 0 der Körperliste).
        head = self.body[0]

        # Neuen Kopf berechnen: aktuelle Kopfposition + Richtungsvektor.
        # self.direction ist ein Tupel (dx, dy), z.B. RIGHT = (30, 0).
        # direction[0] ist die X-Verschiebung, direction[1] die Y-Verschiebung.
        new_head = [head[0] + self.direction[0],
                    head[1] + self.direction[1]]

        # Den neuen Kopf vorne in die Liste einfügen (Index 0).
        # Jetzt ist die Liste einen Eintrag länger als vorher.
        self.body.insert(0, new_head)

        # Jetzt entscheiden wir, was am Ende der Schlange passiert:
        if not self.grow_status:
            # Normalbewegung: Das letzte Segment entfernen.
            # Die Snake bleibt gleich lang – sie hat sich nur um einen Block verschoben.
            self.body.pop()
        else:
            # Wachstum: Das letzte Segment bleibt erhalten.
            # Die Snake wird um einen Block länger.
            # Danach setzen wir das Flag zurück, damit sie beim nächsten Schritt nicht nochmals wächst.
            self.grow_status = False

    # -------------------------------------------------------------------------
    # draw: Alle Segmente der Snake auf den Bildschirm zeichnen
    # -------------------------------------------------------------------------
    def draw(self, screen):
        s = constants.BLOCK_SIZE  # Kurzname für die Blockgröße

        # enumerate() liefert uns sowohl den Index i als auch das Segment selbst.
        # i == 0 → Kopf, i > 0 → Körper
        for i, seg in enumerate(self.body):
            x, y = seg  # Position des Segments entpacken

            if i == 0:
                # Kopf: gelb gefüllt, mit einem dunkleren Rand.
                # Der Rand wird durch einen zweiten draw.rect-Aufruf mit dem
                # letzten Parameter "2" gezeichnet – das ist die Randbreite in Pixeln.
                pygame.draw.rect(screen, constants.YELLOW, (x, y, s, s))
                pygame.draw.rect(screen, (180, 150, 0), (x, y, s, s), 2)
            else:
                # Körper: ungerade und gerade Segmente wechseln zwischen grün und dunkelgrün.
                # i % 2 gibt den Rest der Division durch 2 zurück:
                #   i % 2 == 0 → gerades Segment  → helleres Grün
                #   i % 2 != 0 → ungerades Segment → dunkleres Grün
                # Das erzeugt einen leichten Schachbretteffekt, der den Körper lesbarer macht.
                color = constants.GREEN if i % 2 == 0 else constants.DARK_GREEN
                pygame.draw.rect(screen, color, (x, y, s, s))
                # Schwarzer 1-Pixel-Rand trennt die einzelnen Segmente optisch voneinander.
                pygame.draw.rect(screen, constants.BLACK, (x, y, s, s), 1)

    # -------------------------------------------------------------------------
    # check_collision: Prüft ob die Snake gegen etwas gestoßen ist
    # -------------------------------------------------------------------------
    def check_collision(self):
        # Nur der Kopf kann kollidieren, der Rest des Körpers folgt immer nach.
        head = self.body[0]

        # Wandkollision: Der Kopf verlässt den erlaubten Pixelbereich.
        # head[0] ist die X-Position, head[1] die Y-Position.
        # Erlaubt: 0 bis WIDTH-1 (X) und 0 bis HEIGHT-1 (Y).
        # not (...) kehrt die Bedingung um: True wenn der Kopf außerhalb liegt.
        if not (0 <= head[0] < constants.WIDTH and 0 <= head[1] < constants.HEIGHT):
            return True

        # Selbstkollision: Prüft ob der Kopf an der gleichen Position wie ein Körpersegment ist.
        # self.body[1:] ist ein Slice – die Liste ohne das erste Element (also ohne den Kopf selbst).
        # Würden wir self.body[0] (den Kopf) mitzählen, gäbe es immer eine Kollision mit sich selbst.
        if head in self.body[1:]:
            return True

        # Kein Hindernis getroffen → alles in Ordnung
        return False


