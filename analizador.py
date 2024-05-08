from flask import Flask, request, render_template
import ply.lex as lex

tokens = (
    'IDENTIFIER',
    'FOR',
    'IF',
    'DO',
    'WHILE',
    'ELSE',
    'LPAREN',
    'RPAREN',
)

def t_FOR(t):
    r'\bfor\b|\bFOR\b'
    t.type = 'FOR'
    t.description = 'Reservada for'
    return t

def t_IF(t):
    r'\bif\b|\bIF\b'
    t.type = 'IF'
    t.description = 'Reservada if'
    return t

def t_DO(t):
    r'\bdo\b|\bDO\b'
    t.type = 'DO'
    t.description = 'Reservada do'
    return t

def t_WHILE(t):
    r'\bwhile\b|\bWHILE\b'
    t.type = 'WHILE'
    t.description = 'Reservada while'
    return t

def t_ELSE(t):
    r'\belse\b|\bELSE\b'
    t.type = 'ELSE'
    t.description = 'Reservada else'
    return t


def t_LPAREN(t):
    r'\('
    t.type = 'LPAREN'
    t.description = 'Parentesis de apertura'
    return t

def t_RPAREN(t):
    r'\)'
    t.type = 'RPAREN'
    t.description = 'Parentesis de cierre'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'IDENTIFIER'
    t.description = 'Identificador'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.txt'):
                code = file.read().decode('utf-8')
            else:
                return "File type not supported"
        else:
            code = request.form['code']
        lexer.input(code)
        line_counter = 1
        tokens = []
        for token in lexer:
            tokens.append({'type': token.type, 'value': token.value, 'line': line_counter, 'description': token.description})
            if token.value in ['(', ')']:
                line_counter += 1
            else:
                words = token.value.split()
                line_counter += len(words)
        return render_template('index.html', tokens=tokens)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    