from flask import Flask, render_template, request, jsonify, make_response
import json
import requests
from rapidfuzz.distance import Levenshtein
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'
IMDB_API_BASEURL = "https://imdb-api.com/en/API"
IMDB_API_KEY = "k_6p68dybu"

with open('{}/databases/movies.json'.format("."), "r") as jsf:
    movies = json.load(jsf)["movies"]


# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>", 200)

# HTML template
@app.route("/template", methods=['GET'])
def template():
    return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'), 200)

# JSON retourne le json movies
@app.route("/json", methods=["GET"])
def get_json():
    return make_response(jsonify(movies), 200)

# JSON du movie récupéré avec l'id ou bien une erreur 400
@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie), 200)
            return res
    return make_response(jsonify({"error": "Movie ID not found"}), 400)

# JSON du movie récupéré avec le titre ou bien une erreur 400
@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                json = movie

    if not json:
        res = make_response(jsonify({"error": "movie title not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res

# JSON du movie récupéré avec la note ou bien une erreur 400
@app.route("/moviesbyrating", methods=["GET"])
def get_movie_by_rate():
    json = ""
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["rating"]) == str(req["rating"]):
                if not json:
                    json = [movie]
                else:
                    json.append(movie)
    if not json:
        res = make_response(jsonify({"error": "movie rating not found"}), 400)
    else:
        res = make_response(jsonify(json), 200)
    return res

# post d'un movie et vérification via l'id
@app.route("/movies/<movieId>", methods=['POST'])
def create_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error": "movie ID already exists"}), 409)

    movies.append(req)
    res = make_response(jsonify({"message": "movie added"}), 200)
    return res

# Put d'une note via le movie id (modicication)
@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = float(rate)
            res = make_response(jsonify(movie), 200)
            return res

    res = make_response(jsonify({"error": "movie ID not found"}), 201)
    return res

# delete un movie via le movie id
@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie), 200)

    res = make_response(jsonify({"error": "movie ID not found"}), 400)
    return res


# TP BLEU
# recupération des movie par date appelle d'api (showmovie)
@app.route("/movies/date/<date>", methods=['GET'])
def get_movie_date(date):
    res_movie = requests.get('http://localhost:3202/showmovies/' + date)
    movies_json = res_movie.json()['movies']
    movie_tab = {'movies': []}
    for movie in movies_json:
        for movie_in in movies:
            if str(movie) == str(movie_in["id"]):
                movie_tab['movies'].append(movie_in)

    res = make_response(jsonify(movie_tab), 200)
    return res

# get un movie par son nom (nom le plus proche méthode de Levenshtein)
@app.route("/movies/name/<title>", methods=['GET'])
def get_movie_name(title):
    film_proche = {'movies': []}
    for movie in movies:
        dist = Levenshtein.distance(str(movie["title"]).lower(), str(title).lower())
        film_proche['movies'].append({'movie': movie, 'dist': str(dist)})

    film_tri = []

    for f in film_proche['movies']:
        film_tri.append(f)
        i = False
        while not i:
            i = True
            for pointeur in range(len(film_tri)):
                if pointeur != len(film_tri) - 1 and int(film_tri[pointeur]['dist']) > int(
                        film_tri[pointeur + 1]['dist']):  # si je suis sup à celui d'apres
                    ret = film_tri[pointeur]  # je me stock
                    film_tri[pointeur] = film_tri[pointeur + 1]  # je met celui d'avant à ma place
                    film_tri[pointeur + 1] = ret  # je me remet arpes
                    i = False

    res = make_response(jsonify(film_tri[0]['movie']), 200)
    return res


# TP ROUGE
@app.route("/imdb/movie/<title>", methods=["GET"])
def get_movie_by_title(title):
    """
    By calling this route, user can find a list of movies that match the given title
    This route returns a list of movieItems
    """
    req = requests.get(f"{IMDB_API_BASEURL}/SearchMovie/{IMDB_API_KEY}/{title}")
    if req.status_code != 200:
        return make_response({"error": "something went wrong with IMDB API"}, 503)
    result = req.json()
    if result["errorMessage"] == "":
        return make_response(jsonify(result["results"]), 200)
    return make_response({"error": result["errorMessage"]})


@app.route("/imdb/trailer/<movieId>", methods=["GET"])
def get_movie_trailer(movieId):
    """
    By calling this route, user can find the trailer link of the film associated to the given id
    This route returns a json which contains the trailer's link {link: "thelink"}
    """
    req = requests.get(f"{IMDB_API_BASEURL}/Trailer/{IMDB_API_KEY}/{movieId}")
    if req.status_code != 200:
        return make_response({"error": "something went wrong with IMDB API"}, 503)
    result = req.json()
    if result["errorMessage"] == "":
        return make_response({"link": result["link"]}, 200)
    return make_response({"error": result["errorMessage"]})


if __name__ == "__main__":
    # p = sys.argv[1]
    print("Server running in port %s" % (PORT))
    app.run(host=HOST, port=PORT, debug=True)
