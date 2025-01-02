class Parser:
    def __init__(self, tokens):
        self.tokens = [t for t in tokens if t[0] != 'NEWLINE']  # Filtrar NEWLINE
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]
        self.stack = ['$']  # Pila inicializada con el símbolo de fin de entrada

        # Tabla LL(1)
        self.table = {
            'Program': {
                'inicio': ['inicio', '{', 'Block', '}', 'fin']
            },
            'Block': {
                'var': ['Statement', 'Block'],
                'IDENTIFIER': ['Statement', 'Block'],
                '}': ['ε']  # epsilon
            },
            'Statement': {
                'var': ['Declaration'],
                'IDENTIFIER': ['Assignment']
            },
            'Declaration': {
                'var': ['var', 'IDENTIFIER', '=', 'Expression', ';']
            },
            'Assignment': {
                'IDENTIFIER': ['IDENTIFIER', '=', 'Expression', ';']
            },
            'Expression': {
                'IDENTIFIER': ['Term', "Expression'"],
                'NUMBER': ['Term', "Expression'"],
                '(': ['Term', "Expression'"]
            },
            "Expression'": {
                '+': ['+', 'Term', "Expression'"],
                '-': ['-', 'Term', "Expression'"],
                'ε': ['ε']  # epsilon
            },
            'Term': {
                'IDENTIFIER': ['Factor', "Term'"],
                'NUMBER': ['Factor', "Term'"],
                '(': ['Factor', "Term'"]
            },
            "Term'": {
                '*': ['*', 'Factor', "Term'"],
                '/': ['/', 'Factor', "Term'"],
                'ε': ['ε']  # epsilon
            },
            'Factor': {
                'NUMBER': ['NUMBER'],
                'IDENTIFIER': ['IDENTIFIER'],
                '(': ['(', 'Expression', ')']
            }
        }

    def advance(self):
        """Avanza al siguiente token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = ('$', None)

    def raise_error(self, message):
        """Lanza un error sintáctico con contexto claro."""
        line, column = self.current_token[2], self.current_token[3]
        raise Exception(f"{message} en línea {line}, columna {column}.")

    def parse(self):
        """Inicia el análisis sintáctico."""
        self.stack.append('Program')  # Añadir el símbolo inicial a la pila

        while self.stack:
            top = self.stack.pop()  # Obtener el elemento superior de la pila
            print(f"Pila: {self.stack}, Top: {top}, Token actual: {self.current_token}")

            if top == 'ε':  # Simboliza epsilon, no consume nada
                continue

            if top in self.table:  # Es un no terminal
                # Usar el valor del token actual (self.current_token[1])
                production = self.table[top].get(self.current_token[1])
                if production is None:
                    raise Exception(
                        f"Error: No hay producción para {top} con token {self.current_token}"
                    )
                print(f"Producción seleccionada para {top}: {production}")
                self.stack.extend(reversed(production))  # Añadir la producción a la pila
            elif top == self.current_token[1]:  # Es un terminal que coincide con el valor del token actual
                print(f"Coincidencia encontrada: {top}")
                self.advance()  # Avanzar al siguiente token
            else:  # Error si no hay coincidencia
                raise Exception(
                    f"Error: Se esperaba {top}, pero se encontró {self.current_token}"
                )

        if self.current_token[0] != '$':  # Aseguramos que se haya consumido toda la entrada
            raise Exception("Error: Entrada no completamente consumida.")
        print("Análisis sintáctico completado sin errores.")

