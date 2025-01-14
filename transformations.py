# Importar las bibliotecas necesarias
import numpy as np  # Biblioteca para cálculos matemáticos y manejo de arreglos
import tkinter as tk  # Biblioteca para crear interfaces gráficas
from tkinter import ttk  # Widgets mejorados para interfaces gráficas
import matplotlib.pyplot as plt  # Biblioteca para graficar figuras

class TransformationApp:
    """
    Clase principal que gestiona la interfaz gráfica y las operaciones de creación y graficación de figuras geométricas.
    """

    def __init__(self, root):
        """
        Inicializa la aplicación y configura la interfaz gráfica.

        Parámetros:
        - root: Ventana principal de la aplicación (Tkinter).
        """
        self.root = root
        self.root.title("Figuras y Transformaciones")  # Título de la ventana
        self.figure = []  # Almacena la figura actual
        self.vertices = []  # Almacena vértices personalizados

        # Crear botones principales para las figuras
        ttk.Button(root, text="Crear Triángulo", command=self.create_triangle).pack(pady=5)
        ttk.Label(root, text="Crea un triángulo predeterminado").pack(anchor="w")

        ttk.Button(root, text="Crear Cuadrado", command=self.create_square).pack(pady=5)
        ttk.Label(root, text="Crea un cuadrado predeterminado").pack(anchor="w")

        ttk.Button(root, text="Crear Círculo", command=self.create_circle).pack(pady=5)
        ttk.Label(root, text="Crea un círculo predeterminado").pack(anchor="w")

        ttk.Button(root, text="Agregar Vértice", command=self.add_vertex).pack(pady=5)
        ttk.Label(root, text="Añade vértices personalizados a la figura").pack(anchor="w")

        ttk.Button(root, text="Graficar Figura y Vértices", command=self.plot_results).pack(pady=10)
        ttk.Label(root, text="Muestra la figura creada y los vértices personalizados").pack(anchor="w")

    def create_triangle(self):
        """
        Crear un triángulo equilátero predeterminado y almacenarlo.
        """
        self.figure = np.array([[0, 0], [6, 0], [3, 5]])  # Coordenadas del triángulo
        print("Triángulo creado:", self.figure)

    def create_square(self):
        """
        Crear un cuadrado predeterminado y almacenarlo.
        """
        self.figure = np.array([[0, 0], [5, 0], [5, 5], [0, 5]])  # Coordenadas del cuadrado
        print("Cuadrado creado:", self.figure)

    def create_circle(self):
        """
        Crear un círculo predeterminado y almacenarlo.
        """
        x, y, radius = 0, 0, 5  # Centro y radio del círculo
        angles = np.linspace(0, 2 * np.pi, 100)  # Ángulos en radianes para el círculo
        self.figure = np.array([[x + radius * np.cos(a), y + radius * np.sin(a)] for a in angles])  # Coordenadas del círculo
        print("Círculo creado:", self.figure)

    def add_vertex(self):
        """
        Agregar un vértice a la lista de vértices personalizados mediante una ventana emergente.
        """
        vertex_window = tk.Toplevel(self.root)
        vertex_window.title("Agregar Vértice")

        ttk.Label(vertex_window, text="Coordenada X:").grid(row=0, column=0, padx=5, pady=5)
        x_entry = ttk.Entry(vertex_window)
        x_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(vertex_window, text="Coordenada Y:").grid(row=1, column=0, padx=5, pady=5)
        y_entry = ttk.Entry(vertex_window)
        y_entry.grid(row=1, column=1, padx=5, pady=5)

        def save_vertex():
            try:
                x, y = float(x_entry.get()), float(y_entry.get())
                self.vertices.append([x, y])
                print("Vértice agregado:", [x, y])
                vertex_window.destroy()
            except ValueError:
                print("Error: Las coordenadas deben ser números válidos.")

        ttk.Button(vertex_window, text="Guardar Vértice", command=save_vertex).grid(row=2, column=0, columnspan=2, pady=10)

    def plot_results(self):
        """
        Graficar las figuras creadas junto con los vértices personalizados.
        """
        if not self.figure and not self.vertices:  # Verificar si hay figuras o vértices creados
            print("No hay figura ni vértices creados.")
            return

        fig, ax = plt.subplots(figsize=(8, 8))

        # Graficar la figura principal si existe
        if self.figure:
            points = np.vstack([self.figure, self.figure[0]])  # Cerrar la figura conectando el último punto con el primero
            ax.plot(points[:, 0], points[:, 1], linestyle="--", color="black", label="Figura")  # Líneas de contorno
            ax.fill(points[:, 0], points[:, 1], alpha=0.5, color="blue")  # Relleno de la figura
            print("Figura graficada:", self.figure)

        # Graficar los vértices personalizados
        if self.vertices:
            vertices_array = np.array(self.vertices)
            ax.scatter(vertices_array[:, 0], vertices_array[:, 1], color="red", label="Vértices Personalizados")
            print("Vértices personalizados graficados:", self.vertices)

        # Ajustar límites del gráfico
        self.adjust_plot_limits(ax)

        # Configurar estilo del gráfico
        ax.set_aspect("equal")
        ax.grid(True, linestyle="--", linewidth=0.5)
        ax.set_title("Figura y Vértices")
        ax.legend()
        plt.show()

    def adjust_plot_limits(self, ax):
        """
        Ajustar los límites del gráfico para incluir todas las figuras y vértices.

        Parámetros:
        - ax: Objeto de ejes del gráfico.
        """
        all_points = np.vstack([self.figure] if self.figure else [])
        if self.vertices:
            all_points = np.vstack([all_points, np.array(self.vertices)]) if all_points.size > 0 else np.array(self.vertices)

        if all_points.size > 0:
            min_x, min_y = np.min(all_points, axis=0)
            max_x, max_y = np.max(all_points, axis=0)
            margin = 1  # Márgenes alrededor de los límites
            ax.set_xlim(min_x - margin, max_x + margin)
            ax.set_ylim(min_y - margin, max_y + margin)

# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TransformationApp(root)
    root.mainloop()
