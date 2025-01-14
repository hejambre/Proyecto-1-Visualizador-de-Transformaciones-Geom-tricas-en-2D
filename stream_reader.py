# Importar las bibliotecas necesarias
import json  # Para manejar archivos JSON
import numpy as np  # Biblioteca para cálculos matemáticos y manejo de arreglos
import tkinter as tk  # Biblioteca para crear interfaces gráficas
from tkinter import filedialog, ttk  # Widgets avanzados y diálogos para seleccionar archivos
import matplotlib.pyplot as plt  # Biblioteca para crear gráficos y visualizaciones
from datetime import datetime  # Biblioteca para manejar fechas y horas

class TransformationApp:
    """
    Clase principal que gestiona la interfaz gráfica y las transformaciones geométricas.
    """

    def __init__(self, root):
        """
        Inicializa la interfaz de usuario y configura los componentes principales.

        Parámetros:
        - root: Ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Transformaciones desde Archivo")  # Título de la ventana
        self.result_dict = {}  # Diccionario para almacenar los resultados de las transformaciones
        self.max_value = 1  # Límite inicial de los ejes en las gráficas

        # Crear botones principales para cargar y transformar figuras
        ttk.Button(root, text="Cargar Archivo", command=self.load_file).pack(pady=5)
        ttk.Label(root, text="(Carga un archivo JSON con vértices y configuraciones)").pack(anchor="w")

        ttk.Button(root, text="Aplicar Rotación", command=self.apply_rotation).pack(pady=5)
        ttk.Label(root, text="(Aplica rotación según el ángulo especificado)").pack(anchor="w")

        ttk.Button(root, text="Aplicar Escala", command=self.apply_scale).pack(pady=5)
        ttk.Label(root, text="(Escala los vértices según los valores proporcionados)").pack(anchor="w")

        ttk.Button(root, text="Aplicar Traslación", command=self.apply_translation).pack(pady=5)
        ttk.Label(root, text="(Traslada los vértices según los valores especificados)").pack(anchor="w")

        ttk.Button(root, text="Graficar Resultados", command=self.plot_results).pack(pady=5)
        ttk.Label(root, text="(Genera una gráfica con los resultados de las transformaciones)").pack(anchor="w")

        ttk.Button(root, text="Guardar Gráfica", command=self.save_graphic).pack(pady=5)
        ttk.Label(root, text="(Guarda la gráfica como archivo PNG)").pack(anchor="w")

        # Contenedor para entradas de transformación
        self.transformation_frame = ttk.Frame(root, padding=10)
        self.transformation_frame.pack(pady=10)
        self.add_transformation_inputs()

    def load_file(self):
        """
        Carga un archivo JSON con configuraciones de vértices y transformaciones.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if file_path:
            try:
                self.result_dict, self.max_value = self.load_from_file(file_path)
                print(f"Archivo cargado: {file_path}")
                print("Contenido cargado:")
                for key, data in self.result_dict.items():
                    print(f"{key}: {data['value']}")
            except Exception as e:
                print(f"Error al cargar el archivo: {e}")

    def load_from_file(self, filename):
        """
        Procesa un archivo JSON para extraer puntos y aplicar transformaciones iniciales.

        Parámetros:
        - filename: Ruta del archivo JSON.

        Retorna:
        - result_dict: Diccionario con los resultados de las transformaciones iniciales.
        - max_value: Valor máximo para ajustar los ejes de las gráficas.
        """
        with open(filename, "r") as file:
            config = json.load(file)

        vertices = np.array(config.get("points", []))
        if not len(vertices):
            raise ValueError("No se encontraron puntos en el archivo.")

        result_dict = {"original": {"value": vertices, "color": "#1A0014"}}
        min_value, max_value = np.min(vertices), np.max(vertices)

        # Aplicar transformaciones especificadas en el archivo
        if "rotation" in config:
            angle = np.radians(config["rotation"].get("angle", 90))
            result = self.rotation(vertices, angle)
            result_dict["rotation"] = {"value": result, "color": "#FF5733"}
            min_value, max_value = min(min_value, np.min(result)), max(max_value, np.max(result))

        if "scale" in config:
            sx, sy = config["scale"].get("value", [1, 1])
            result = self.scale(vertices, sx, sy)
            result_dict["scale"] = {"value": result, "color": "#33FF57"}
            min_value, max_value = min(min_value, np.min(result)), max(max_value, np.max(result))

        if "translation" in config:
            tx, ty = config["translation"].get("value", [0, 0])
            result = self.translation(vertices, tx, ty)
            result_dict["translation"] = {"value": result, "color": "#FFD700"}
            min_value, max_value = min(min_value, np.min(result)), max(max_value, np.max(result))

        return result_dict, max(abs(max_value), abs(min_value))

    def add_transformation_inputs(self):
        """
        Crear entradas para las transformaciones geométricas (rotación, escala y traslación).
        """
        ttk.Label(self.transformation_frame, text="Rotación (°):").grid(row=0, column=0, sticky="w")
        self.rotation_entry = ttk.Entry(self.transformation_frame)
        self.rotation_entry.grid(row=0, column=1)

        ttk.Label(self.transformation_frame, text="Escala (Sx, Sy):").grid(row=1, column=0, sticky="w")
        self.scale_entry = ttk.Entry(self.transformation_frame)
        self.scale_entry.grid(row=1, column=1)

        ttk.Label(self.transformation_frame, text="Traslación (Tx, Ty):").grid(row=2, column=0, sticky="w")
        self.translation_entry = ttk.Entry(self.transformation_frame)
        self.translation_entry.grid(row=2, column=1)

    def apply_rotation(self):
        """
        Aplicar rotación a los vértices cargados.
        """
        if "original" not in self.result_dict:
            print("No hay datos cargados para transformar.")
            return

        angle = self.get_float(self.rotation_entry.get(), radians=True)
        if angle:
            vertices = np.array(self.result_dict["original"]["value"])
            self.result_dict["rotation"] = {"value": self.rotation(vertices, angle), "color": "#FF5733"}
            print("Rotación aplicada:", self.result_dict["rotation"]["value"])

    def apply_scale(self):
        """
        Aplicar escala a los vértices cargados.
        """
        if "original" not in self.result_dict:
            print("No hay datos cargados para transformar.")
            return

        scale = self.get_float_list(self.scale_entry.get())
        if scale and len(scale) == 2:
            vertices = np.array(self.result_dict["original"]["value"])
            self.result_dict["scale"] = {"value": self.scale(vertices, *scale), "color": "#33FF57"}
            print("Escala aplicada:", self.result_dict["scale"]["value"])

    def apply_translation(self):
        """
        Aplicar traslación a los vértices cargados.
        """
        if "original" not in self.result_dict:
            print("No hay datos cargados para transformar.")
            return

        translation = self.get_float_list(self.translation_entry.get())
        if translation and len(translation) == 2:
            vertices = np.array(self.result_dict["original"]["value"])
            self.result_dict["translation"] = {"value": self.translation(vertices, *translation), "color": "#FFD700"}
            print("Traslación aplicada:", self.result_dict["translation"]["value"])

    def calculate_limits(self):
        """
        Calcula los límites para centrar las figuras en el gráfico.
        """
        all_points = np.concatenate([data["value"] for data in self.result_dict.values()])
        min_limit, max_limit = np.min(all_points, axis=0), np.max(all_points, axis=0)
        margin = 1  # Margen para ajustar los límites
        return min_limit[0] - margin, max_limit[0] + margin, min_limit[1] - margin, max_limit[1] + margin

    def plot_results(self):
        """
        Generar una gráfica con los resultados de las transformaciones aplicadas.
        """
        if not self.result_dict:
            print("No hay resultados para graficar.")
            return

        fig, ax = plt.subplots(figsize=(8, 8))
        for key, data in self.result_dict.items():
            points = np.array(data["value"])
            points = np.vstack([points, points[0]])  # Cerrar la figura
            ax.fill(points[:, 0], points[:, 1], alpha=0.5, label=key.capitalize(), color=data["color"])
            ax.plot(points[:, 0], points[:, 1], linestyle="--", color="black")

        min_x, max_x, min_y, max_y = self.calculate_limits()
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_aspect("equal")
        ax.legend()
        plt.show()

    def save_graphic(self):
        """
        Guardar la gráfica generada como un archivo PNG.
        """
        if not self.result_dict:
            print("No hay resultados para guardar.")
            return

        file_name = f"graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig, ax = plt.subplots(figsize=(8, 8))
        for key, data in self.result_dict.items():
            points = np.array(data["value"])
            points = np.vstack([points, points[0]])  # Cerrar la figura
            ax.fill(points[:, 0], points[:, 1], alpha=0.5, label=key.capitalize(), color=data["color"])
            ax.plot(points[:, 0], points[:, 1], linestyle="--", color="black")

        min_x, max_x, min_y, max_y = self.calculate_limits()
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_aspect("equal")
        ax.legend()
        fig.savefig(file_name)
        print(f"Gráfica guardada como: {file_name}")

    @staticmethod
    def rotation(vertices, angle):
        """
        Aplica una rotación a los vértices.

        Parámetros:
        - vertices: Arreglo de vértices.
        - angle: Ángulo de rotación en radianes.

        Retorna:
        - Arreglo de vértices rotados.
        """
        return np.dot(vertices, [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

    @staticmethod
    def scale(vertices, sx, sy):
        """
        Aplica una escala a los vértices.

        Parámetros:
        - vertices: Arreglo de vértices.
        - sx: Escala en el eje x.
        - sy: Escala en el eje y.

        Retorna:
        - Arreglo de vértices escalados.
        """
        return np.dot(vertices, [[sx, 0], [0, sy]])

    @staticmethod
    def translation(vertices, tx, ty):
        """
        Aplica una traslación a los vértices.

        Parámetros:
        - vertices: Arreglo de vértices.
        - tx: Traslación en el eje x.
        - ty: Traslación en el eje y.

        Retorna:
        - Arreglo de vértices trasladados.
        """
        return vertices + [tx, ty]

    @staticmethod
    def get_float(value, radians=False):
        """
        Convierte un valor de cadena a flotante.

        Parámetros:
        - value: Cadena a convertir.
        - radians: Si es True, convierte el valor a radianes.

        Retorna:
        - Flotante o None si la conversión falla.
        """
        try:
            val = float(value)
            return np.radians(val) if radians else val
        except ValueError:
            return None

    @staticmethod
    def get_float_list(value):
        """
        Convierte una cadena separada por comas a una lista de flotantes.

        Parámetros:
        - value: Cadena de texto a convertir.

        Retorna:
        - Lista de números flotantes o una lista vacía si falla.
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
