from flask import Flask, request, render_template
import ply.lex as lex

app = Flask(__name__)

# Define reserved words
reserved = {
    'programa': 'PROGRAMA', 'int': 'INT', 'read': 'READ', 'print': 'PRINT', 'end': 'END',
    'la': 'LA', 'es': 'ES'
}

tokens = (
    'IDENTIFIER', 'NUMBER', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA', 'PLUS', 'MINUS', 'ERROR'
) + tuple(reserved.values())

# Simple rules for individual tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','
t_ignore = ' \t\n'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'IDENTIFIER')
    if t.type == 'IDENTIFIER' and not t.value.isidentifier():
        t.type = 'ERROR'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']
        lexer.input(code)
        tokens_list = []
        sums = { 'Palabra_Reservada': 0, 'Paréntesis_Izquierdo': 0, 'Paréntesis_Derecho': 0, 'Llave_Izquierda': 0, 
                 'Llave_Derecha': 0, 'Punto_y_Coma': 0, 'Variable': 0, 'Operación': 0, 'Coma': 0, 'Error': 0 }
        for tok in lexer:
            token_dict = {
                'TOKEN': tok.type,
                'value': tok.value,
                'Palabra_Reservada': 'X' if tok.type in reserved.values() else '',
                'Paréntesis_Izquierdo': 'X' if tok.type == 'LPAREN' else '',
                'Paréntesis_Derecho': 'X' if tok.type == 'RPAREN' else '',
                'Llave_Izquierda': 'X' if tok.type == 'LBRACE' else '',
                'Llave_Derecha': 'X' if tok.type == 'RBRACE' else '',
                'Punto_y_Coma': 'X' if tok.type == 'SEMICOLON' else '',
                'Variable': 'X' if tok.type == 'IDENTIFIER' else '',
                'Operación': 'X' if tok.type in ['PLUS', 'MINUS'] else '',
                'Coma': 'X' if tok.type == 'COMMA' else '',
                'Error': 'X' if tok.type == 'ERROR' else ''
            }
            tokens_list.append(token_dict)
            # Increment counters for 'X' marks
            for key in sums:
                if token_dict[key] == 'X':
                    sums[key] += 1
        return render_template('index.html', tokens=tokens_list, code=code, sums=sums)
    return render_template('index.html', tokens=[], code='', sums={})

if __name__ == '__main__':
    app.run(debug=True)
