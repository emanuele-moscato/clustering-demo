from flask import Flask, jsonify, request, abort, make_response
import pandas as pd

app = Flask(__name__)
PORT = 8000

@app.errorhandler(404)
def not_found(error=None):
    return make_response(jsonify({'error': 'Not found'}))
    
@app.route('/get_data', methods=['GET'])
def get_data():
    data_df = pd.read_csv('../data/data.csv')
    response_body = data_df.to_dict()
    return make_response(jsonify(response_body), 200)
    

if __name__ == '__main__':
    app.run(port=PORT, debug=False)