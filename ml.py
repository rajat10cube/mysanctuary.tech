from flask import Flask, request, jsonify
from transformers import pipeline
from detoxify import Detoxify

classifier = pipeline("zero-shot-classification",
                      model="valhalla/distilbart-mnli-12-1")
emotion_classifier = pipeline('sentiment-analysis', 
                    model='joeddav/distilbert-base-uncased-go-emotions-student')

candidate_labels = ['venting', 'suggestion', 'self harm','advice']

app = Flask(__name__)



@app.route('/mlmodels')
def topics():

    query = request.args.get('query', type = str)

    emotion = emotion_classifier(query)
    topics = classifier(query, candidate_labels)
    toxicity = Detoxify('unbiased').predict(query)
    
    return jsonify({'topics':topics,
    'emotion':emotion,
    'toxicity':str(toxicity)})

if __name__ == '__main__':
    app.run(debug=True)
