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


@app.route("/user/booking/<userId>/<date>", methods=["GET"])
def get_user_booking_bydate(userId, date):
    r = requests.get(f"http://localhost:3201/bookings/{str(userId)}")
    if r.status_code != 200:
        return make_response({"error": "bad input parameter"})
    result = r.json()
    for dateItem in result["dates"]:
        if str(dateItem["date"]) == str(date):
            return make_response(dateItem, 200)
    return make_response({"error": "not found"}, 404)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
