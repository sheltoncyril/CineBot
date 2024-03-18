from flask import Flask, request
from Recomender import recomend_me
from recomender_augmented import recommend_me_augmented

app = Flask(__name__)


# @app.route('/time')
# def get_current_time():
#     return {'time': time.time()}


@app.route("/query", methods=["POST"])
def send_query():
    query = request.get_json()["data"]["message"]

    movie1, _ = recomend_me(query)
    movie2 = recommend_me_augmented(query)
    return {"response": " ".join([movie1, movie2])}
