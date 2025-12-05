import tkinter as tk
import random

# Configuración básica
ANCHO, ALTO = 400, 400
TAMANO = 20
VELOCIDAD = 150

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        # Canvas
        self.canvas = tk.Canvas(root, bg='black', width=ANCHO, height=ALTO)
        self.canvas.pack()
        
        # Pantalla inicial
        self.mostrar_inicio()
    
    def mostrar_inicio(self):
        self.canvas.create_text(200, 150, text="SNAKE GAME", 
                               fill="white", font=('Arial', 24))
        self.boton = tk.Button(self.root, text="INICIAR", 
                              command=self.iniciar_juego,
                              bg='green', fg='white')
        self.canvas.create_window(200, 220, window=self.boton)
    
    def iniciar_juego(self):
        # Limpiar pantalla
        self.canvas.delete("all")
        self.boton.destroy()
        
        # Inicializar variables
        self.direccion = 'Right'
        self.puntos = 0
        self.activo = True
        
        # Crear serpiente
        self.serpiente = [[200, 200], [180, 200], [160, 200]]
        self.manzana = self.nueva_manzana()
        self.calavera = self.nueva_calavera()
        
        # Dibujar
        self.dibujar_todo()
        
        # Controles
        self.root.bind('<Left>', lambda e: self.cambiar_dir('Left'))
        self.root.bind('<Right>', lambda e: self.cambiar_dir('Right'))
        self.root.bind('<Up>', lambda e: self.cambiar_dir('Up'))
        self.root.bind('<Down>', lambda e: self.cambiar_dir('Down'))
        
        # Iniciar bucle
        self.mover()
    
    def nueva_manzana(self):
        while True:
            x = random.randrange(0, ANCHO//TAMANO) * TAMANO
            y = random.randrange(0, ALTO//TAMANO) * TAMANO
            if [x, y] not in self.serpiente:
                return [x, y]
    
    def nueva_calavera(self):
        while True:
            x = random.randrange(0, ANCHO//TAMANO) * TAMANO
            y = random.randrange(0, ALTO//TAMANO) * TAMANO
            if [x, y] not in self.serpiente and [x, y] != self.manzana:
                return [x, y]
    
    def dibujar_todo(self):
        self.canvas.delete("all")
        
        # Dibujar serpiente
        for i, (x, y) in enumerate(self.serpiente):
            color = 'lightgreen' if i==0 else 'green'
            self.canvas.create_rectangle(x, y, x+TAMANO, y+TAMANO, fill=color)
        
        # Dibujar manzana
        x, y = self.manzana
        self.canvas.create_oval(x+5, y+5, x+TAMANO-5, y+TAMANO-5, fill='red')
        
        # Dibujar calavera
        x, y = self.calavera
        self.canvas.create_text(x+10, y+10, text="💀", font=('Arial', 12))
        
        # Puntos
        self.canvas.create_text(50, 20, text=f"Puntos: {self.puntos}", fill="white")
    
    def cambiar_dir(self, nueva):
        if (nueva == 'Left' and self.direccion != 'Right' or
            nueva == 'Right' and self.direccion != 'Left' or
            nueva == 'Up' and self.direccion != 'Down' or
            nueva == 'Down' and self.direccion != 'Up'):
            self.direccion = nueva
    
    def mover(self):
        if not self.activo:
            return
        
        # Nueva cabeza
        cabeza = self.serpiente[0][:]
        if self.direccion == 'Right': cabeza[0] += TAMANO
        elif self.direccion == 'Left': cabeza[0] -= TAMANO
        elif self.direccion == 'Up': cabeza[1] -= TAMANO
        elif self.direccion == 'Down': cabeza[1] += TAMANO
        
        # Colisiones
        if (cabeza[0] < 0 or cabeza[0] >= ANCHO or
            cabeza[1] < 0 or cabeza[1] >= ALTO or
            cabeza in self.serpiente):
            self.activo = False
            self.canvas.create_text(200, 200, text="GAME OVER", 
                                   fill="red", font=('Arial', 24))
            return
        
        # Mover serpiente
        self.serpiente.insert(0, cabeza)
        
        # Comprobar manzana
        if cabeza == self.manzana:
            self.puntos += 10
            self.manzana = self.nueva_manzana()
        elif cabeza == self.calavera:
            self.puntos -= 5
            if self.puntos < 0: self.puntos = 0
            if len(self.serpiente) > 3:
                self.serpiente.pop()
                self.serpiente.pop()
            self.calavera = self.nueva_calavera()
        else:
            self.serpiente.pop()
        
        # Redibujar
        self.dibujar_todo()
        
        # Continuar
        self.root.after(VELOCIDAD, self.mover)

# Ejecutar
if __name__ == '__main__':
    root = tk.Tk()
    juego = SnakeGame(root)
    root.mainloop()