from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
import json
from bson.json_util import dumps
from bson.objectid import ObjectId


from transformers import pipeline
from detoxify import Detoxify

classifier = pipeline("zero-shot-classification",
                      model="valhalla/distilbart-mnli-12-1")
emotion_classifier = pipeline('sentiment-analysis', 
                    model='joeddav/distilbert-base-uncased-go-emotions-student')

candidate_labels = ['venting', 'suggestion', 'self harm','advice']



app = Flask(__name__)
CORS(app)
connection_string = "mongodb+srv://rajat10cube:2XOj760AEsxnWmcW@cluster0.ooyfroj.mongodb.net/?retryWrites=true&w=majority"
db_name = "vents"
collection_name1 = "01"
collection_name2 = "02"

try:
# Connect to the MongoDB cluster using the connection string
    client = pymongo.MongoClient(connection_string)
    print("client",client.server_info())
except:
    print("connection error")
# Get the specified database and collection
db = client[db_name]
collection1 = db[collection_name1]
collection2 = db[collection_name2]

@app.route('/register', methods=['POST'])
def register():
    print("called register")
    print("request.json",request.json)
    data = request.json
    print("data",data)
    username = data['username']
    password = data['password']
    post = {'username':username,'password':password}
    collection1.insert_one(post)
    print("registeration done")
    return jsonify('registered')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    cursor = collection1.find({ 'username': username, 'password':password })
    print(list(cursor))
    documents = list(cursor)
    return jsonify(json.loads(dumps(documents)))


@app.route('/vents', methods=['POST'])
def posting_vents():
    data = request.json
    username = data['username']
    post_content = data['post_content']
   # time = data['time']

    print(username,post_content)
    toxicity = Detoxify('unbiased').predict(post_content)


    first_element_score = list(toxicity.values())[0] #get the most score 
    first_element_name = list(toxicity.keys())[0] #get the most score 

    if first_element_score > 0.80:
        return_str = 'Cant post because of ' + first_element_name
        return jsonify(return_str)

    else:
        emotion = emotion_classifier(post_content)
        topics = classifier(post_content, candidate_labels)
        post = {'username':username,'post_content':post_content, 'emotion':emotion[0]['label'],'topics':topics['labels'][0] }
        # Insert the data into the collection
        result = collection2.insert_one(post)
        return jsonify('Vent posted')

@app.route('/vents', methods=['GET'])
def getting_vents():

    # Use the find method to query the collection
    cursor = collection2.find()
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
    result = collection2.update_one(filter, update)
    print(result.matched_count)
    return jsonify(result.modified_count)

if __name__ == '__main__':
    app.run(debug=True)

