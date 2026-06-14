import pygame
import sys
import random

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
receta_cantones = Receta("Arroz Cantones", ["Cantones"], 40, 90)

#Clase para estaciones de trabajo
class Estacion:
    def __init__(self, tipo, x, y, ingredientes_aceptados=None):
        self.tipo = tipo  # dispensador, tabla, olla, sarten, freidora, wok, entrega
        self.x = x
        self.y = y
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
    def __init__(self, x, y, tipo_ingrediente):
        super().__init__("dispensador", x, y)
        self.tipo_ingrediente = tipo_ingrediente

    def interactuar(self, chef):
        if chef.mano is None:
            chef.mano = self.tipo_ingrediente()

class Tabla(Estacion):
    def __init__(self, x, y, ingredientes_aceptados):
        super().__init__("tabla", x, y, ingredientes_aceptados)

    def interactuar(self, chef):
        if chef.mano is None:
            return
        ing = chef.mano
        if ing.nombre in self.ingredientes_aceptados and ing.estacion_actual == self.tipo:
            ing.actualizar()

class EstacionTrabajo(Estacion):
    def __init__(self, tipo, x, y, ingredientes_aceptados):
        super().__init__(tipo, x, y, ingredientes_aceptados)

    def interactuar(self, chef):
        if chef.mano is not None: #Dejar ingrediente
            ing = chef.mano
            if ing.nombre in self.ingredientes_aceptados and ing.estacion_actual == self.tipo and self.ingrediente is None:
                self.ingrediente = ing
                self.ocupada = True
                chef.mano = None

        else: #Recoger ingrediente
            if self.ingrediente and self.ingrediente.estado == "preparado":
                chef.mano = self.ingrediente
                self.ingrediente = None
                self.ocupada = False

class Wok(Estacion):
    def __init__(self, x, y, ingredientes_aceptados):
        super().__init__("wok", x, y, ingredientes_aceptados)
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
    def __init__(self, x, y, recetas):
        super().__init__("entrega", x, y)
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
                    return receta
            self.plato = []
            return None

#Clase para el Chef
class Chef:
    def __init__(self, name, dir, x, y):
        self.nombre = name
        self.mano = None
        self.direccion = dir #"arriba", "abajo", "izquierda", "derecha"
        self.x, self.y = x, y
        self.puntos = 0

    def mover(self, x, y):
        self.x += x
        self.y += y
        if x == 1:
            self.direccion = "derecha"
        elif x == -1:
            self.direccion = "izquierda"
        elif y == 1:
            self.direccion = "abajo"
        elif y == -1:
            self.direccion = "arriba"

    def interactuar(self, estaciones):
        deltas = {
        "arriba": (0, -1),
        "abajo": (0,  1),
        "izquierda": (-1, 0),
        "derecha": (1,  0)}

        x, y = deltas[self.direccion]
        frente_x = self.x + x
        frente_y = self.y + y

        for estacion in estaciones:
            if estacion.x == frente_x and estacion.y == frente_y:
                return estacion.interactuar(self)
        return None

    def agregar_puntos(self, puntos):
        self.puntos += puntos

