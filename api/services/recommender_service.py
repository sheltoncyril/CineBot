from Recomender import recomend_me
from recomender_augmented import recommend_me_augmented


def get_response_for_query(query):
    movie, movie_plot = recomend_me(query)
    movie2 = recommend_me_augmented(query)
    print(movie2[0], movie[0])
    return
