# importação
from flask import Flask

app = Flask(__name__)

# definir uma rota raiz (página inicial) e a função que será executada ao requisitar
@app.route('/teste')
def hello_world():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True)
