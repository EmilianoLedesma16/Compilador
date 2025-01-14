import tkinter as tk
import p_base
import sys

class CustomStdout:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert("end", text)

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
        if len(result.elements) == 1:
            result_text.insert("end", repr(result.elements[0]) + "\n")
        else:
            result_text.insert("end", repr(result) + "\n")

# Crear la ventana
window = tk.Tk()
window.title("Interfaz básica")

# Crear el campo de texto para ingresar el código
code_input = tk.Text(window, height=20, width=100)
code_input.pack()

# Crear el botón para compilar y ejecutar
compile_button = tk.Button(window, text="Compilar y Ejecutar", command=compile_code)
compile_button.pack()

# Crear el campo de texto para mostrar los resultados
result_text = tk.Text(window, height=20, width=100)
result_text.pack()

# Iniciar el bucle de eventos
window.mainloop()
