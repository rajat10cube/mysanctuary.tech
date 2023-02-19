from flask import Flask, request, jsonify
import pymongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

connection_string = "mongodb+srv://arpanqx:arpan77@cluster0.iqoj2fz.mongodb.net/?retryWrites=true&w=majority"
db_name = "vents"
collection_name = "01"

# Connect to the MongoDB cluster using the connection string
client = pymongo.MongoClient(connection_string)

# Get the specified database and collection
db = client[db_name]
collection = db[collection_name]

@app.route('/vents', methods=['POST'])
def posting_vents():
    data = request.json
    username = data['username']
    post_content = data['post_content']
   # time = data['time']

    # Insert the data into the collection
    result = collection.insert_one(data)
    print(result)
    return jsonify(1)

@app.route('/vents', methods=['GET'])
def getting_vents():

    # Use the find method to query the collection
    cursor = collection.find()
    
    # Convert the cursor to a list of documents
    documents = list(cursor)


    return jsonify(json.loads(dumps(documents)))

@app.route('/vents', methods=['PUT'])
def updating_vents():
    like_count = ''
    like_username = ''
    comment_username = ''
    comment_content = ''

    data = request.json

    id = data['id']

    like_up = data['like_up']
    comment_up = data['comment_up']


    comment_username = data['comment_username']
    comment_content = data['comment_content']


    if str(like_up) == '1':
        like_count = int(like_count) + 1
        like_count = data['like_count'] # only 1 
        like_username = data['like_username']
    else:
        pass

    if str(comment_up) == '1':
        comment_username = data['comment_username']
        comment_content = data['comment_content']
    else:
        pass


    filter = {'_id': ObjectId(id)}

    

    # define the update to apply to the document
    update = {'$set': 
    {
        'like_count': like_count, 
        'like_username':like_username,
        'comment_username':comment_username,
        'comment_content':comment_content
        }
    }


    # call the update_one() method to update the document
    result = collection.update_one(filter, update)
    print(result.matched_count)
    return jsonify(result.modified_count)

if __name__ == '__main__':
    app.run(debug=True)
