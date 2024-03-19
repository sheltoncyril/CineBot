from prompting import *
from Recomender import recomend_me

from api.services.recomender_augmented import recommend_me_augmented

if __name__ == "__main__":
    query = "Adventure and Comedy with Leonardo Di Caprio"  # input('what do you want to watch')
    movie, movie_plot = recomend_me(query)
    movie2 = recommend_me_augmented(query)
    print(movie2[0], movie[0])
    # context = [ {'role':'system', 'content':"""You are CineBot. """} ]
    # res = collect_user_queries(query, movie[0], context)
    # formatted_response = format_ai_response(res)
    # print(formatted_response)    #print(formatted_response)
