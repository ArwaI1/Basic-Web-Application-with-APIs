from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulated data storage for submitted forms
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    if not name or not email or not message:
        error = "All fields are required!"
        return render_template('index.html', error=error)

    # Save message in the simulated data storage
    new_message = {
        'id': len(messages) + 1,
        'name': name,
        'email': email,
        'message': message
    }
    messages.append(new_message)

    return render_template('result.html', name=name, email=email, message=message)

# API: Get all messages
@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

# API: Get a message by ID
@app.route('/api/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    for message in messages:
        if message['id'] == message_id:
            return jsonify(message)
    return jsonify({"error": "Message not found"}), 404

# API: Add a new message via POST
@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.json
    if 'name' not in data or 'email' not in data or 'message' not in data:
        return jsonify({"error": "All fields (name, email, message) are required!"}), 400

    new_message = {
        'id': len(messages) + 1,
        'name': data['name'],
        'email': data['email'],
        'message': data['message']
    }
    messages.append(new_message)
    return jsonify(new_message), 201

# API: Update an existing message
@app.route('/api/messages/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    data = request.json
    for message in messages:
        if message['id'] == message_id:
            message['name'] = data.get('name', message['name'])
            message['email'] = data.get('email', message['email'])
            message['message'] = data.get('message', message['message'])
            return jsonify(message)
    return jsonify({"error": "Message not found"}), 404

# API: Delete a message
@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    for message in messages:
        if message['id'] == message_id:
            messages.remove(message)
            return jsonify({"message": "Message deleted"})
    return jsonify({"error": "Message not found"}), 404

if __name__ == '__main__':
    app.run(debug=False, port=3000)
