from flask import Flask, request, jsonify
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

candidate_labels = ['venting','suggestion','advice']



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



    toxicity = Detoxify('unbiased').predict(post_content)


    first_element_score = list(toxicity.values())[0] #get the most score 
    first_element_name = list(toxicity.keys())[0] #get the most score 

    if first_element_score > 0.80:
        return_str = 'Cant post because of ' + first_element_name
        return jsonify(return_str)

    else:
        emotion = emotion_classifier(post_content)
        topics = classifier(post_content, candidate_labels)
        if (topics['labels'][0] == 'suggestion' or topics['labels'][0] == 'advice'):
            try:
                highest_score_particular_user = db.students.find_one(filter={"username": username}, sort=[("healer_score", pymongo.DESCENDING)])["score"]
                healer_score = highest_score_particular_user
                healer_score = healer_score + 1 
            except:
                healer_score = 4
            
        post = {'username':username,'post_content':post_content, 'like_count':0, 'healer_score':healer_score, 'emotion':emotion[0]['label'],'topics':topics['labels'][0] }
        # Insert the data into the collection
        result = collection.insert_one(post)
        return jsonify('Vent posted')

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
    comment_like_up = data['comment_like_up']

    if comment_up:
        comment_username = data['comment_username']
        comment_content = data['comment_content']


    result_for_username = collection.find_one(filter={"_id": ObjectId(id)})
    
    username_for_id = result_for_username["username"]

    result_for_username = collection.find_one(filter={"username": username_for_id})

    like_count = result_for_username["like_count"]

    highest_score_particular_user = collection.find_one(filter={"username": username_for_id}, sort=[("healer_score", pymongo.DESCENDING)])["healer_score"]
    healer_score = highest_score_particular_user


    if (str(like_up) == '1' and result_for_username["topics"] == 'suggestion'):
        like_count = int(like_count) + 1
        like_username = data['like_username']
        healer_score = healer_score + 4
    else:
        pass

    if str(comment_up) == '1':
        comment_username = data['comment_username']
        comment_content = data['comment_content']
    else:
        pass

    if str(comment_like_up) == '1':
        try:
            comment_like_up = int(result_for_username['comment_like_up']) + 1
            healer_score = healer_score + 4
        except:
            comment_like_up = 1
    else:
        pass



    filter = {'_id': ObjectId(id)}

    

    # define the update to apply to the document
    update = {'$set': 
    {
        'like_count': like_count, 
        'like_username':like_username,
        'comment_username':comment_username,
        'comment_content':comment_content,
        'healer_score' : healer_score,
        'comment_like_up':comment_like_up
        }
    }


    # call the update_one() method to update the document
    result = collection.update_one(filter, update)
    print(result.matched_count)
    return jsonify(result.modified_count)


@app.route('/healer-score', methods=['GET'])
def healer():

    username = request.args.get('username')
    highest_score_particular_user = collection.find_one(filter={"username": username}, sort=[("healer_score", pymongo.DESCENDING)])["healer_score"]
    healer_score = highest_score_particular_user

    return jsonify(healer_score)

@app.route('/leaderboard', methods=['GET'])
def leaderboard():

    max_score_dict_list = []
    distinct_usernames = collection.distinct("username")
    for username in distinct_usernames:
        max_score = collection.find_one(filter={"username": username}, sort=[("healer_score", pymongo.DESCENDING)])["healer_score"]
        max_score_dict = {username:max_score}
        max_score_dict_list.append(max_score_dict) 
    

    sorted_list = sorted(max_score_dict_list, key=lambda x: list(x.values())[0], reverse=True)
    return jsonify(sorted_list)


if __name__ == '__main__':
    app.run(debug=True)