import tkinter as tk
from tkinter import messagebox
from lexico import Lexer
from sintactico import Parser
from semantico import SemanticAnalyzer
from simulador import Simulator

def run_compiler():
    source_code = code_text.get("1.0", tk.END).strip()

    if not source_code:
        messagebox.showerror("Error", "El código fuente está vacío.")
        return

    try:
        # Análisis léxico
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        # Análisis sintáctico
        parser = Parser(tokens)
        ast = parser.parse_program()

        # Análisis semántico
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)

        # Simulación
        simulator = Simulator(semantic_analyzer)
        simulator.run(ast)

        output_text.insert(tk.END, "\nCompilación y ejecución completadas con éxito.\n")
    except Exception as e:
        output_text.insert(tk.END, f"\nError: {str(e)}\n")

# Interfaz gráfica
root = tk.Tk()
root.title("Compilador de Lenguaje Personalizado")
root.geometry("800x600")

# Etiqueta y cuadro de texto para el código fuente
tk.Label(root, text="Código Fuente:", font=("Arial", 12, "bold")).pack(pady=5)
code_text = tk.Text(root, wrap="word", font=("Consolas", 10), height=20)
code_text.pack(fill="both", padx=10, pady=5, expand=True)

# Botón para compilar
compile_button = tk.Button(
    root, text="Compilar y Ejecutar", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
    command=run_compiler
)
compile_button.pack(pady=10)

# Etiqueta y cuadro de texto para la salida
tk.Label(root, text="Salida:", font=("Arial", 12, "bold")).pack(pady=5)
output_text = tk.Text(root, wrap="word", font=("Consolas", 10), height=10, state="normal", bg="#f4f4f4")
output_text.pack(fill="both", padx=10, pady=5, expand=True)

# Iniciar la aplicación
root.mainloop()
