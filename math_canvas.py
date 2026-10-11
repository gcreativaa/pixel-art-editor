import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw

class MathCanvasEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("G-Creativa Math & Equation Canvas - Pro")
        self.root.geometry("950x650")
        self.root.configure(bg="#2c3e50")

        # Variables lógicas de dibujo
        self.color_actual = "black"    # Color seleccionado en la paleta
        self.color_pincel = "black"    # Color activo (cambia a blanco si usamos la goma)
        self.x_previo = None
        self.y_previo = None
        
        # Imagen en memoria (Pillow) para exportación de alta fidelidad
        self.imagen_memoria = Image.new("RGB", (950, 550), "white")
        self.draw_memoria = ImageDraw.Draw(self.imagen_memoria)

        self.configurar_interfaz()

    def configurar_interfaz(self):
        # Panel Superior de Herramientas (Diseño UI)
        panel_herramientas = tk.Frame(self.root, bg="#34495e", pady=10)
        panel_herramientas.pack(fill=tk.X)

        # --- CONTROLES DE DIBUJO ---
        btn_lapiz = tk.Button(panel_herramientas, text="✏️ Lápiz", command=self.usar_lapiz, font=("Arial", 10, "bold"))
        btn_lapiz.pack(side=tk.LEFT, padx=5)

        # Nuevo botón para la paleta de colores
        btn_color = tk.Button(panel_herramientas, text="🎨 Color", command=self.elegir_color, font=("Arial", 10, "bold"))
        btn_color.pack(side=tk.LEFT, padx=5)

        # Nuevo control deslizante (Slider) para el grosor dinámico
        self.slider_grosor = tk.Scale(panel_herramientas, from_=1, to=30, orient=tk.HORIZONTAL, 
                                      label="Grosor", bg="#34495e", fg="white", 
                                      highlightthickness=0, length=120, font=("Arial", 8))
        self.slider_grosor.set(3) # Grosor inicial predeterminado
        self.slider_grosor.pack(side=tk.LEFT, padx=15)

        btn_goma = tk.Button(panel_herramientas, text="🧽 Goma", command=self.usar_goma, font=("Arial", 10, "bold"))
        btn_goma.pack(side=tk.LEFT, padx=5)

        btn_limpiar = tk.Button(panel_herramientas, text="🗑️ Limpiar Todo", command=self.limpiar_lienzo, font=("Arial", 10, "bold"))
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        # --- CONTROLES DE EXPORTACIÓN ---
        btn_latex = tk.Button(panel_herramientas, text="∑ Exportar a LaTeX", command=self.exportar_latex, bg="#8e44ad", fg="white", font=("Arial", 10, "bold"))
        btn_latex.pack(side=tk.RIGHT, padx=10)

        btn_vector = tk.Button(panel_herramientas, text="📐 Vector EPS", command=self.exportar_vector, bg="#d35400", fg="white", font=("Arial", 10, "bold"))
        btn_vector.pack(side=tk.RIGHT, padx=5)

        btn_png = tk.Button(panel_herramientas, text="💾 PNG/JPG", command=self.exportar_imagen, bg="#27ae60", fg="white", font=("Arial", 10, "bold"))
        btn_png.pack(side=tk.RIGHT, padx=5)

        # --- LIENZO DIGITAL (CANVAS) ---
        self.canvas = tk.Canvas(self.root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Vinculación de eventos del ratón
        self.canvas.bind("<Button-1>", self.iniciar_trazo)
        self.canvas.bind("<B1-Motion>", self.dibujar_trazo)
        self.canvas.bind("<ButtonRelease-1>", self.terminar_trazo)

    # --- LÓGICA DE DIBUJO ---
    def elegir_color(self):
        """Abre la paleta del sistema y actualiza el color activo."""
        color = colorchooser.askcolor(color=self.color_actual)[1]
        if color:
            self.color_actual = color
            self.color_pincel = color # Si elige color, automáticamente vuelve a modo lápiz

    def usar_lapiz(self):
        """Restaura el pincel al color seleccionado."""
        self.color_pincel = self.color_actual

    def usar_goma(self):
        """Cambia el color a blanco para simular el borrado."""
        self.color_pincel = "white"

    def iniciar_trazo(self, event):
        self.x_previo = event.x
        self.y_previo = event.y

    def dibujar_trazo(self, event):
        if self.x_previo and self.y_previo:
            # Obtenemos el grosor en tiempo real desde el slider
            # Si estamos usando la goma, multiplicamos el grosor para borrar más rápido
            grosor_activo = self.slider_grosor.get()
            if self.color_pincel == "white":
                grosor_activo = grosor_activo * 3 

            # Dibuja en la interfaz de usuario
            self.canvas.create_line(self.x_previo, self.y_previo, event.x, event.y, 
                                    width=grosor_activo, fill=self.color_pincel, 
                                    capstyle=tk.ROUND, smooth=True)
            
            # Dibuja simultáneamente en la memoria RAM para exportar después
            self.draw_memoria.line([self.x_previo, self.y_previo, event.x, event.y], 
                                   fill=self.color_pincel, width=grosor_activo)
            
            self.x_previo = event.x
            self.y_previo = event.y

    def terminar_trazo(self, event):
        self.x_previo = None
        self.y_previo = None

    def limpiar_lienzo(self):
        self.canvas.delete("all")
        self.draw_memoria.rectangle([0, 0, 950, 550], fill="white")

    # --- LÓGICA DE EXPORTACIÓN ---
    def exportar_imagen(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")]
        )
        if ruta:
            self.imagen_memoria.save(ruta)
            messagebox.showinfo("Éxito", f"Ecuación guardada como imagen en:\n{ruta}")

    def exportar_vector(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".eps", 
            filetypes=[("Vector EPS", "*.eps")]
        )
        if ruta:
            self.canvas.postscript(file=ruta, colormode='color')
            messagebox.showinfo("Éxito", f"Vector matemático guardado en:\n{ruta}")

    def exportar_latex(self):
        mensaje = (
            "Para convertir escritura a mano en código LaTeX puramente tipográfico, "
            "se requiere conectar este software a una API de Inteligencia Artificial (como Mathpix o OpenAI Vision).\n\n"
            "Tu dibujo matemático actual puede guardarse como vector (.eps) para insertarlo directamente "
            "en tu documento LaTeX usando \\includegraphics{}."
        )
        messagebox.showinfo("Módulo de IA Requerido", mensaje)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = MathCanvasEditor(ventana)
    ventana.mainloop()