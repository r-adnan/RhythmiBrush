from flask import Flask, request, jsonify 

app = Flask(__name__)

@app.route('/api_endpoint', methods=['GET'])
def api_endpoint():
    print("do stuff")