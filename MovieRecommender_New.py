from flask import Flask, render_template, request
# from model.recommender import MovieRecommender
# import os
app = Flask(__name__)

# recommender = MovieRecommender(
#     "data/tmdb_5000_movies.csv",
#     "data/tmdb_5000_credits.csv"
# )

@app.route("/", methods=["GET", "POST"])
def home():
    return "Movie Recommender System is under construction."
    # recommendations = []
    # error = None

    # if request.method == "POST":
    #     movie = request.form.get("movie")
    #     print("User typed:", movie)  # debug line

    #     recommendations = recommender.recommend(movie)

    #     if not recommendations:
    #         error = "Movie not found in dataset. Please try another title."

    # return render_template(
    #     "index.html",
    #     recommendations=recommendations,
    #     error=error
    # )

if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 5000))
    app.run()
