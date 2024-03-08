from Recomender import recomend_me
from prompting import *

if __name__ == "__main__":
    query = input('what do you want to watch')
    movie,movie_plot = recomend_me(query)
    print(movie[0])
    context = [ {'role':'system', 'content':"""You are CineBot. """} ]
    res = collect_user_queries(query, movie[0], context)
    formatted_response = format_ai_response(res)
    print(formatted_response)