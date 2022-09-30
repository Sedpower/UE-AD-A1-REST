from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"


@app.route("/user/booking/<userid>", methods=['GET'])
def get_movie_by_userid(userid):

   dates = requests.get('http://172.16.124.165:3201/bookings/'+userid)
   if (str(dates) == '<Response [400]>'):
      return make_response(jsonify({"error": "bad input parameter"}), 400)
   dates = dates.json()
   movie_tab = {'movies':[]}

   for date in dates['dates']:
      for movie in date["movies"]:
         res_movie = requests.get('http://172.16.124.165:3200/movies/'+movie)
         movie_tab['movies'].append(res_movie.json())

   res = make_response(jsonify(movie_tab), 200)

   return res


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