class Cocina:
    def __init__(self, chefs, estaciones, recetas_posibles, tiempo_total, paredes=None):
        self.chefs = chefs
        self.estaciones = estaciones
        self.recetas_posibles = recetas_posibles
        self.recetas_activas = []
        self.tiempo = tiempo_total * FPS
        self.puntaje = 0
        self.chef_activo = 0
        self.paredes = paredes or set()
        self.spawn_timer = 0
        self.spawn_intervalo = 8 * FPS
        self.max_recetas = 4

        #Primera receta al iniciar
        self.generar_receta()

    def cambiar_chef(self):
        self.chef_activo = 1 - self.chef_activo #Cambio entre 0 y 1

    def generar_receta(self):
        if len(self.recetas_activas) < self.max_recetas:
            receta = random.choice(self.recetas_posibles)
            self.recetas_activas.append({
                "receta": receta,
                "tiempo_restante": receta.tiempo_limite * FPS,
                "puntos_actuales": receta.puntos,
            })

    def mover_chef(self, dx, dy):
        chef = self.chefs[self.chef_activo]
        nuevo_x = chef.x + dx
        nuevo_y = chef.y + dy

        #Verificar límites de la cocina, gira el chef si intenta salir
        bloqueado = (nuevo_x, nuevo_y) in self.paredes
        if not bloqueado:
            for est in self.estaciones:
                if est.x == nuevo_x and est.y == nuevo_y:
                    bloqueado = True
                    break

        if bloqueado:
            if dx == 1:  chef.direccion = "derecha"
            if dx == -1: chef.direccion = "izquierda"
            if dy == 1:  chef.direccion = "abajo"
            if dy == -1: chef.direccion = "arriba"
        else:
            chef.mover(dx, dy)

    def interactuar(self):
        chef = self.chefs[self.chef_activo]
        resultado = chef.interactuar(self.estaciones)
        if resultado is not None:
            self.entregar(resultado)

    def entregar(self, receta):
        chef = self.chefs[self.chef_activo]
        for r in self.recetas_activas[:]:
            if r["receta"] is receta:
                self.puntaje += r["puntos_actuales"]
                chef.agregar_puntos(r["puntos_actuales"])
                self.recetas_activas.remove(r)
                break

    #Verificar presion en tabla para cortar
    def actualizar_tabla(self, teclas):
        chef = self.chefs[self.chef_activo]
        if not (teclas[pygame.K_e] or teclas[pygame.K_SPACE]):
            return

        movimiento = {"arriba":(0,-1), "abajo":(0,1), "izquierda":(-1,0), "derecha":(1,0)}
        dx, dy = movimiento[chef.direccion]
        fx, fy = chef.x + dx, chef.y + dy

        for est in self.estaciones:
            if est.x == fx and est.y == fy and isinstance(est, Tabla):
                est.interactuar(chef)
    
    #Actualizaciones de tablero
    def update(self, teclas):
        self.tiempo -= 1

        # movimiento del chef activo
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.mover_chef(0, -1)
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.mover_chef(0, 1)
        elif teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.mover_chef(-1, 0)
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.mover_chef(1, 0)

        # cortar en tabla si la tecla está sostenida
        self.actualizar_tabla(teclas)

        # actualizar cocción/preparación en estaciones
        for est in self.estaciones:
            est.actualizar()

        # actualizar tiempos de recetas activas
        for r in self.recetas_activas[:]:
            r["tiempo_restante"] -= 1
            if r["tiempo_restante"] <= 0:
                r["puntos_actuales"] = r["puntos_actuales"] // 2 #Penaliza puntaje a la mitad por no entregar
                r["tiempo_restante"] = r["receta"].tiempo_limite * FPS
                if r["puntos_actuales"] <= 0:
                    self.puntaje = max(0, self.puntaje - r["receta"].puntos)
                    self.recetas_activas.remove(r)

        # generar recetas nuevas con el tiempo
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_intervalo:
            self.spawn_timer = 0
            self.generar_receta()

        # ¿se acabó el tiempo?
        return self.tiempo > 0
    
    #Dibujar la cocina, chefs, estaciones y HUD
    def draw(self, screen, offset_x=0, offset_y=0):
        # estaciones
        for est in self.estaciones:
            self.draw_estacion(screen, est, offset_x, offset_y)

        # chefs
        for i, chef in enumerate(self.chefs):
            self.draw_chef(screen, chef, offset_x, offset_y, activo=(i == self.chef_activo))

        # HUD
        self.draw_hud(screen)

    def draw_estacion(self, screen, est, ox, oy):
        px = ox + est.x * TILE
        py = oy + est.y * TILE
        colores = {
            "dispensador": GRIS,
            "tabla": VERDE,
            "olla": NARANJA,
            "sarten": ROJO,
            "freidora": AMARILLO,
            "wok": AZUL,
            "entrega": DORADO,
        }
        color = colores.get(est.tipo, GRIS_OSC)
        pygame.draw.rect(screen, color, (px, py, TILE-2, TILE-2), border_radius=8)

        etiqueta = F_S.render(est.tipo[:4].upper(), True, NEGRO)
        screen.blit(etiqueta, (px + 4, py + 4))

        if est.ingrediente:
            ing_s = F_S.render(est.ingrediente.nombre[:4], True, BLANCO)
            screen.blit(ing_s, (px + 4, py + TILE - 20))

    def draw_chef(self, screen, chef, ox, oy, activo):
        px = ox + chef.x * TILE
        py = oy + chef.y * TILE
        color = AMARILLO if activo else AZUL
        pygame.draw.circle(screen, color, (px + TILE//2, py + TILE//2), TILE//3)

        nombre_s = F_S.render(chef.nombre, True, BLANCO)
        screen.blit(nombre_s, (px, py - 18))

        if chef.mano:
            ing_s = F_S.render(chef.mano.nombre[:4], True, BLANCO)
            screen.blit(ing_s, (px + TILE//2 - 10, py + TILE//2 - 8))

    def draw_hud(self, screen):
        seg = max(0, self.tiempo // FPS)
        t_s = F_L.render(f"{seg//60:02d}:{seg%60:02d}", True, BLANCO) #tiempo surface
        screen.blit(t_s, (20, 20))

        p_s = F_L.render(f"{self.puntaje}", True, DORADO) #puntaje surface
        screen.blit(p_s, (SCREEN_W - p_s.get_width() - 20, 20))

        for i, r in enumerate(self.recetas_activas):
            x = 20 + i * 180
            y = 80
            pygame.draw.rect(screen, GRIS_OSC, (x, y, 170, 80), border_radius=10)
            nombre_s = F_S.render(r["receta"].nombre, True, BLANCO)
            pts_s = F_S.render(f"{r['puntos_actuales']}", True, AMARILLO)
            seg_r = max(0, r["tiempo_restante"] // FPS)
            t_r_s = F_S.render(f"{seg_r}s", True, GRIS)
            screen.blit(nombre_s, (x + 8, y + 8))
            screen.blit(pts_s, (x + 8, y + 30))
            screen.blit(t_r_s, (x + 8, y + 52))

#Generar paredes para niveles
def generar_paredes(ancho, alto):
    paredes = set()
    for x in range(ancho):
        paredes.add((x, 0))         # pared superior
        paredes.add((x, alto - 1))  # pared inferior
    for y in range(alto):
        paredes.add((0, y))         # pared izquierda
        paredes.add((ancho - 1, y)) # pared derecha
    return paredes

#Nivel 1
NIVEL1_PAREDES = generar_paredes(11, 8)

NIVEL1_RECETAS = [receta_papas, receta_dumpling]

NIVEL1_ESTACIONES = [
    Dispensador(2, 0, Papa),
    Dispensador(9, 0, Dumpling),
    Tabla(3, 7, ["Papa"]),
    EstacionTrabajo("olla", 6, 7, ["Dumpling"]),
    EstacionTrabajo("freidora", 8, 7, ["Papa"]),
    Entrega(10, 3, NIVEL1_RECETAS)
]

NIVEL1_CHEFS = [
    Chef("Pedri", "abajo", 5, 3),
    Chef("Gavi", "abajo", 5, 4)
]

#Nivel 2


#Nivel 3


#Facilitar acceso
NIVELES = [
    {
        "chefs": NIVEL1_CHEFS,
        "estaciones": NIVEL1_ESTACIONES,
        "recetas": NIVEL1_RECETAS,
        "paredes": NIVEL1_PAREDES,
        "tiempo": 90,
    }
]

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
                        config = NIVELES[nivel_elegido]
                        cocina = Cocina(config["chefs"], config["estaciones"], config["recetas"], config["tiempo"], config["paredes"])
                        estado = "jugando"

            elif estado == "jugando":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        estado = "menu"
                    elif event.key == pygame.K_p:
                        estado = "pausa"
                    elif event.key == pygame.K_TAB:
                        cocina.cambiar_chef()
                    elif event.key in (pygame.K_e, pygame.K_SPACE):
                        cocina.interactuar()

            elif estado == "pausa":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        estado = "jugando"
                    elif event.key == pygame.K_ESCAPE:
                        estado = "menu"

            elif estado == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        estado = "menu"
                        cocina = None

        #Actualizar interfaz
        if estado == "menu":
            menu.update()
        elif estado == "jugando" and cocina:
            sigue = cocina.update(pygame.key.get_pressed())
            if not sigue:
                estado = "game_over"

        #Dibujar interaz
        if estado == "menu":
            menu.draw()
        elif estado == "jugando" and cocina:
            screen.fill(NEGRO)
            cocina.draw(screen, offset_x=64, offset_y=64)
        elif estado == "pausa" and cocina:
            screen.fill(NEGRO)
            cocina.draw(screen, offset_x=64, offset_y=64)
            overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            pausa_s = F_TITULO.render("PAUSA", True, BLANCO)
            screen.blit(pausa_s, (SCREEN_W//2 - pausa_s.get_width()//2, SCREEN_H//2 - 40))
        elif estado == "game_over":
            screen.fill(NEGRO)
            go_s = F_TITULO.render("¡TIEMPO!", True, ROJO)
            pts_s = F_XL.render(f"Puntaje: {cocina.puntaje}", True, DORADO)
            screen.blit(go_s, (SCREEN_W//2 - go_s.get_width()//2, 200))
            screen.blit(pts_s, (SCREEN_W//2 - pts_s.get_width()//2, 320))
            hint = F_M.render("Presione ESC para volver al menú", True, GRIS)
            screen.blit(hint, (SCREEN_W//2 - hint.get_width()//2, 420))

        pygame.display.flip()


if __name__ == "__main__":
    main()
