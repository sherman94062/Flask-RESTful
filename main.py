
from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
api = Api(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Flask-RESTful"]  # Replace with your actual MongoDB database name
collection = db["documents"]  # Replace with your actual MongoDB collection name


class DocumentResource(Resource):
    def get(self, document_id):
        try:
            document = collection.find_one({"_id": ObjectId(document_id)})
            if document:
                return document
            else:
                return {"message": "Document not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def put(self, document_id):
        try:
            data = request.get_json()
            result = collection.update_one({"_id": ObjectId(document_id)}, {"$set": data})
            if result.modified_count > 0:
                return {"message": "Document updated successfully"}
            else:
                return {"message": "Document not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, document_id):
        try:
            result = collection.delete_one({"_id": ObjectId(document_id)})
            if result.deleted_count > 0:
                return {"message": "Document deleted successfully"}
            else:
                return {"message": "Document not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500


class DocumentListResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            document_id = collection.insert_one(data).inserted_id
            return {"message": "Document created successfully", "document_id": str(document_id)}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def get(self):
        try:
            documents = list(collection.find())
            return documents
        except Exception as e:
            return {"error": str(e)}, 500


api.add_resource(DocumentListResource, '/api/documents')
api.add_resource(DocumentResource, '/api/documents/<string:document_id>')


if __name__ == '__main__':
    app.run(debug=True)
