from flask import Flask, jsonify
import sqlite3
import os
import json
from flask_cors import CORS, cross_origin

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# app = CORS(app)


def get_db_connection():
    conn = sqlite3.connect('football.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
@app.route('/<string:league>')
@cross_origin()
def home(league='epl'):
    default_error_return = {'league_name': league.upper(), 'data': []}
    league_list = ['epl', 'ligue-1', 'bundesliga', 'serie-a', 'laliga']
    conn = get_db_connection()
    league_standing_list = ''

    if league.lower() not in league_list:
        return default_error_return
    else:
        league = league.lower()

    d_a_t_a = conn.execute(
        "SELECT * FROM table_standings WHERE LOWER(league_name) = '{}';".format(
            league)
    ).fetchall()

    conn.close()
    if d_a_t_a:
        for i in d_a_t_a:
            league_standing_list = json.loads(str(i[2]))
        return json.loads(league_standing_list)
    else:
        return default_error_return


if __name__ == "__main__":
    app.run(debug=True)
