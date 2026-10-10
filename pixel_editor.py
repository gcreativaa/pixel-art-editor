import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageDraw

class PixelArtEditor:
    def __init__(self, root, columnas=16, filas=16, tamaño_pixel=30):
        self.root = root
        self.root.title("G-Creativa Pixel Studio")
        
        # Configuraciones de la cuadrícula
        self.columnas = columnas
        self.filas = filas
        self.tamaño_pixel = tamaño_pixel
        
        # Color actual para pintar (por defecto negro)
        self.color_actual = "#000000"
        
        # Matriz para guardar los datos de color de cada píxel
        self.matriz_colores = [["#FFFFFF" for _ in range(columnas)] for _ in range(filas)]
        
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Panel de herramientas (Botones)
        panel_herramientas = tk.Frame(self.root, bg="#2c3e50", pady=10)
        panel_herramientas.pack(fill=tk.X)

        btn_color = tk.Button(panel_herramientas, text="🎨 Elegir Color", command=self.elegir_color, font=("Arial", 10, "bold"))
        btn_color.pack(side=tk.LEFT, padx=10)
        
        btn_limpiar = tk.Button(panel_herramientas, text="🧹 Limpiar Lienzo", command=self.limpiar_lienzo, font=("Arial", 10, "bold"))
        btn_limpiar.pack(side=tk.LEFT, padx=10)

        btn_exportar = tk.Button(panel_herramientas, text="💾 Exportar PNG", command=self.exportar_png, bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
        btn_exportar.pack(side=tk.RIGHT, padx=10)

        # Lienzo de dibujo (Canvas)
        ancho_canvas = self.columnas * self.tamaño_pixel
        alto_canvas = self.filas * self.tamaño_pixel
        
        self.canvas = tk.Canvas(self.root, width=ancho_canvas, height=alto_canvas, bg="#FFFFFF", bd=0, highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)

        # Dibujar la cuadrícula inicial
        self.rectangulos = {}
        for fila in range(self.filas):
            for col in range(self.columnas):
                x1 = col * self.tamaño_pixel
                y1 = fila * self.tamaño_pixel
                x2 = x1 + self.tamaño_pixel
                y2 = y1 + self.tamaño_pixel
                # Creamos el rectángulo y lo guardamos en un diccionario con sus coordenadas
                rect_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FFFFFF", outline="#ecf0f1")
                self.rectangulos[(col, fila)] = rect_id

        # Eventos del ratón
        # Clic izquierdo para pintar, clic derecho para borrar
        self.canvas.bind("<B1-Motion>", self.pintar)
        self.canvas.bind("<Button-1>", self.pintar)
        self.canvas.bind("<B3-Motion>", self.borrar)
        self.canvas.bind("<Button-3>", self.borrar)

    def elegir_color(self):
        color = colorchooser.askcolor(color=self.color_actual)[1]
        if color:
            self.color_actual = color

    def obtener_coordenadas(self, evento):
        # Convierte la posición del ratón en la cuadrícula lógica
        col = evento.x // self.tamaño_pixel
        fila = evento.y // self.tamaño_pixel
        return col, fila

    def pintar(self, evento):
        col, fila = self.obtener_coordenadas(evento)
        if 0 <= col < self.columnas and 0 <= fila < self.filas:
            rect_id = self.rectangulos[(col, fila)]
            self.canvas.itemconfig(rect_id, fill=self.color_actual, outline=self.color_actual)
            self.matriz_colores[fila][col] = self.color_actual

    def borrar(self, evento):
        col, fila = self.obtener_coordenadas(evento)
        if 0 <= col < self.columnas and 0 <= fila < self.filas:
            rect_id = self.rectangulos[(col, fila)]
            self.canvas.itemconfig(rect_id, fill="#FFFFFF", outline="#ecf0f1")
            self.matriz_colores[fila][col] = "#FFFFFF"

    def limpiar_lienzo(self):
        for fila in range(self.filas):
            for col in range(self.columnas):
                rect_id = self.rectangulos[(col, fila)]
                self.canvas.itemconfig(rect_id, fill="#FFFFFF", outline="#ecf0f1")
                self.matriz_colores[fila][col] = "#FFFFFF"

    def exportar_png(self):
        # Pedimos al usuario dónde guardar el archivo
        ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if not ruta:
            return

        # Creamos una imagen en memoria con Pillow basada en nuestra matriz lógica
        imagen = Image.new("RGB", (self.columnas, self.filas), "white")
        pixeles = imagen.load()

        for fila in range(self.filas):
            for col in range(self.columnas):
                # Convertimos el color Hex a RGB
                hex_color = self.matriz_colores[fila][col].lstrip('#')
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                pixeles[col, fila] = rgb_color

        # Guardamos la imagen en su tamaño real de píxel (ej. 16x16)
        imagen.save(ruta)
        print(f"Arte exportado exitosamente a: {ruta}")

if __name__ == "__main__":
    ventana = tk.Tk()
    ventana.resizable(False, False)
    # Iniciamos el editor con un lienzo de 16x16 píxeles
    app = PixelArtEditor(ventana, columnas=16, filas=16, tamaño_pixel=30)
    ventana.mainloop()