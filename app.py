from flask import Flask, render_template, request, jsonify
from vocabulary_grapher import create_word_graph
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_projector', methods=['POST'])
def generate_projector():
    axes = {}
    for key, value in request.form.items():
        if 'axis' in key:
            axes[key] = value
    centre_word = request.form['centreWord']

    projector_url = create_word_graph(centre_word, axes.values())
    return jsonify({'url': projector_url})

if __name__ == '__main__':
    app.run(debug=True)
