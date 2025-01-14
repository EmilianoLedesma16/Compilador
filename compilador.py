import tkinter as tk
import p_base
import sys

class CustomStdout:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert("end", text)

    def flush(self):
        pass

def compile_code():
    code = code_input.get("1.0", "end").strip()
    result_text.delete("1.0", "end")  # Borrar resultados anteriores

    if code == "":
        return

    # Redirigir la salida estándar a la interfaz gráfica
    sys.stdout = CustomStdout(result_text)

    result, error = p_base.run('<stdin>', code)
    display_result(result, error)

def display_result(result, error):
    if error:
        result_text.insert("end", error.as_string() + "\n")
    elif result:
        if hasattr(result, 'elements') and len(result.elements) == 1:
            result_text.insert("end", repr(result.elements[0]) + "\n")
        else:
            result_text.insert("end", repr(result) + "\n")

# Crear la ventana
window = tk.Tk()
window.title("Compilador Personalizado")

# Ajustar la ventana al tamaño de la pantalla
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

# Crear un marco principal para organizar los elementos
main_frame = tk.Frame(window, bg="#2e3b4e")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Crear el campo de texto para ingresar el código
code_label = tk.Label(main_frame, text="Código Fuente:", font=("Arial", 16), bg="#2e3b4e", fg="white")
code_label.pack(anchor="w", pady=(0, 5))

code_input = tk.Text(main_frame, height=20, width=100, font=("Courier New", 14), bg="#1c1c1c", fg="white", insertbackground="white")
code_input.pack(fill="both", expand=True, pady=(0, 10))

# Crear el botón para compilar y ejecutar
compile_button = tk.Button(main_frame, text="Compilar y Ejecutar", command=compile_code, font=("Arial", 14), bg="#4caf50", fg="white", activebackground="#45a049")
compile_button.pack(pady=(0, 10))

# Crear el campo de texto para mostrar los resultados
result_label = tk.Label(main_frame, text="Resultados:", font=("Arial", 16), bg="#2e3b4e", fg="white")
result_label.pack(anchor="w", pady=(0, 5))

result_text = tk.Text(main_frame, height=20, width=100, font=("Courier New", 14), bg="#1c1c1c", fg="white", state="normal", insertbackground="white")
result_text.pack(fill="both", expand=True)

# Iniciar el bucle de eventos
window.mainloop()
