import os, logging
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from psycopg2 import pool
from util import *

DB_HOST = os.environ["DBHOST"]
DB_PORT = os.environ["DBPORT"]
DB_USER = os.environ["DBUSER"]
DB_PASS = os.environ["DBPASSWORD"]

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')

app = Flask(__name__)
cors = CORS(app)

db_pool = pool.SimpleConnectionPool(
    minconn=1,  # Minimum number of connections
    maxconn=10,  # Maximum number of connections
    database="mtc",
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)

@app.route("/", methods=['GET'])
@cross_origin()
def main():
    return Response('{"status":"Running"}', status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=False)