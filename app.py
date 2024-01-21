import bson
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

# access your MongoDB Atlas cluster
load_dotenv()
connection_string: str = os.environ.get('CONNECTION_STRING')
mongo_client: MongoClient = MongoClient(connection_string)

# add in your database and collection from Atlas 
database: Database = mongo_client.get_database('TeslaData')
collection: Collection = database.get_collection('battery')

# book = {'VIN': '111111111', 'SOC': 99.9}
# collection.insert_one(book)

# instantiating new object with “name”
app: Flask = Flask(__name__)
# # our initial form page 
# @app.route("/") 
# def index():
#     return 'Hi!'

# # our initial form page
@app.route('/')
def index():
	return render_template('index.html')

# CREATE and READ 
@app.route('/battery', methods=["GET", "POST"])
def battery():
    if request.method == 'POST':
        # CREATE
        vin: str = request.json['VIN']
        soc: float = request.json['SOC']

        # insert new book into books collection in MongoDB
        collection.insert_one({"VIN": vin, "SOC": soc})

        return f"CREATE: Your car {vin} ({soc} soc) has been added to your battery.\n "

    elif request.method == 'GET':
        # READ
        batteydata = list(collection.find())
        new_state = []

        for states in batteydata:
            vin = states['VIN']
            soc = states['SOC']
            battery_state = {'VIN': vin, 'SOC': soc}
            new_state.insert(0,battery_state)

        return new_state
    
# UPDATE
@app.route("/battery/<string:state_id>", methods = ['PUT'])
def update_battery(state_id: str):
    new_vin: str = request.json['VIN']
    new_soc: float = request.json['SOC']
    collection.update_one({"_id": bson.ObjectId(state_id)}, {"$set": {"VIN": new_vin, "SOC": new_soc}})

    return f"UPDATE: Your state has been updated to: {new_vin} ({new_soc} SOC).\n"


# DELETE
@app.route("/battery/<string:state_id>", methods = ['DELETE'])
def remove_battery(state_id: str):
    collection.delete_one({"_id": bson.ObjectId(state_id)})

    return f"DELETE: Your book (id = {state_id}) has been removed from your battery.\n"