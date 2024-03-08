from Recomender import recomend_me

if __name__ == "__main__":
    query = "Crime movie with Leonardo DiCaprio"
    movie,movie_plot = recomend_me(query)
    response = f"I recomend you {movie[0]} \n here is the plot : \n {movie_plot[0]}"
    print(response)