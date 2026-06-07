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

#Clase para ingredientes
class Ingrediente:
    def __init__(self, name, pasos, estado = "crudo"):
        self.nombre = name
        self.pasos = pasos
        self.paso_actual = 0
        self.estado = estado  # "crudo", "preparado", "quemado"
        self.tiempo_prep = 0

    @property
    def estacion_actual(self):
        return self.pasos[self.paso_actual][0]

    @property
    def min_prep(self):
        return self.pasos[self.paso_actual][1]

    @property
    def max_prep(self):
        return self.pasos[self.paso_actual][2]

    def actualizar(self):
        if self.estado == "quemado":
            return
        self.tiempo_prep += 1

        if self.estado == "crudo" and self.tiempo_prep >= self.min_prep:
            if self.paso_actual < len(self.pasos)-1:
                self.paso_actual += 1
                self.tiempo_prep = 0
            else:
                self.estado = "preparado"
                self.tiempo_prep = 0

        elif self.estado == "preparado":
            if self.max_prep > 0 and self.tiempo_prep >= self.max_prep:
                self.estado = "quemado"

#Subclases de ingredientes para cada ingrediente
class Papa(Ingrediente):
    def __init__(self):
        super().__init__("Papa", [("tabla",    2*FPS, 0), ("freidora", 3*FPS, 3*FPS)])

class Dumpling(Ingrediente):
    def __init__(self):
        super().__init__("Dumpling", [("olla", 3*FPS, 3*FPS)])

class Fideos(Ingrediente):
    def __init__(self):
        super().__init__("Fideos", [("olla", 5*FPS, 3*FPS)])

class Vegetal(Ingrediente):
    def __init__(self):
        super().__init__("Vegetal", [("tabla", 2*FPS, 0)])

class Carne(Ingrediente):
    def __init__(self):
        super().__init__("Carne", [("sarten", 6*FPS, 4*FPS)])

class Arroz(Ingrediente):
    def __init__(self):
        super().__init__("Arroz", [("olla", 4*FPS, 3*FPS)])

class Huevo(Ingrediente):
    def __init__(self):
        super().__init__("Huevo", [("sarten", 3*FPS, 2*FPS)])

class PlatoPreparado(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre, [("entrega", 0, 0)])
        self.estado = "preparado"

#Clase para recetas
class Receta:
    def __init__(self, nombre, ingredientes, puntos, tiempo):
        self.nombre = nombre
        self.ingredientes = ingredientes
        self.puntos = puntos
        self.tiempo_limite = tiempo

    def verificar(self, ingredientes):
        if len(ingredientes) != len(self.ingredientes):
            return False
        
        disponibles = list(ingredientes)

        for nom in self.ingredientes:
            encontrado = False
            for i, ing in enumerate(disponibles):
                if ing.nombre == nom and ing.estado == "preparado":
                    disponibles.pop(i)
                    encontrado = True
                    break
            if not encontrado:
                return False
        return True

#Nivel 1
receta_papas = Receta("Papas Fritas", ["Papa"], 15, 40)
receta_dumpling = Receta("Dumplings",    ["Dumpling"], 10, 30)

#Nivel 2
receta_chopsuey = Receta("Chop Suey", ["Fideos", "Vegetal", "Carne"], 25, 60)

#Nivel 3
receta_cantones = Receta("Arroz Cantones", ["Arroz", "Huevo", "Vegetal", "Carne"], 40, 90)

#Clase para estaciones de trabajo
class Estacion:
    def __init__(self, tipo, ingredientes_aceptados=None):
        self.tipo = tipo  # dispensador, tabla, olla, sarten, freidora, wok, entrega
        self.ocupada = False
        self.ingrediente = None
        self.ingredientes_aceptados = ingredientes_aceptados

    def actualizar(self):
        if self.ingrediente:
            self.ingrediente.actualizar()

    def interactuar(self, chef):
        pass

#Estaciones 
class Dispensador(Estacion):
    def __init__(self, tipo_ingrediente):
        super().__init__("dispensador")
        self.tipo_ingrediente = tipo_ingrediente

    def interactuar(self, chef):
        if chef.mano is None:
            chef.mano = self.tipo_ingrediente()

class Tabla(Estacion):
    def __init__(self, ingredientes_aceptados):
        super().__init__("tabla", ingredientes_aceptados)

    def interactuar(self, chef):
        if chef.mano is None:
            return
        ing = chef.mano
        if ing.nombre in self.ingredientes_aceptados and ing.estacion_actual == self.tipo:
            ing.actualizar()

class EstacionTrabajo(Estacion):
    def __init__(self, tipo, ingredientes_aceptados):
        super().__init__(tipo, ingredientes_aceptados)

    def interactuar(self, chef):
        if chef.mano is not None: #Dejar ingrediente
            ing = chef.mano
            if ing.nombre in self.ingredientes_aceptados and ing.estacion_actual == self.tipo and self.ingrediente is None:
                self.ingrediente = ing
                self.ocupada = True
                chef.mano = None

        else: #Recoger ingrediente
            if self.ingrediente and self.ingrediente.estado == "preparado" and chef.mano is None:
                chef.mano = self.ingrediente
                self.ingrediente = None
                self.ocupada = False

class Wok(Estacion):
    def __init__(self, ingredientes_aceptados):
        super().__init__("wok", ingredientes_aceptados)
        self.ingredientes_dentro = []
        self.resultado = None

    def interactuar(self, chef):
        if self.resultado and chef.mano is None: #Recoger cantones
            chef.mano = self.resultado
            self.resultado = None
            self.ingredientes_dentro = []
            return

        if chef.mano is not None: #Dejar ingrediente compatible
            if self.resultado is not None: #No se puede agregar mas ingredientes si ya esta listo
                return
            ing = chef.mano
            nombres_dentro = [i.nombre for i in self.ingredientes_dentro]
            if ing.nombre in self.ingredientes_aceptados and ing.estado == "preparado" and ing.nombre not in nombres_dentro:
                self.ingredientes_dentro.append(ing)
                chef.mano = None
                if len(self.ingredientes_dentro) == len(self.ingredientes_aceptados): #Ver si ya estan todos
                    self.resultado = PlatoPreparado("Cantones")

class Entrega(Estacion):
    def __init__(self, recetas):
        super().__init__("entrega")
        self.plato = []
        self.recetas = recetas

    def interactuar(self, chef):
        if chef.mano is not None and chef.mano.estado == "preparado":
            self.plato.append(chef.mano)
            chef.mano = None
        elif chef.mano is None:
            for receta in self.recetas:
                if receta.verificar(self.plato):
                    self.plato = []
                    return receta.puntos
            self.plato = []
            return 0
        

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
