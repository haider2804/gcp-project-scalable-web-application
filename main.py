import functions_framework
from google.cloud import storage
import os
import json
from flask import jsonify, request

# Initialize the Google Cloud Storage client
storage_client = storage.Client()
bucket_name = "myproject-static-website-007"  # replace with your bucket name

@functions_framework.http
def handle_file(request):
    """HTTP Cloud Function to upload or retrieve files in Cloud Storage."""
    
    # Check if this is an upload request with a file
    if request.method == "POST" and request.files.get("file"):
        file = request.files["file"]
        blob = storage_client.bucket(bucket_name).blob(file.filename)
        blob.upload_from_file(file)
        
        return f"File {file.filename} uploaded to {bucket_name}.", 200
    
    # Retrieve a file if a filename is provided in query
    elif request.method == "GET":
        filename = request.args.get("filename")
        
        if not filename:
            return jsonify({"error": "No filename specified"}), 400
        
        blob = storage_client.bucket(bucket_name).blob(filename)
        
        if not blob.exists():
            return jsonify({"error": "File not found"}), 404
        
        file_contents = blob.download_as_text()
        return file_contents, 200
    
    # If the request is neither a valid POST nor GET, return an error
    return jsonify({"error": "Invalid request"}), 400
