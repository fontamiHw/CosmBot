from flask import Flask, jsonify, request


class WebServer:
    def __init__(self, event_processor, host='0.0.0.0', port=5000):
        self.jenkins= event_processor
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/pr', methods=['POST'])
        def receive_json():
            data = request.get_json()
            if not data:
                return jsonify({"error": "No JSON data provided"}), 400
            
            # Process the JSON data here
            data = self.jenkins.event_received(data)
            return jsonify({"message": "JSON data received", "data": data}), 200

        @self.app.route('/pr/file', methods=['POST'])
        def receive_file():
            if 'file' not in request.files:
                return jsonify({"error": "No file part in the request"}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            # Save the file or process it here
            file.save(f"./{file.filename}")
            return jsonify({"message": "File received", "filename": file.filename}), 200

    def start(self):
        self.app.run(host=self.host, port=self.port)
