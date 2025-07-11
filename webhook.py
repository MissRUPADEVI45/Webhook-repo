from flask import Flask, request, jsonify
from datetime import datetime
import pymongo
import os

# Create a Flask web application
app = Flask(__name__)

# MongoDB connection setup
MONGO_URI = "mongodb+srv://missrupadevi0450:RUPADEVI@45@cluster0.3874lmx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGO_URI)
db = client['github_events']              # Database name
collection = db['events']                 # Collection to store GitHub events

# Root route - simple status check
@app.route('/')
def home():
    return "Webhook server is running! Ready to receive GitHub events."

# Webhook route that listens to GitHub POST requests
@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json                                    # Get JSON data from the GitHub webhook
    event_type = request.headers.get('X-GitHub-Event')    # Identify an event type like push, pull_request from the GitHub header
  
    if not data:                           # If no data is received, return an error response
        return "⚠️ No data received", 400

    # Prepare a document to store in MongoDB
    event_doc = {
        "event_type": event_type,          # What kind of GitHub event was received
        "data": data,                      # The full payload sent by GitHub
        "received_at": datetime.utcnow()   # Timestamp when this webhook was received
    }

    # Save the event document into MongoDB
    collection.insert_one(event_doc)

    # Respond to GitHub with a success message
    return jsonify({"status": "success"}), 200
@app.route('/events')
def show_events():
    events = list(collection.find().sort("received_at", -1))
    return render_template("Assignment.html", events=events)   
#  Run the Flask app
if __name__ == '__main__':
    app.run(port=5000)  # Localhost port
