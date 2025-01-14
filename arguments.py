# Importar las bibliotecas necesarias
import numpy as np  # Biblioteca para cálculos matemáticos y manejo de arreglos
import tkinter as tk  # Biblioteca para crear interfaces gráficas
from tkinter import ttk, filedialog  # Widgets avanzados y diálogos para seleccionar archivos
import matplotlib.pyplot as plt  # Biblioteca para generar gráficos y visualizaciones
from datetime import datetime  # Biblioteca para manejar fechas y horas

class TransformationApp:
    """
    Clase principal que gestiona la interfaz gráfica y las transformaciones geométricas.
    """

    def __init__(self, root):
        """
        Inicializa la ventana principal y los componentes de la interfaz.

        Parámetros:
        - root: Ventana principal de la aplicación (Tkinter).
        """
        self.root = root
        self.root.title("Transformaciones de Figuras")  # Título de la ventana

        self.vertices = []  # Lista de vértices iniciales
        self.transformed_vertices = {}  # Diccionario para almacenar transformaciones aplicadas

        # Crear opciones principales de figuras
        ttk.Label(root, text="Opciones de Figura:").grid(row=0, column=0, pady=5, sticky="w")
        self.option = tk.StringVar(value="square")  # Variable para controlar la opción seleccionada
        options = [("Cuadrado", "square"), ("Triángulo", "triangle"), ("Agregar Vértices", "vertex")]
        for i, (label, value) in enumerate(options):
            ttk.Radiobutton(root, text=label, variable=self.option, value=value, command=self.update_interface).grid(row=i+1, column=0, sticky="w")

        # Contenedor dinámico para las entradas específicas de la figura seleccionada
        self.dynamic_frame = ttk.Frame(root)
        self.dynamic_frame.grid(row=5, column=0, pady=10)

        # Botones principales para interactuar con las figuras y transformaciones
        ttk.Button(root, text="Aplicar Transformaciones", command=self.apply_transformations).grid(row=6, column=0, pady=5)
        ttk.Label(root, text="(Aplica las transformaciones especificadas en los campos)").grid(row=6, column=1, sticky="w")

        ttk.Button(root, text="Graficar Resultados", command=self.plot_data).grid(row=7, column=0, pady=5)
        ttk.Label(root, text="(Muestra la figura original y sus transformaciones)").grid(row=7, column=1, sticky="w")

        ttk.Button(root, text="Guardar Gráfica", command=self.save_graphic).grid(row=8, column=0, pady=5)
        ttk.Label(root, text="(Guarda la gráfica actual como archivo PNG)").grid(row=8, column=1, sticky="w")

        # Contenedor para las entradas de transformaciones geométricas
        self.transformation_frame = ttk.Frame(root)
        self.transformation_frame.grid(row=9, column=0, pady=10)
        self.add_transformation_inputs()

        # Inicializar la interfaz dinámica
        self.update_interface()

    def update_interface(self):
        """
        Actualizar la interfaz gráfica según la figura seleccionada.
        """
        # Limpiar widgets existentes en el área dinámica
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        # Configurar entradas específicas según la opción seleccionada
        if self.option.get() == "square":
            self.add_inputs([("x", "0"), ("y", "0"), ("Tamaño", "5")])
        elif self.option.get() == "triangle":
            self.add_inputs([("x1, y1", "0,0"), ("x2, y2", "5,0"), ("x3, y3", "2.5,5")])
        elif self.option.get() == "vertex":
            self.add_inputs([("Vértices (x, y separados por ;)", "")])

    def add_inputs(self, fields):
        """
        Crear entradas dinámicas basadas en los campos proporcionados.

        Parámetros:
        - fields: Lista de tuplas con el nombre y el valor predeterminado de las entradas.
        """
        self.inputs = {}  # Diccionario para almacenar referencias a las entradas
        for i, (label, default) in enumerate(fields):
            ttk.Label(self.dynamic_frame, text=label).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(self.dynamic_frame)
            entry.insert(0, default)
            entry.grid(row=i, column=1)
            self.inputs[label] = entry

    def add_transformation_inputs(self):
        """
        Crear entradas para transformaciones geométricas como rotación, escala y traslación.
        """
        self.transformations = {}
        fields = [("Rotación (°)", "rotation"), ("Escala (Sx, Sy)", "scale"), ("Traslación (Tx, Ty)", "translation")]
        for i, (label, key) in enumerate(fields):
            ttk.Label(self.transformation_frame, text=label).grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(self.transformation_frame)
            entry.grid(row=i, column=1)
            self.transformations[key] = entry

    def apply_transformations(self):
        """
        Aplicar las transformaciones seleccionadas a la figura cargada.
        """
        self.get_vertices()
        if not self.vertices:
            print("No hay vértices cargados.")
            return

        angle = self.get_float(self.transformations["rotation"].get(), radians=True)
        scale = self.get_float_list(self.transformations["scale"].get())
        translation = self.get_float_list(self.transformations["translation"].get())

        self.transformed_vertices = {"original": self.vertices}
        vertices = np.array(self.vertices)

        if angle is not None:
            rotation_matrix = [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
            self.transformed_vertices["rotation"] = np.dot(vertices, rotation_matrix).tolist()

        if scale and len(scale) == 2:
            scale_matrix = [[scale[0], 0], [0, scale[1]]]
            self.transformed_vertices["scale"] = np.dot(vertices, scale_matrix).tolist()

        if translation and len(translation) == 2:
            translated = vertices + translation
            self.transformed_vertices["translation"] = translated.tolist()

        # Mostrar transformaciones en la terminal
        print("Transformaciones aplicadas:")
        for key, value in self.transformed_vertices.items():
            print(f"{key.capitalize()}: {value}")

    def get_vertices(self):
        """
        Obtener los vértices de la figura según la opción seleccionada.
        """
        if self.option.get() == "square":
            x, y, size = map(float, [self.inputs["x"].get(), self.inputs["y"].get(), self.inputs["Tamaño"].get()])
            self.vertices = [[x, y], [x + size, y], [x + size, y + size], [x, y + size]]
        elif self.option.get() == "triangle":
            self.vertices = [list(map(float, pair.split(","))) for pair in self.inputs.values()]
        elif self.option.get() == "vertex":
            self.vertices = [list(map(float, pair.split(","))) for pair in self.inputs["Vértices (x, y separados por ;)"].get().split(";")]

    def calculate_limits(self):
        """
        Calcular los límites óptimos para centrar y ajustar la gráfica según las figuras creadas.
        """
        all_points = np.concatenate([np.array(v) for v in self.transformed_vertices.values()])
        min_x, min_y = np.min(all_points, axis=0)
        max_x, max_y = np.max(all_points, axis=0)
        margin = 1  # Margen adicional para la visualización
        return min(min_x, min_y) - margin, max(max_x, max_y) + margin

    def plot_data(self):
        """
        Graficar las figuras y transformaciones aplicadas.
        """
        if not self.transformed_vertices:
            print("No hay datos para graficar.")
            return

        fig, ax = plt.subplots(figsize=(8, 8))
        for key, vertices in self.transformed_vertices.items():
            vertices = np.array(vertices)
            vertices = np.vstack([vertices, vertices[0]])  # Cerrar la figura
            ax.fill(vertices[:, 0], vertices[:, 1], alpha=0.5, label=key.capitalize())
            ax.plot(vertices[:, 0], vertices[:, 1], linestyle="--", color="black")

        min_limit, max_limit = self.calculate_limits()
        ax.set_xlim(min_limit, max_limit)
        ax.set_ylim(min_limit, max_limit)
        ax.set_aspect("equal")
        ax.legend()
        plt.show()

    def save_graphic(self):
        """
        Guardar la gráfica generada como un archivo PNG.
        """
        if not self.transformed_vertices:
            print("No hay resultados para guardar.")
            return

        file_name = f"graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig, ax = plt.subplots(figsize=(8, 8))
        for key, vertices in self.transformed_vertices.items():
            vertices = np.array(vertices)
            vertices = np.vstack([vertices, vertices[0]])
            ax.fill(vertices[:, 0], vertices[:, 1], alpha=0.5, label=key.capitalize())
            ax.plot(vertices[:, 0], vertices[:, 1], linestyle="--", color="black")

        min_limit, max_limit = self.calculate_limits()
        ax.set_xlim(min_limit, max_limit)
        ax.set_ylim(min_limit, max_limit)
        ax.set_aspect("equal")
        ax.legend()
        fig.savefig(file_name)
        print(f"Gráfica guardada como: {file_name}")

    def get_float(self, value, radians=False):
        """
        Convierte un valor de cadena a flotante.

        Parámetros:
        - value: Cadena a convertir.
        - radians: Convertir a radianes si es True.

        Retorna:
        - Flotante o None si la conversión falla.
        """
        try:
            value = float(value)
            return np.radians(value) if radians else value
        except ValueError:
            return None

    def get_float_list(self, value):
        """
        Convierte una cadena separada por comas a una lista de flotantes.

        Parámetros:
        - value: Cadena de texto a convertir.

        Retorna:
        - Lista de números flotantes o lista vacía si falla.
        """
        try:
            return [float(x) for x in value.split(",")]
        except ValueError:
            return []

# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TransformationApp(root)
    root.mainloop()
