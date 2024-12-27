from lexico import Lexer
from sintactico import Parser
from semantico import SemanticAnalyzer
from simulador import Interpreter

if __name__ == "__main__":
    # Código fuente de prueba
    code = """
    inicio {
        var x = 10;
        var y = 20;
        imprimir(x);
        imprimir(y);
    } fin
    """

    print("Código Fuente:")
    print(code)
    print("\n======================\n")

    try:
        # Fase 1: Análisis Léxico
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print("Tokens:\n")
        for token in tokens:
            print(token)
        print("\n======================\n")

        # Fase 2: Análisis Sintáctico
        parser = Parser(tokens)
        ast = parser.parse_program()
        print("AST:\n")
        print(ast)
        print("\n======================\n")

        # Fase 3: Análisis Semántico
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        print("Análisis Semántico: Completado\n")
        print("Tabla de Símbolos:", analyzer.symbol_table.symbols)
        print("\n======================\n")

        # Fase 4: Interpretación
        interpreter = Interpreter()
        interpreter.interpret(ast)
        print("\n======================\n")
        print("Interpretación Completada")
        print("Estado Final de la Tabla de Símbolos:", interpreter.symbol_table)

    except Exception as e:
        print("Error:", str(e))
