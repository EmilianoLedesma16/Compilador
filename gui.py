import tkinter as tk
from lexico import Lexer
from sintactico import Parser
from semantico import SemanticAnalyzer
from simulador import Simulator

def compile_code():
    try:
        # Obtener el código fuente desde el área de texto
        source_code = text_area.get("1.0", "end").strip()

        if not source_code:
            raise ValueError("Error: No se ingresó ningún código para compilar.")

        # Análisis léxico
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        print("Análisis léxico completado.")
        print("Tokens generados:")
        for token in tokens:
            print(token)

        # Análisis sintáctico
        parser = Parser(tokens)
        ast = parser.parse()  # AST generado por el parser
        print("Análisis sintáctico completado sin errores.")

        # Análisis semántico
        if not tokens:
            raise ValueError("Error: No se generaron tokens para el análisis semántico.")
        
        semantic_analyzer = SemanticAnalyzer(tokens)
        semantic_analyzer.analyze()
        print("Análisis semántico completado sin errores.")

        # Simulación
        simulator = Simulator(semantic_analyzer)
        output = simulator.run(ast)
        print("Ejecución simulada completada.")

        # Mostrar resultado en la GUI
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Análisis completado sin errores.\n\nSalida de la simulación:\n{output}")
        output_text.configure(state="disabled")
    except Exception as e:
        # Mostrar el error en la GUI
        output_text.configure(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", f"Error: {e}")
        output_text.configure(state="disabled")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Compilador y Simulador")
root.geometry("800x600")

# Área de texto para ingresar el código fuente
text_area = tk.Text(root, wrap="word", height=20, width=90)
text_area.pack(pady=10)

# Botón para compilar el código
compile_button = tk.Button(root, text="Compilar", command=compile_code)
compile_button.pack(pady=10)

# Área de salida para mostrar mensajes
output_text = tk.Text(root, wrap="word", height=10, width=90, state="disabled")
output_text.pack(pady=10)

# Ejecutar la interfaz
root.mainloop()
