from sys import argv
from flask import Flask, request, make_response, redirect, url_for
from flask import render_template
import Solver

app = Flask(__name__)

@app.route("/")
def index():
    html = render_template('index.html', correct=True)
    response = make_response(html)
    return response

@app.route('/results', methods=['GET'])
def results():
    scramble = request.args.get("scramble")
    return make_response("<br>".join(Solver.solve_scramble(scramble)))

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='0.0.0.0', port=int(argv[1]), debug=True)