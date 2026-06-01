import pygame
import sys

SCREEN_W = 1280
SCREEN_H = 720
FPS = 60
TILE = 64  # tamaño de cada celda del grid en píxeles

# Colores
NEGRO = (10,10,15)
BLANCO = (240,240,240)
GRIS = (100,100,120)
GRIS_OSC = (40,40,55)
ROJO = (210,70,70)
VERDE = (80,190,110)
AMARILLO = (255,210,50)
NARANJA = (255,140,50)
AZUL = (70,130,210)
DORADO = (255,185,0)
COLOR_N1 = (60,140,200) # azul porcelana
COLOR_N2 = (200,80,60)  # rojo chino
COLOR_N3 = (180,140,40)   # dorado auroso

# ── Fuentes ───────────────────────────────────
pygame.font.init()

def fuente(tam, bold=False):
    try:
        return pygame.font.SysFont("segoeui", tam, bold=bold)
    except:
        return pygame.font.Font(None, tam)

F_S = fuente(16)
F_M = fuente(22)
F_L = fuente(32,bold=True)
F_XL = fuente(52,bold=True)
F_TITULO = fuente(80,bold=True)

#Clase menu, maneja las pantallas del menu, seleccion de nivel y muestra controles
class Menu:
    NIVELES_INFO = [
        {
            "nombre": "Restaurante Dragón de Jade",
            "descripcion": "Nivel fácil. Servvir papas fritas\ny dumplings.",
            "color": COLOR_N1,
            "tiempo": "90s",
        },
        {
            "nombre": "Restaurante Fénix Dorado",
            "descripcion": "Nivel medio. Servir chop suey\ny las recetas anteriores.",
            "color": COLOR_N2,
            "tiempo": "120s",
        },
        {
            "nombre": "Restaurante Palacio Imperial",
            "descripcion": "Nivel difícil. Todo lo anterior\nmás arroz cantones.",
            "color": COLOR_N3,
            "tiempo": "150s",
        },
    ]

    def __init__(self, screen):
        self.screen = screen
        self.sub_pantalla = "principal"  # "principal", "niveles", "controles"
        self.hover = None               # key del botón bajo el cursor
        self.botones_actuales = []

    #Procesa eventos como clicks y teclas
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.click(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.sub_pantalla != "principal":
                self.sub_pantalla = "principal"
            else:
                return ("salir", None)
        return None

    #Click del mouse
    def click(self, pos):
        for rect, accion in self.botones_actuales:
            if pygame.Rect(rect).collidepoint(pos):
                return self.ejecutar(accion)
        return None

    #Ejecutar accion del boton
    def ejecutar(self, accion):
        if accion == "jugar":
            self.sub_pantalla = "niveles"
        elif accion == "controles":
            self.sub_pantalla = "controles"
        elif accion == "atras":
            self.sub_pantalla = "principal"
        elif accion == "salir":
            return ("salir", None)
        elif isinstance(accion, tuple) and accion[0] == "nivel":
            return ("jugar", accion[1])
        return None

    #Actualizar estado del menu
    def update(self):
        pos = pygame.mouse.get_pos()
        self.hover = None
        for rect, accion in self.botones_actuales:
            if pygame.Rect(rect).collidepoint(pos):
                self.hover = accion
                break

    #Dibujar la pantalla actual del menu
    def draw(self):
        if self.sub_pantalla == "principal":
            self.draw_principal()
        elif self.sub_pantalla == "niveles":
            self.draw_niveles()
        elif self.sub_pantalla == "controles":
            self.draw_controles()

    #Dibujar menu principal
    def draw_principal(self):
        self.screen.fill(NEGRO)

        # Título
        t1 = F_TITULO.render("CRAZY SNACK RUSH", True, DORADO)
        t2 = F_XL.render("TEC", True, NARANJA)
        sub = F_M.render("Restaurante Chino por Samuel y Jacky", True, GRIS)

        self.screen.blit(t1,  (SCREEN_W//2 - t1.get_width()//2,  80))
        self.screen.blit(t2,  (SCREEN_W//2 - t2.get_width()//2, 175))
        self.screen.blit(sub, (SCREEN_W//2 - sub.get_width()//2, 255))

        # Botones
        botones = [("JUGAR","jugar",COLOR_N2),("CONTROLES", "controles", GRIS_OSC),("SALIR", "salir", GRIS_OSC)]
        self.botones_actuales = []
        for i, (label, accion, color) in enumerate(botones):
            rect = (SCREEN_W//2 - 130, 320 + i * 90, 260, 65)
            self.dibujar_boton(rect, label, accion, color)
            self.botones_actuales.append((rect, accion))

    #Seleccionar nivel
    def draw_niveles(self):
        self.screen.fill(NEGRO)
        titulo = F_L.render("ELIGA SU RESTAURANTE", True, BLANCO)
        self.screen.blit(titulo, (SCREEN_W//2 - titulo.get_width()//2, 40))

        self.botones_actuales = []
        card_w, card_h = 320, 300
        total_w = card_w * 3 + 40 * 2
        start_x = (SCREEN_W - total_w) // 2

        #Crear tarjetas de niveles
        for i, info in enumerate(self.NIVELES_INFO):
            x = start_x + i * (card_w + 40)
            y = 110
            accion = ("nivel", i)
            activo = self.hover == accion

            # Fondo tarjeta
            color_borde = info["color"]
            bg = (50, 45, 60) if not activo else (70, 65, 85)
            pygame.draw.rect(self.screen, bg, (x, y, card_w, card_h), border_radius=16)
            pygame.draw.rect(self.screen, color_borde,(x, y, card_w, card_h), 3, border_radius=16)

            # Número de nivel
            n = F_XL.render(f"#{i+1}", True, color_borde)
            self.screen.blit(n, (x + card_w//2 - n.get_width()//2, y + 20))

            # Nombre
            nombre_surf = F_M.render(info["nombre"], True, BLANCO)
            self.screen.blit(nombre_surf, (x + 16, y + 118))

            # Descripción (multilínea)
            for j, linea in enumerate(info["descripcion"].split("\n")):
                ls = F_S.render(linea, True, GRIS)
                self.screen.blit(ls, (x + 16, y + 170 + j * 22))

            # Tiempo
            ts = F_M.render(f"{info['tiempo']}", True, AMARILLO)
            self.screen.blit(ts, (x + 16, y + card_h - 45))

            self.botones_actuales.append(((x, y, card_w, card_h), accion))

        # Botón atrás
        back = (50, SCREEN_H - 75, 150, 50)
        self.dibujar_boton(back, "ATRÁS", "atras", GRIS_OSC)
        self.botones_actuales.append((back, "atras"))

    #Controles
    def draw_controles(self):
        self.screen.fill(NEGRO)
        titulo = F_L.render("CONTROLES", True, BLANCO)
        self.screen.blit(titulo, (SCREEN_W//2 - titulo.get_width()//2, 40))

        controles = [
            ("WASD  /  Flechas", "Mover al chef activo"),
            ("E  /  Espacio", "Interactuar con estación"),
            ("Tab", "Cambiar entre Chef 1 y Chef 2"),
            ("P", "Pausar"),
            ("ESC", "Volver al menú")]
        
        for i, (tecla, desc) in enumerate(controles):
            y = 140 + i * 80
            pygame.draw.rect(self.screen, GRIS_OSC, (SCREEN_W//2 - 340, y, 680, 60), border_radius=10)
            t_surf = F_L.render(tecla, True, AMARILLO)
            d_surf = F_M.render(desc,  True, BLANCO)
            self.screen.blit(t_surf, (SCREEN_W//2 - 320, y + 10))
            self.screen.blit(d_surf, (SCREEN_W//2 + 10,  y + 15))

        hint = F_S.render("Presione ESC para volver", True, GRIS)
        self.screen.blit(hint, (SCREEN_W//2 - hint.get_width()//2, SCREEN_H - 50))

        self.botones_actuales = []

    #Dibujar botón
    def dibujar_boton(self, rect, label, accion, color_base):
        activo = self.hover == accion
        color = tuple(min(255, c + 30) for c in color_base) if activo else color_base
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        pygame.draw.rect(self.screen, BLANCO, rect, 2, border_radius=12)
        surf = F_L.render(label, True, BLANCO)
        x = rect[0] + rect[2]//2 - surf.get_width()//2
        y = rect[1] + rect[3]//2 - surf.get_height()//2
        self.screen.blit(surf, (x, y))

#Ciclo main
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Crazy Snack Rush TEC")
    clock = pygame.time.Clock()

    estado = "menu" # "menu", "jugando", "pausa", "game_over"
    nivel_elegido = 0
    menu = Menu(screen)
    cocina = None 

    while True:
        clock.tick(FPS)

        #Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if estado == "menu":
                resultado = menu.handle_event(event)
                if resultado:
                    accion, dato = resultado
                    if accion == "salir":
                        pygame.quit()
                        sys.exit()
                    elif accion == "jugar":
                        nivel_elegido = dato
                        #cocina = Cocina(nivel_elegido)
                        estado = "jugando"
                        print(f" Iniciar nivel {nivel_elegido + 1}")

            elif estado == "jugando":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        estado = "menu"
                    elif event.key == pygame.K_p:
                        estado = "pausa"
                    # TAB, E/Espacio

            elif estado == "pausa":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        estado = "jugando"
                    elif event.key == pygame.K_ESCAPE:
                        estado = "menu"

        #Actualizar interfaz
        if estado == "menu":
            menu.update()
        elif estado == "jugando" and cocina:
            pass  # cocina.update(pygame.key.get_pressed())

        #Dibujar interaz
        if estado == "menu":
            menu.draw()
        elif estado == "jugando" and cocina:
            pass  # cocina.draw(screen)
        elif estado == "pausa" and cocina:
            pass  # overlay pausa

        pygame.display.flip()


if __name__ == "__main__":
    main()
