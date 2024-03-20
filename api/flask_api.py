from flask import Flask, request
from services import service_registry

# from services.Recomender import recomend_me

app = Flask(__name__)


# @app.route('/time')
# def get_current_time():
#     return {'time': time.time()}

service_registry.init()


@app.route("/query", methods=["POST"])
def send_query():
    query = request.get_json()["data"]["message"]
    suggestions = list()
    # movie1, _ = recomend_me(query)
    # suggestions.extend(movie1)
    movie2 = service_registry.get_service("similarity_recommender_service").recommend(query)
    suggestions.extend(movie2)
    return {"response": ", ".join(suggestions)}
