# UE-AD-A1-REST

ce que vous avez fait dans le TP (vert/bleu/rouge) et quelques explications

TP vert :

1-4 fait.

5 : 

recupérer les movies via user is et date (appelle api bookings)
@app.route("/user/booking/<userId>/<date>", methods=["GET"])

récupérer les movies par date via user id (appelle api bookings + movies)
@app.route("/user/booking/<userid>", methods=['GET'])

++ YAML

TP bleu :

movie.py

recupération des movies par date appelle d'api (showmovie)
@app.route("/movies/date/<date>", methods=['GET'])

get un movie par son nom (nom le plus proche méthode de Levenshtein)
@app.route("/movies/name/<q>", methods=['GET'])


TP rouge :

movie.py

retourne une list de movie via un titr

@app.route("/imdb/movie/<title>", methods=["GET"])

retourne le lien du trailer d'un movie via movieId

@app.route("/imdb/trailer/<movieId>", methods=["GET"])


instructions pour lancer nos codes avec Docker Compose

nous n'avons pas utilisé docker.

instructions pour lancer nos codes avec PyCharm

run les quatres fichiers .py movie,user,booking,showtime

