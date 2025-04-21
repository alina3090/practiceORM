from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/')
def hello_world():
 return jsonify({'app': 'top films'})
if __name__ == 'main':
 app.run(debug=True)

import structures.views