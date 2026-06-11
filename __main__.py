# =============================================================================
# __main__.py – Hauptprogramm
# =============================================================================
# Diese Datei koordiniert den gesamten Spielablauf.
# Sie kümmert sich um drei Zustände:
#
#   1. Startbildschirm  → show_start_screen()
#   2. Laufendes Spiel  → run_game()
#   3. Game Over        → show_gameover_screen()
#
# Die Datei heißt __main__.py, damit man das Spiel als Paket starten kann:
#   python -m snake_game
# Python sucht dann automatisch nach dieser Datei im Ordner.
# =============================================================================

import pygame
import sys
import constants
from snake import Snake
from food import Food


# =============================================================================
# Hilfsfunktionen – werden von allen drei Spielzuständen benutzt
# =============================================================================

def draw_grid(screen):
    # Zeichnet vertikale und horizontale Linien über das gesamte Spielfeld.
    # range(0, WIDTH, BLOCK_SIZE) erzeugt Werte 0, 30, 60, 90 ... bis WIDTH.
    # So entsteht ein gleichmäßiges Raster, das die einzelnen Felder sichtbar macht.
    # Die Farbe DARK_GRAY ist sehr dezent, damit das Raster nicht vom Spiel ablenkt.
    for x in range(0, constants.WIDTH, constants.BLOCK_SIZE):
        pygame.draw.line(screen, constants.DARK_GRAY, (x, 0), (x, constants.HEIGHT))
    for y in range(0, constants.HEIGHT, constants.BLOCK_SIZE):
        pygame.draw.line(screen, constants.DARK_GRAY, (0, y), (constants.WIDTH, y))


