from flask import Flask, jsonify, request
import json
app = Flask(__name__)
data_store = {
    1: {"name": "John Doe", "age": 30, "city": "New York"},
    2: {"name": "Jane Smith", "age": 25, "city": "Los Angeles"}
}

@app.route('/api/helloWorld', methods=['GET'])
def hello_world():
    return "Hello, World!"
@app.route('/api/json', methods=['GET'])
def get_json():
    try:
        with open('ex5.json', 'r') as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
@app.route('/api/data/<int:item_id>', methods=['GET'])
def fetch_by_id(item_id):
    item = data_store.get(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/api/data/<int:item_id>', methods=['DELETE'])
def delete_by_id(item_id):
    """Delete item by ID."""
    if item_id in data_store:
        del data_store[item_id]
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/api/data/<int:item_id>', methods=['PUT'])
def update_by_id(item_id):
    """Update item by ID."""
    if item_id in data_store:
        data = request.json
        data_store[item_id].update(data)
        return jsonify({"message": "Item updated successfully", "data": data_store[item_id]})
    else:
        return jsonify({"error": "Item not found"}), 404
@app.route('/api/data', methods=['POST'])
def create_entry():
    """Create a new entry."""
    new_id = max(data_store.keys()) + 1 if data_store else 1
    data = request.json
    data_store[new_id] = data
    return jsonify({"message": "Item created successfully", "id": new_id, "data": data}), 201

if __name__ == '__main__':
    app.run(debug=True,port=5001)
