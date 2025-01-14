# Importar las bibliotecas necesarias
import numpy as np  # Biblioteca para cálculos matemáticos y manejo de arreglos
import tkinter as tk  # Biblioteca para crear interfaces gráficas
from tkinter import ttk  # Widgets mejorados para interfaces gráficas
import matplotlib.pyplot as plt  # Biblioteca para graficar figuras

class TransformationApp:
    """
    Clase principal para gestionar la interfaz gráfica y las operaciones de transformación de figuras geométricas.
    """

    def __init__(self, root):
        """
        Inicializa la aplicación y configura la interfaz gráfica.

        Parámetros:
        - root: Ventana principal de la aplicación (Tkinter).
        """
        self.root = root
        self.root.title("Transformaciones de Figuras")  # Título de la ventana
        self.figure = None  # Figura seleccionada (cuadrado o triángulo)
        self.result_dict = {}  # Diccionario para almacenar las transformaciones aplicadas
        self.vertices = []  # Lista de vértices personalizados

        # Botones principales para crear figuras
        ttk.Button(root, text="Crear Cuadrado", command=self.create_square).pack(pady=5)
        ttk.Label(root, text="Crea un cuadrado predeterminado").pack(anchor="w")

        ttk.Button(root, text="Crear Triángulo", command=self.create_triangle).pack(pady=5)
        ttk.Label(root, text="Crea un triángulo predeterminado").pack(anchor="w")

        ttk.Button(root, text="Agregar Vértice", command=self.add_vertex).pack(pady=5)
        ttk.Label(root, text="Añade vértices personalizados a la figura").pack(anchor="w")

        # Contenedor para las entradas de transformaciones
        frame = ttk.LabelFrame(root, text="Transformaciones")
        frame.pack(pady=10, padx=10, fill=tk.X)

        # Entradas de texto para transformaciones
        self.rotation_entry = self.create_input(frame, "Rotación (°):")
        self.scale_entry = self.create_input(frame, "Escala (Sx, Sy):")
        self.translation_entry = self.create_input(frame, "Traslación (Tx, Ty):")
        self.reflection_entry = self.create_input(frame, "Reflexión (H/V):")

        # Botones para aplicar transformaciones y graficar
        ttk.Button(frame, text="Aplicar Transformaciones", command=self.apply_transformations).pack(pady=5)
        ttk.Label(frame, text="Aplica las transformaciones seleccionadas a la figura actual").pack(anchor="w")

        ttk.Button(frame, text="Graficar", command=self.plot_results).pack(pady=5)
        ttk.Label(frame, text="Genera una gráfica con la figura y sus transformaciones").pack(anchor="w")

    def create_input(self, frame, label):
        """
        Crea una entrada de texto con una etiqueta.

        Parámetros:
        - frame: Contenedor donde se añadirá la entrada.
        - label: Texto que describe la entrada.

        Retorna:
        - entry: Objeto de entrada de texto.
        """
        ttk.Label(frame, text=label).pack(anchor="w")
        entry = ttk.Entry(frame)
        entry.pack(fill=tk.X, padx=5)
        return entry

    def create_square(self):
        """
        Crear un cuadrado predeterminado y almacenarlo en la aplicación.
        """
        self.figure = np.array([[0, 0], [5, 0], [5, 5], [0, 5]])  # Coordenadas del cuadrado
        self.result_dict = {"original": {"value": self.figure, "color": "#1A0014"}}
        print("Cuadrado creado:", self.figure)

    def create_triangle(self):
        """
        Crear un triángulo predeterminado y almacenarlo en la aplicación.
        """
        self.figure = np.array([[0, 0], [5, 0], [2.5, 5]])  # Coordenadas del triángulo
        self.result_dict = {"original": {"value": self.figure, "color": "#1A0014"}}
        print("Triángulo creado:", self.figure)

    def add_vertex(self):
        """
        Agregar un vértice a la lista de vértices personalizados.
        """
        new_vertex = tk.Toplevel(self.root)
        new_vertex.title("Agregar Vértice")

        ttk.Label(new_vertex, text="Coordenada X:").grid(row=0, column=0, padx=5, pady=5)
        x_entry = ttk.Entry(new_vertex)
        x_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(new_vertex, text="Coordenada Y:").grid(row=1, column=0, padx=5, pady=5)
        y_entry = ttk.Entry(new_vertex)
        y_entry.grid(row=1, column=1, padx=5, pady=5)

        def save_vertex():
            try:
                x, y = float(x_entry.get()), float(y_entry.get())
                self.vertices.append([x, y])
                print("Vértice agregado:", [x, y])
                new_vertex.destroy()
            except ValueError:
                print("Error: Coordenadas inválidas.")

        ttk.Button(new_vertex, text="Agregar", command=save_vertex).grid(row=2, column=0, columnspan=2, pady=10)

    def apply_transformations(self):
        """
        Aplicar las transformaciones seleccionadas a la figura actual.
        """
        if self.figure is None and not self.vertices:
            print("No hay figura ni vértices personalizados creados.")
            return

        vertices = self.figure if self.figure is not None else np.array(self.vertices)

        # Rotación
        angle = self.get_float(self.rotation_entry.get(), radians=True)
        if angle:
            matrix = [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
            self.result_dict["rotation"] = {"value": np.dot(vertices, matrix), "color": "#FF5733"}

        # Escala
        scale_values = self.get_float_list(self.scale_entry.get())
        if scale_values and len(scale_values) == 2:
            matrix = [[scale_values[0], 0], [0, scale_values[1]]]
            self.result_dict["scale"] = {"value": np.dot(vertices, matrix), "color": "#33FF57"}

        # Reflexión
        ref_type = self.reflection_entry.get().strip().lower()
        if ref_type == "h":
            matrix = [[1, 0], [0, -1]]
            self.result_dict["reflection"] = {"value": np.dot(vertices, matrix), "color": "#3357FF"}
        elif ref_type == "v":
            matrix = [[-1, 0], [0, 1]]
            self.result_dict["reflection"] = {"value": np.dot(vertices, matrix), "color": "#3357FF"}

        # Traslación
        translation_values = self.get_float_list(self.translation_entry.get())
        if translation_values and len(translation_values) == 2:
            self.result_dict["translation"] = {"value": vertices + translation_values, "color": "#FFD700"}

        print("Transformaciones aplicadas:")
        for key, data in self.result_dict.items():
            print(f"{key}: {data['value']}")

    def plot_results(self):
        """
        Graficar las figuras y sus transformaciones.
        """
        if not self.result_dict:
            print("No hay datos para graficar.")
            return

        fig, ax = plt.subplots(figsize=(6, 6))
        for key, data in self.result_dict.items():
            points = np.array(data["value"])
            points = np.vstack([points, points[0]])  # Cerrar la figura
            ax.fill(points[:, 0], points[:, 1], label=key.capitalize(), alpha=0.5, color=data["color"])
            ax.plot(points[:, 0], points[:, 1], linestyle="--", color="black")

        self.adjust_plot_limits(ax)
        ax.set_aspect("equal")
        ax.legend()
        plt.show()

    def adjust_plot_limits(self, ax):
        """
        Ajustar los límites del gráfico para que las figuras estén siempre visibles y centradas.
        """
        all_points = np.vstack([data["value"] for data in self.result_dict.values()])
        min_x, min_y = np.min(all_points, axis=0)
        max_x, max_y = np.max(all_points, axis=0)
        margin = 1  # Margen para los límites
        ax.set_xlim(min_x - margin, max_x + margin)
        ax.set_ylim(min_y - margin, max_y + margin)

    @staticmethod
    def get_float(value, radians=False):
        """
        Convertir una cadena en un número flotante.

        Parámetros:
        - value: Cadena de texto a convertir.
        - radians: Convertir el valor a radianes si es True.

        Retorna:
        - Número flotante o None si el valor no es válido.
        """
        try:
            val = float(value)
            return np.radians(val) if radians else val
        except ValueError:
            return None

    @staticmethod
    def get_float_list(value):
        """
        Convertir una cadena separada por comas en una lista de flotantes.

        Parámetros:
        - value: Cadena de texto a convertir.

        Retorna:
        - Lista de números flotantes o una lista vacía si el valor no es válido.
        """
        try:
            return list(map(float, value.split(",")))
        except ValueError:
            return []

# Punto de entrada
if __name__ == "__main__":
    root = tk.Tk()
    app = TransformationApp(root)
    root.mainloop()