def draw_text_centered(screen, text, font, color, y):
    # font.render() wandelt einen String in eine Pygame-Surface (ein Bild) um.
    # True = Antialiasing aktivieren (glattere Schrift).
    surface = font.render(text, True, color)

    # get_rect() gibt das Rechteck der Surface zurück.
    # center=(...) setzt den Mittelpunkt des Rechtecks – so ist der Text automatisch zentriert.
    # constants.WIDTH // 2 ist die horizontale Mitte des Fensters.
    rect = surface.get_rect(center=(constants.WIDTH // 2, y))

    # blit() zeichnet die Text-Surface auf den Bildschirm an der berechneten Position.
    screen.blit(surface, rect)


def draw_button(screen, text, font, rect, color_bg, color_text):
    # Prüfen ob die Maus gerade über dem Button schwebt.
    # rect.collidepoint(mouse) gibt True zurück, wenn der Mauspunkt innerhalb des Rechtecks liegt.
    mouse   = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse)

    # Hover-Effekt: Wenn die Maus über dem Button ist, wird die Hintergrundfarbe aufgehellt.
    # min(c + 40, 255) addiert 40 zu jedem Farbkanal, bleibt aber unter 255 (dem Maximum).
    # tuple(...) baut daraus wieder ein RGB-Tupel.
    bg = tuple(min(c + 40, 255) for c in color_bg) if hovered else color_bg

    # Hintergrund des Buttons zeichnen. border_radius=6 macht die Ecken leicht abgerundet.
    pygame.draw.rect(screen, bg,              rect, border_radius=6)
    # Weißer Rahmen um den Button (letzter Parameter = Randbreite in Pixeln).
    pygame.draw.rect(screen, constants.WHITE, rect, 2, border_radius=6)

    # Text in der Mitte des Buttons zeichnen.
    label = font.render(text, True, color_text)
    screen.blit(label, label.get_rect(center=rect.center))

    # True zurückgeben wenn der Button gerade hover-aktiv ist (für spätere Nutzung möglich).
    return hovered


# =============================================================================
# Spielzustand 1: Startbildschirm
# =============================================================================

def show_start_screen(screen, clock, font_big, font_mid, font_small):
    # Button-Rechteck definieren: pygame.Rect(x, y, breite, höhe)
    # Wir zentrieren ihn horizontal, indem wir von der Fenstermitte die halbe Breite abziehen.
    btn = pygame.Rect(constants.WIDTH // 2 - 120, 520, 240, 60)

    # Eigene Schleife für den Startbildschirm – läuft, bis der Spieler startet.
    while True:
        screen.fill(constants.BLACK)   # Hintergrund schwarz füllen
        draw_grid(screen)              # Raster drüberzeichnen

        # Texte von oben nach unten aufbauen
        draw_text_centered(screen, "🐍  SNAKE",                               font_big,   constants.GREEN, 200)
        draw_text_centered(screen, "Steuere die Schlange mit den Pfeiltasten.", font_small, constants.GRAY,  320)
        draw_text_centered(screen, "Frisst sie ihr eigenes Essen, wächst sie.", font_small, constants.GRAY,  365)
        draw_text_centered(screen, "Berühr nicht die Wand oder dich selbst!",  font_small, constants.GRAY,  410)

        draw_button(screen, "▶  Spielen", font_mid, btn, (0, 100, 0), constants.WHITE)
        draw_text_centered(screen, "oder ENTER drücken", font_small, constants.GRAY, 610)

        # Bildschirm aktualisieren – zeigt alles, was wir bisher gezeichnet haben.
        pygame.display.flip()
        # Framerate begrenzen: Hier brauchen wir keine 8 FPS wie im Spiel,
        # 30 FPS reichen für einen statischen Bildschirm und sparen CPU-Last.
        clock.tick(30)

        # Ereignisse verarbeiten (Tastendrücke, Mausklicks, Fenster schließen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()   # Fenster X-Button → sofort beenden
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return                      # ENTER → Spiel starten
            if event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(event.pos):
                return                      # Button-Klick → Spiel starten


# =============================================================================
# Spielzustand 2: Laufendes Spiel
# =============================================================================

def run_game(screen, clock, font_mid, font_small):
    # Neue Snake und neues Food erstellen – frischer Start für jede Runde.
    snake = Snake()
    food  = Food(snake.body)
    score = 0

    # Hauptspielschleife – läuft jeden Frame, solange das Spiel läuft.
    while True:

        # --- INPUT: Tastatureingaben abfragen --------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                # Pfeiltaste → Richtung wechseln. change_direction() verhindert
                # intern, dass die Snake sich direkt umkehrt.
                if event.key == pygame.K_UP:    snake.change_direction(constants.UP)
                if event.key == pygame.K_DOWN:  snake.change_direction(constants.DOWN)
                if event.key == pygame.K_LEFT:  snake.change_direction(constants.LEFT)
                if event.key == pygame.K_RIGHT: snake.change_direction(constants.RIGHT)

        # --- LOGIK: Spielzustand aktualisieren --------------------------------
        snake.move()   # Snake einen Schritt bewegen

        # Kollision mit Food prüfen: Kopf der Snake == Position des Foods?
        # snake.body[0] ist der Kopf, food.position ist die aktuelle Food-Position.
        if snake.body[0] == food.position:
            snake.grow_status = True    # Snake soll beim nächsten move() wachsen
            score += 1                  # Punkt zählen
            food.randomize(snake.body)  # Food an neue zufällige Position setzen

        # Kollision mit Wand oder sich selbst → Runde beenden.
        # Wir geben den Score zurück, damit der Game-Over-Bildschirm ihn anzeigen kann.
        if snake.check_collision():
            return score

        # --- ZEICHNEN: Aktuellen Spielstand rendern ---------------------------
        screen.fill(constants.BLACK)   # Altes Bild überschreiben
        draw_grid(screen)              # Raster zeichnen
        snake.draw(screen)             # Snake zeichnen
        food.draw(screen)              # Food zeichnen

        # Score-Anzeige oben links (10 Pixel vom Rand)
        score_surf = font_small.render(f"Score: {score}", True, constants.WHITE)
        screen.blit(score_surf, (10, 8))

        pygame.display.flip()          # Fertig gezeichnetes Bild anzeigen
        clock.tick(constants.FPS)      # Auf FPS-Limit warten (steuert die Spielgeschwindigkeit)


# =============================================================================
# Spielzustand 3: Game-Over-Bildschirm
# =============================================================================

def show_gameover_screen(screen, clock, font_big, font_mid, font_small, score, highscore):
    # Zwei Buttons nebeneinander: "Nochmal" links, "Beenden" rechts.
    # Die Mittelpunkte liegen jeweils 260 Pixel links und 40 Pixel rechts der Fenstermitte.
    btn_retry = pygame.Rect(constants.WIDTH // 2 - 260, 560, 220, 60)
    btn_quit  = pygame.Rect(constants.WIDTH // 2 +  40, 560, 220, 60)

    while True:
        screen.fill(constants.BLACK)
        draw_grid(screen)

        # Spielergebnis anzeigen
        draw_text_centered(screen, "GAME OVER",               font_big,   constants.RED,    200)
        draw_text_centered(screen, f"Score:      {score}",    font_mid,   constants.WHITE,  320)
        draw_text_centered(screen, f"Highscore:  {highscore}", font_mid,  constants.YELLOW, 385)

        # Sonderanzeige wenn ein neuer Highscore erreicht wurde.
        # score > 0 verhindert die Anzeige beim allerersten Spielversuch mit 0 Punkten.
        if score == highscore and score > 0:
            draw_text_centered(screen, "🏆  Neuer Highscore!", font_small, constants.YELLOW, 450)

        # Buttons zeichnen (Rückgabewert hovered wird hier nicht weiter gebraucht)
        draw_button(screen, "🔄  Nochmal", font_mid, btn_retry, (0, 100, 0), constants.WHITE)
        draw_button(screen, "✖  Beenden",  font_mid, btn_quit,  (120, 0, 0), constants.WHITE)

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: return "retry"   # ENTER → nochmal spielen
                if event.key == pygame.K_ESCAPE: return "quit"    # ESC   → Spiel beenden
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_retry.collidepoint(event.pos): return "retry"
                if btn_quit.collidepoint(event.pos):  return "quit"


# =============================================================================
# Einstiegspunkt – hier startet das Programm
# =============================================================================

def main():
    pygame.init()   # Pygame-Module initialisieren (muss vor allem anderen aufgerufen werden)

    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()   # Clock steuert die FPS-Begrenzung

    # Drei Schriftgrößen für verschiedene UI-Elemente:
    #   font_big   → Haupttitel und "Game Over"
    #   font_mid   → Buttons und Score-Anzeigen
    #   font_small → Erklärungstexte und laufender Score im Spiel
    font_big   = pygame.font.SysFont("Arial", 80, bold=True)
    font_mid   = pygame.font.SysFont("Arial", 42)
    font_small = pygame.font.SysFont("Arial", 28)

    # Der Highscore wird in dieser Variable über mehrere Runden hinweg gespeichert.
    # Er wird zurückgesetzt, wenn das Programm beendet wird (keine Datei-Speicherung).
    highscore = 0

    # Startbildschirm anzeigen – Funktion kehrt erst zurück, wenn der Spieler startet.
    show_start_screen(screen, clock, font_big, font_mid, font_small)

    # Spielschleife über mehrere Runden: läuft, bis der Spieler "Beenden" wählt.
    while True:
        score = run_game(screen, clock, font_mid, font_small)

        # Highscore aktualisieren, falls dieser Score besser ist.
        if score > highscore:
            highscore = score

        # Game-Over-Bildschirm anzeigen und auf Entscheidung des Spielers warten.
        # Die Funktion gibt "retry" oder "quit" zurück.
        action = show_gameover_screen(screen, clock, font_big, font_mid, font_small, score, highscore)
        if action == "quit":
            break   # Schleife verlassen → weiter zu pygame.quit()

    pygame.quit()   # Pygame sauber beenden und alle Ressourcen freigeben
    sys.exit()      # Python-Prozess beenden


# Dieser Block stellt sicher, dass main() nur aufgerufen wird, wenn die Datei
# direkt gestartet wird – nicht wenn sie von einer anderen Datei importiert wird.
if __name__ == "__main__":
    main()
