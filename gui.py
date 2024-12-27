import tkinter as tk
from tkinter import messagebox
from lexico import Lexer
from sintactico import Parser
from semantico import SemanticAnalyzer
from simulador import Interpreter

def compile_code():
    code = code_text.get("1.0", tk.END).strip()
    output_text.delete("1.0", tk.END)

    if not code:
        messagebox.showwarning("Advertencia", "El área de código está vacía.")
        return

    try:
        # Fase 1: Análisis Léxico
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        output_text.insert(tk.END, "Tokens:\n")
        output_text.insert(tk.END, "\n".join(map(str, tokens)) + "\n\n")

        # Fase 2: Análisis Sintáctico
        parser = Parser(tokens)
        ast = parser.parse_program()
        output_text.insert(tk.END, "AST:\n")
        output_text.insert(tk.END, str(ast) + "\n\n")

        # Fase 3: Análisis Semántico
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        output_text.insert(tk.END, "Análisis Semántico: Completado\n")
        output_text.insert(tk.END, f"Tabla de Símbolos: {analyzer.symbol_table.symbols}\n\n")

        # Fase 4: Interpretación
        interpreter = Interpreter()
        interpreter.interpret(ast)
        output_text.insert(tk.END, "Interpretación Completada\n")
        output_text.insert(tk.END, f"Estado Final de la Tabla de Símbolos: {interpreter.symbol_table}\n")

    except Exception as e:
        output_text.insert(tk.END, f"Error: {str(e)}\n")

# Crear ventana principal
root = tk.Tk()
root.title("Compilador Personalizado")

# Área de texto para el código fuente
code_label = tk.Label(root, text="Código Fuente:")
code_label.pack()

code_text = tk.Text(root, height=15, width=80)
code_text.pack()

# Botón para compilar
compile_button = tk.Button(root, text="Compilar", command=compile_code)
compile_button.pack()

# Área de texto para la salida
output_label = tk.Label(root, text="Salida:")
output_label.pack()

output_text = tk.Text(root, height=15, width=80, state=tk.NORMAL)
output_text.pack()

# Ejecutar la interfaz gráfica
root.mainloop()
