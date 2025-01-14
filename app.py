# Importar las bibliotecas necesarias
import numpy as np  # Biblioteca para cálculos matemáticos y manejo de arreglos
import tkinter as tk  # Biblioteca para crear interfaces gráficas
from tkinter import ttk, filedialog  # Widgets avanzados y diálogos para seleccionar archivos
import matplotlib.pyplot as plt  # Biblioteca para generar gráficos y visualizaciones
from datetime import datetime  # Biblioteca para manejar fechas y horas

# Constantes para reflexiones
HORIZONTAL_REFLECTION = 0  # Reflexión horizontal
VERTICAL_REFLECTION = 1  # Reflexión vertical

class TransformationApp:
    """
    Clase principal que gestiona la interfaz gráfica y las transformaciones geométricas.
    """

    def __init__(self, root):
        """
        Inicializa la ventana principal y los componentes de la interfaz.

        Parámetros:
        - root: Ventana raíz de Tkinter.
        """
        self.root = root
        self.root.title("Transformaciones de Figuras")  # Título de la ventana
        self.vertices = []  # Lista de vértices de la figura original
        self.results = {}  # Diccionario para almacenar las transformaciones aplicadas

        # Crear opciones para las figuras geométricas
        ttk.Label(root, text="Opciones de Figura:").grid(row=0, column=0, pady=5, sticky="w")
        self.option_var = tk.StringVar(value="Cuadrado")  # Variable para controlar la figura seleccionada
        options = ["Cuadrado", "Triángulo", "Agregar Vértices", "Cargar desde Archivo"]
        for i, option in enumerate(options):
            ttk.Radiobutton(
                root, text=option, variable=self.option_var, value=option, command=self.update_ui
            ).grid(row=i+1, column=0, sticky="w")

        # Contenedor dinámico para las entradas específicas de la figura seleccionada
        self.dynamic_frame = ttk.Frame(root)
        self.dynamic_frame.grid(row=5, column=0, pady=10)

        # Entradas para transformaciones geométricas
        self.add_transformation_inputs()

        # Botones principales con descripciones
        ttk.Button(root, text="Aplicar Transformaciones", command=self.apply_transformations).grid(row=10, column=0, pady=5)
        ttk.Label(root, text="* Aplica las transformaciones ingresadas a la figura seleccionada.").grid(row=11, column=0, sticky="w")

        ttk.Button(root, text="Graficar Resultados", command=self.plot_results).grid(row=12, column=0, pady=5)
        ttk.Label(root, text="* Muestra la figura original y sus transformaciones.").grid(row=13, column=0, sticky="w")

        ttk.Button(root, text="Guardar Gráfica", command=self.save_image).grid(row=14, column=0, pady=5)
        ttk.Label(root, text="* Guarda la gráfica en un archivo PNG.").grid(row=15, column=0, sticky="w")

        # Inicializar la interfaz dinámica
        self.update_ui()

    def update_ui(self):
        """
        Actualizar la interfaz gráfica según la figura seleccionada.
        """
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        if self.option_var.get() == "Cuadrado":
            self.add_inputs([("x", "0"), ("y", "0"), ("Tamaño", "5")])
        elif self.option_var.get() == "Triángulo":
            self.add_inputs([("x1, y1", "0,0"), ("x2, y2", "5,0"), ("x3, y3", "2.5,5")])
        elif self.option_var.get() == "Agregar Vértices":
            self.add_inputs([("Vértices (x, y separados por ;)", "")])
        elif self.option_var.get() == "Cargar desde Archivo":
            ttk.Button(self.dynamic_frame, text="Seleccionar Archivo", command=self.load_file).grid(row=0, column=0)

    def add_inputs(self, fields):
        """
        Crear entradas dinámicas para las opciones seleccionadas.

        Parámetros:
        - fields: Lista de tuplas con el nombre y el valor predeterminado de las entradas.
        """
        self.inputs = {}
        for i, (label, default) in enumerate(fields):
            ttk.Label(self.dynamic_frame, text=f"{label}:").grid(row=i, column=0, sticky="w")
            entry = ttk.Entry(self.dynamic_frame)
            entry.insert(0, default)
            entry.grid(row=i, column=1)
            self.inputs[label] = entry

    def add_transformation_inputs(self):
        """
        Crear entradas para transformaciones geométricas como rotación, escala y traslación.
        """
        ttk.Label(self.root, text="Transformaciones:").grid(row=6, column=0, pady=10)
        self.rotation_entry = self.create_input("Rotación (°):", 7)
        self.scale_entry = self.create_input("Escala (Sx, Sy):", 8)
        self.translation_entry = self.create_input("Traslación (Tx, Ty):", 9)
        self.reflection_entry = self.create_input("Reflexión (H/V):", 10)

    def create_input(self, label, row):
        """
        Crear un cuadro de entrada con etiqueta.

        Parámetros:
        - label: Texto descriptivo para la entrada.
        - row: Fila donde se ubicará.

        Retorna:
        - Objeto de entrada (Entry) de Tkinter.
        """
        ttk.Label(self.root, text=label).grid(row=row, column=0, sticky="w")
        entry = ttk.Entry(self.root)
        entry.grid(row=row, column=1)
        return entry

    def load_file(self):
        """
        Cargar un archivo JSON con datos de vértices desde el sistema de archivos.
        """
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            print(f"Archivo cargado: {file_path}")

    def get_vertices(self):
        """
        Obtener los vértices de la figura según la opción seleccionada.
        """
        if self.option_var.get() == "Cuadrado":
            x, y, size = map(float, [self.inputs["x"].get(), self.inputs["y"].get(), self.inputs["Tamaño"].get()])
            self.vertices = [[x, y], [x + size, y], [x + size, y + size], [x, y + size]]
        elif self.option_var.get() == "Triángulo":
            self.vertices = [list(map(float, pair.split(","))) for pair in (self.inputs[key].get() for key in self.inputs)]
        elif self.option_var.get() == "Agregar Vértices":
            self.vertices = [list(map(float, pair.split(","))) for pair in self.inputs["Vértices (x, y separados por ;)"].get().split(";")]

    def apply_transformations(self):
        """
        Aplicar transformaciones seleccionadas a la figura cargada.
        """
        self.get_vertices()
        if not self.vertices:
            print("No hay vértices cargados.")
            return

        angle = float(self.rotation_entry.get() or 0) * np.pi / 180
        scale = list(map(float, self.scale_entry.get().split(","))) if self.scale_entry.get() else None
        reflection = HORIZONTAL_REFLECTION if self.reflection_entry.get().lower() == "h" else VERTICAL_REFLECTION if self.reflection_entry.get().lower() == "v" else None
        translation = list(map(float, self.translation_entry.get().split(","))) if self.translation_entry.get() else None

        self.results = {"original": self.vertices}
        vertices = np.array(self.vertices)

        if angle:
            rotation_matrix = [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
            self.results["rotation"] = np.dot(vertices, rotation_matrix).tolist()
        if scale:
            scale_matrix = [[scale[0], 0], [0, scale[1]]]
            self.results["scale"] = np.dot(vertices, scale_matrix).tolist()
        if reflection is not None:
            reflection_matrix = [[1, 0], [0, -1]] if reflection == HORIZONTAL_REFLECTION else [[-1, 0], [0, 1]]
            self.results["reflection"] = np.dot(vertices, reflection_matrix).tolist()
        if translation:
            self.results["translation"] = (vertices + translation).tolist()

        # Mostrar los resultados en la terminal
        for key, value in self.results.items():
            print(f"{key.capitalize()}: {value}")

    def calculate_limits(self):
        """
        Calcular los límites óptimos para centrar y ajustar la gráfica según las figuras creadas.
        """
        all_points = np.concatenate([np.array(v) for v in self.results.values()])
        min_x, min_y = np.min(all_points, axis=0)
        max_x, max_y = np.max(all_points, axis=0)
        return min(min_x, min_y) - 1, max(max_x, max_y) + 1

    def plot_results(self):
        """
        Graficar las figuras y transformaciones aplicadas.
        """
        if not self.results:
            print("No hay resultados para graficar.")
            return

        fig, ax = plt.subplots(figsize=(8, 8))
        for name, points in self.results.items():
            points = np.array(points)
            points = np.vstack([points, points[0]])  # Cerrar figura
            ax.plot(points[:, 0], points[:, 1], label=name, marker="o")

        min_limit, max_limit = self.calculate_limits()
        ax.set_xlim(min_limit, max_limit)
        ax.set_ylim(min_limit, max_limit)
        ax.set_aspect("equal")
        ax.legend()
        plt.show()

    def save_image(self):
        """
        Guardar la gráfica generada como archivo PNG.
        """
        if not self.results:
            print("No hay resultados para guardar.")
            return

        file_name = f"graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig, ax = plt.subplots(figsize=(8, 8))
        for name, points in self.results.items():
            points = np.array(points)
            points = np.vstack([points, points[0]])  # Cerrar figura
            ax.plot(points[:, 0], points[:, 1], label=name, marker="o")

        min_limit, max_limit = self.calculate_limits()
        ax.set_xlim(min_limit, max_limit)
        ax.set_ylim(min_limit, max_limit)
        ax.set_aspect("equal")
        ax.legend()
        fig.savefig(file_name)
        print(f"Gráfica guardada como: {file_name}")

# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TransformationApp(root)
    root.mainloop()
