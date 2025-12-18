import tkinter as tk
import random

# --- 1. Constantes y Configuración del Juego ---
ANCHO = 500
ALTO = 500
TAMANO_SEGMENTO = 20
VELOCIDAD = 100  # Menor valor = Mayor velocidad (milisegundos)

# Colores
COLOR_FONDO = 'black'
COLOR_SERPIENTE = 'green'
COLOR_CABEZA = 'lightgreen'
COLOR_MANZANA = 'red'
COLOR_CALAVERA = 'white'

# --- 2. Clases del Juego (Modelos de Game State) ---

class Segmento:
    """Clase simple para manejar las coordenadas de un segmento de la serpiente."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Item:
    """Clase base para los ítems del juego."""
    def __init__(self, x, y, tipo, color, crecimiento):
        self.x = x
        self.y = y
        self.tipo = tipo  # 'manzana' o 'calavera'
        self.color = color
        self.crecimiento = crecimiento  # positivo para crecer, negativo para encoger
        self.canvas_item = None

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de la Serpiente con Crecimiento")
        
        # Variables de estado del juego
        self.direccion = 'Right'
        self.score = 0
        self.juego_activo = False
        self.items = []  # Lista de ítems en el juego
        
        # Inicializar Canvas y Puntuación
        self.canvas = tk.Canvas(root, bg=COLOR_FONDO, width=ANCHO, height=ALTO)
        self.canvas.pack()
        
        self.label_score = tk.Label(root, text="", font=('Arial', 14), fg='white', bg='black')
        self.label_score.pack()
        
        # Iniciar mostrando la pantalla de bienvenida
        self.mostrar_pantalla_inicio()

    # --- 3. Pantalla de Inicio ---
    def mostrar_pantalla_inicio(self):
        """Muestra el mensaje y el botón para que el jugador inicie el juego."""
        
        # Fondo decorativo
        self.canvas.create_rectangle(0, 0, ANCHO, ALTO, fill=COLOR_FONDO, outline=COLOR_FONDO)
        
        # Título del juego
        self.canvas.create_text(
            ANCHO/2, ALTO/2 - 60, 
            text="🐍 SERPIENTE PELIGROSA", 
            fill="white", 
            font=('Arial', 28, 'bold'), 
            tag="inicio"
        )
        
        # Instrucciones
        self.canvas.create_text(
            ANCHO/2, ALTO/2 - 10, 
            text="🍎 Manzana: Crece +1\n💀 Calavera: Encoge -2", 
            fill="white", 
            font=('Arial', 14), 
            tag="inicio"
        )
        
        # Crear un botón de inicio superpuesto al canvas
        self.btn_iniciar = tk.Button(
            self.root, 
            text="🎮 INICIAR JUEGO", 
            command=self.iniciar_juego_logica,
            font=('Arial', 16, 'bold'),
            bg='darkgreen', fg='white',
            relief=tk.RAISED,
            padx=20, pady=10
        )
        # Colocar el botón en el centro
        self.canvas.create_window(ANCHO/2, ALTO/2 + 50, window=self.btn_iniciar)

    def iniciar_juego_logica(self):
        """Prepara las variables, limpia la pantalla de inicio y comienza el bucle."""
        
        # Limpiar la pantalla de inicio
        self.canvas.delete(tk.ALL)
        self.btn_iniciar.destroy()
        
        # Resetear estado del juego
        self.score = 0
        self.direccion = 'Right'
        self.juego_activo = True
        self.items = []
        self.label_score.config(text=f"Puntuación: {self.score} | Longitud: 3")
        
        # Inicializar serpiente con 3 segmentos
        self.lista_cuerpo = [
            Segmento(200, 240),
            Segmento(180, 240), 
            Segmento(160, 240)
        ]
        
        self.objetos_canvas = [] # Representación visual de la serpiente
        
        # Dibujar la serpiente inicial
        for i, seg in enumerate(self.lista_cuerpo):
            if i == 0:  # Cabeza
                color = COLOR_CABEZA
            else:       # Cuerpo
                color = COLOR_SERPIENTE
            segmento = self.canvas.create_rectangle(
                seg.x, seg.y, seg.x + TAMANO_SEGMENTO, seg.y + TAMANO_SEGMENTO,
                fill=color, outline='darkgreen', width=2
            )
            self.objetos_canvas.append(segmento)
        
        # Generar ítems iniciales
        self.generar_items_iniciales()
        
        # Vincular teclas (Input / Controls)
        self.root.bind('<Left>', lambda event: self.cambiar_direccion('Left'))
        self.root.bind('<Right>', lambda event: self.cambiar_direccion('Right'))
        self.root.bind('<Up>', lambda event: self.cambiar_direccion('Up'))
        self.root.bind('<Down>', lambda event: self.cambiar_direccion('Down'))
        
        # Iniciar el bucle de juego
        self.siguiente_movimiento()

    # --- 4. Funciones de Juego ---

    def generar_items_iniciales(self):
        """Genera ítems iniciales en el mapa."""
        # Generar 2 manzanas
        for _ in range(2):
            self.generar_manzana()
        
        # Generar 1 calavera
        for _ in range(1):
            self.generar_calavera()

    def generar_manzana(self):
        """Genera una manzana en posición aleatoria."""
        while True:
            x = random.randrange(0, ANCHO // TAMANO_SEGMENTO) * TAMANO_SEGMENTO
            y = random.randrange(0, ALTO // TAMANO_SEGMENTO) * TAMANO_SEGMENTO
            
            # Verificar que no esté en la serpiente
            if not any(seg.x == x and seg.y == y for seg in self.lista_cuerpo):
                # Verificar que no esté en otro ítem
                if not any(item.x == x and item.y == y for item in self.items):
                    manzana = Item(x, y, 'manzana', COLOR_MANZANA, 1)
                    manzana.canvas_item = self.dibujar_item(manzana)
                    self.items.append(manzana)
                    break

    def generar_calavera(self):
        """Genera una calavera en posición aleatoria."""
        while True:
            x = random.randrange(0, ANCHO // TAMANO_SEGMENTO) * TAMANO_SEGMENTO
            y = random.randrange(0, ALTO // TAMANO_SEGMENTO) * TAMANO_SEGMENTO
            
            # Verificar que no esté en la serpiente
            if not any(seg.x == x and seg.y == y for seg in self.lista_cuerpo):
                # Verificar que no esté en otro ítem
                if not any(item.x == x and item.y == y for item in self.items):
                    calavera = Item(x, y, 'calavera', COLOR_CALAVERA, -2)
                    calavera.canvas_item = self.dibujar_item(calavera)
                    self.items.append(calavera)
                    break

    def dibujar_item(self, item):
        """Dibuja un ítem en el canvas."""
        if item.tipo == 'manzana':
            # Dibujar una manzana
            return self.canvas.create_oval(
                item.x + 3, item.y + 3, 
                item.x + TAMANO_SEGMENTO - 3, item.y + TAMANO_SEGMENTO - 3,
                fill=item.color, outline='darkred', width=2
            )
        else:  # calavera
            # Dibujar una calavera
            return self.canvas.create_polygon(
                item.x + 10, item.y + 5,
                item.x + 15, item.y + 15,
                item.x + 10, item.y + 15,
                item.x + 5, item.y + 15,
                item.x + 10, item.y + 5,
                fill=item.color, outline='gray'
            )

    def cambiar_direccion(self, nueva_direccion):
        """Maneja el Input del usuario (Controls)."""
        if nueva_direccion == 'Left' and self.direccion != 'Right':
            self.direccion = nueva_direccion
        elif nueva_direccion == 'Right' and self.direccion != 'Left':
            self.direccion = nueva_direccion
        elif nueva_direccion == 'Up' and self.direccion != 'Down':
            self.direccion = nueva_direccion
        elif nueva_direccion == 'Down' and self.direccion != 'Up':
            self.direccion = nueva_direccion

    def verificar_colisiones(self, nueva_cabeza):
        """Chequea si la serpiente choca consigo misma o con los bordes."""
        
        # 1. Colisión con los bordes
        if (nueva_cabeza.x < 0 or nueva_cabeza.x >= ANCHO or
            nueva_cabeza.y < 0 or nueva_cabeza.y >= ALTO):
            return True
        
        # 2. Colisión con el cuerpo
        for segmento in self.lista_cuerpo[1:]:
            if nueva_cabeza.x == segmento.x and nueva_cabeza.y == segmento.y:
                return True
            
        return False

    def verificar_colision_items(self, nueva_cabeza):
        """Verifica si la serpiente colisiona con algún ítem."""
        for i, item in enumerate(self.items):
            if nueva_cabeza.x == item.x and nueva_cabeza.y == item.y:
                return i  # Retorna el índice del ítem
        return -1  # No hay colisión

    def procesar_item(self, item_idx):
        """Procesa el efecto de un ítem consumido."""
        item = self.items[item_idx]
        
        # Eliminar el ítem del canvas
        self.canvas.delete(item.canvas_item)
        
        # Aplicar efecto de crecimiento/encogimiento
        crecimiento = item.crecimiento
        
        if crecimiento > 0:  # Manzana - Crecer
            self.score += 10
            # Agregar segmentos según el crecimiento
            for _ in range(crecimiento):
                ultimo_seg = self.lista_cuerpo[-1]
                nuevo_seg = Segmento(ultimo_seg.x, ultimo_seg.y)
                self.lista_cuerpo.append(nuevo_seg)
                # Dibujar el nuevo segmento
                segmento = self.canvas.create_rectangle(
                    nuevo_seg.x, nuevo_seg.y,
                    nuevo_seg.x + TAMANO_SEGMENTO, nuevo_seg.y + TAMANO_SEGMENTO,
                    fill=COLOR_SERPIENTE, outline='darkgreen', width=2
                )
                self.objetos_canvas.append(segmento)
            
            # Generar nueva manzana
            self.generar_manzana()
            
        else:  # Calavera - Encoger
            self.score -= 5
            if self.score < 0:
                self.score = 0
            
            # Eliminar segmentos según el encogimiento
            for _ in range(abs(crecimiento)):
                if len(self.lista_cuerpo) > 3:  # Mantener al menos 3 segmentos
                    # Eliminar el último segmento
                    self.lista_cuerpo.pop()
                    # Eliminar del canvas
                    if self.objetos_canvas:
                        self.canvas.delete(self.objetos_canvas.pop())
            
            # Generar nueva calavera
            self.generar_calavera()
        
        # Eliminar el ítem de la lista
        self.items.pop(item_idx)
        
        # Actualizar puntuación
        self.label_score.config(text=f"Puntuación: {self.score} | Longitud: {len(self.lista_cuerpo)}")
        
        return crecimiento

    def juego_terminado(self):
        """Muestra el mensaje de Game Over."""
        self.juego_activo = False
        
        # Limpiar canvas
        self.canvas.delete(tk.ALL)
        
        # Mostrar mensaje de Game Over
        self.canvas.create_text(
            ANCHO/2, ALTO/2 - 30, 
            text="💀 GAME OVER 💀", 
            fill="red", 
            font=('Arial', 32, 'bold'), 
            tag="gameover"
        )
        
        self.canvas.create_text(
            ANCHO/2, ALTO/2 + 20, 
            text=f"Puntuación Final: {self.score}\nLongitud Máxima: {len(self.lista_cuerpo)}", 
            fill="white", 
            font=('Arial', 18), 
            tag="gameover"
        )
        
        # Mostrar un botón para re-iniciar
        tk.Button(
            self.root, 
            text="🔄 Jugar de Nuevo", 
            command=self.reiniciar_juego,
            font=('Arial', 14),
            bg='darkred', fg='white',
            padx=20, pady=10
        ).pack(pady=20)

    def reiniciar_juego(self):
        """Limpia el estado y vuelve a la pantalla de inicio."""
        # Limpiar elementos adicionales del root
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget != self.btn_iniciar:
                widget.destroy()
        
        # Limpiar canvas y reiniciar
        self.canvas.delete(tk.ALL)
        self.mostrar_pantalla_inicio()

    def siguiente_movimiento(self):
        """Bucle principal que se llama repetidamente."""
        if not self.juego_activo:
            return

        # 1. Calcular la nueva posición de la cabeza
        cabeza_actual = self.lista_cuerpo[0]
        x, y = cabeza_actual.x, cabeza_actual.y
        
        if self.direccion == 'Right':
            nueva_cabeza = Segmento(x + TAMANO_SEGMENTO, y)
        elif self.direccion == 'Left':
            nueva_cabeza = Segmento(x - TAMANO_SEGMENTO, y)
        elif self.direccion == 'Up':
            nueva_cabeza = Segmento(x, y - TAMANO_SEGMENTO)
        elif self.direccion == 'Down':
            nueva_cabeza = Segmento(x, y + TAMANO_SEGMENTO)
            
        # 2. Verificar Colisión con bordes o cuerpo
        if self.verificar_colisiones(nueva_cabeza):
            self.juego_terminado()
            return
            
        # 3. Verificar colisión con ítems
        item_idx = self.verificar_colision_items(nueva_cabeza)
        comio = (item_idx != -1)
        
        # 4. Actualizar el cuerpo de la serpiente
        self.lista_cuerpo.insert(0, nueva_cabeza)
        
        if not comio:
            # Si no comió, eliminar el último segmento (el cuerpo se mueve)
            if self.lista_cuerpo:
                self.lista_cuerpo.pop()
            if self.objetos_canvas:
                self.canvas.delete(self.objetos_canvas.pop())
        else:
            # Procesar el ítem consumido
            crecimiento = self.procesar_item(item_idx)
            
            # Efecto visual
            if crecimiento > 0:
                self.mostrar_efecto("+1", nueva_cabeza.x, nueva_cabeza.y, "green")
            else:
                self.mostrar_efecto("-2", nueva_cabeza.x, nueva_cabeza.y, "red")
        
        # 5. Actualizar colores de la serpiente
        self.actualizar_colores_serpiente()
        
        # 6. Repetir el bucle
        self.root.after(VELOCIDAD, self.siguiente_movimiento)

    def actualizar_colores_serpiente(self):
        """Actualiza los colores de la serpiente (cabeza vs cuerpo)."""
        # Eliminar todos los segmentos visuales
        for obj in self.objetos_canvas:
            self.canvas.delete(obj)
        
        self.objetos_canvas = []
        
        # Redibujar toda la serpiente con colores correctos
        for i, seg in enumerate(self.lista_cuerpo):
            if i == 0:  # Cabeza
                color = COLOR_CABEZA
            else:       # Cuerpo
                # Degradado de color para el cuerpo
                intensidad = min(255, 100 + (i * 10))
                if i % 2 == 0:
                    color = f'#00{int(intensidad):02x}00'
                else:
                    color = COLOR_SERPIENTE
            
            segmento = self.canvas.create_rectangle(
                seg.x, seg.y, seg.x + TAMANO_SEGMENTO, seg.y + TAMANO_SEGMENTO,
                fill=color, outline='darkgreen', width=2
            )
            self.objetos_canvas.append(segmento)

    def mostrar_efecto(self, texto, x, y, color):
        """Muestra un efecto visual cuando se consume un ítem."""
        efecto = self.canvas.create_text(
            x + TAMANO_SEGMENTO/2, y - 10,
            text=texto,
            fill=color,
            font=('Arial', 12, 'bold')
        )
        # El efecto desaparece después de 500ms
        self.root.after(500, lambda: self.canvas.delete(efecto))

# --- Ejecución ---
if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()