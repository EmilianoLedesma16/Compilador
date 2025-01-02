import tkinter as tk
from tkinter import messagebox
from lexico import Lexer
from sintactico import Parser
from semantico import SemanticAnalyzer
from simulador import Simulator


def run_compiler():
    source_code = code_text.get("1.0", tk.END).strip()  # Obtener código del área de texto

    if not source_code:
        messagebox.showerror("Error", "El código fuente está vacío.")
        return

    try:
        output_text.delete("1.0", tk.END)  # Limpiar salida anterior

        # Etapa 1: Análisis Léxico
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        output_text.insert(tk.END, "Análisis léxico completado.\nTokens generados:\n")
        for token in tokens:
            output_text.insert(tk.END, f"{token}\n")

        # Etapa 2: Análisis Sintáctico
        parser = Parser(tokens)
        ast = parser.parse()
        if isinstance(ast, str):  # Si devuelve un error sintáctico
            output_text.insert(tk.END, f"Error Sintáctico: {ast}\n")
            return
        output_text.insert(tk.END, "Análisis sintáctico completado.\n")

        # Etapa 3: Análisis Semántico
        semantic_analyzer = SemanticAnalyzer()
        semantic_result = semantic_analyzer.analyze(ast)
        if "Error" in semantic_result:  # Si devuelve un error semántico
            output_text.insert(tk.END, f"Error Semántico: {semantic_result}\n")
            return
        output_text.insert(tk.END, "Análisis semántico completado.\n")

        # Etapa 4: Simulación
        simulator = Simulator(semantic_analyzer)
        simulation_result = simulator.run(ast)
        output_text.insert(tk.END, "Ejecución completada.\n")
        output_text.insert(tk.END, f"Salida:\n{simulation_result}\n")

    except Exception as e:
        output_text.insert(tk.END, f"Error inesperado: {str(e)}\n")


# Crear ventana principal
root = tk.Tk()
root.title("Compilador de Lenguaje Personalizado")
root.geometry("800x600")

# Etiqueta y cuadro de texto para el código fuente
tk.Label(root, text="Código Fuente:", font=("Arial", 12, "bold")).pack(pady=5)
code_text = tk.Text(root, wrap="word", font=("Consolas", 10), height=20)
code_text.pack(fill="both", padx=10, pady=5, expand=True)

# Botón para compilar
compile_button = tk.Button(
    root,
    text="Compilar y Ejecutar",
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    command=run_compiler
)
compile_button.pack(pady=10)

# Etiqueta y cuadro de texto para la salida
tk.Label(root, text="Salida:", font=("Arial", 12, "bold")).pack(pady=5)
output_text = tk.Text(root, wrap="word", font=("Consolas", 10), height=10, bg="#f4f4f4", state="normal")
output_text.pack(fill="both", padx=10, pady=5, expand=True)

# Ejecutar la aplicación
if __name__ == "__main__":
    root.mainloop()
