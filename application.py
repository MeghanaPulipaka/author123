from flask import Flask, jsonify, request
from AuthorConnection.Model import get_connected_authors_final

app = Flask(__name__)

@app.route('/home', methods=['GET'])
def GetAuthorsBasedOnId():
       id= "authorID_d6e5a_20b30_f8721_6b2c7_58f5e"
       data = get_connected_authors_final(id)
       return jsonify(data)


if __name__ == '__main__':
    app.run(debug = True)
