
class WebServer:
    def __init__(self, app):
        self.app = app
        self.setup_routes()
    
    
    def add_event_processor(self, event_processor):
        self.jenkins= event_processor
        

    def setup_routes(self):
        @self.app.get("/predict")
        async def predict(x: float):
            y = x*4
            return {"result": y}
            
            
        # @self.app.post('/pr')
        # def receive_json():
        #     data = request.get_json()
        #     if not data:
        #         return jsonify({"error": "No JSON data provided"}), 400
            
        #     # Process the JSON data here
        #     data = self.jenkins.event_received(data)
        #     return jsonify({"message": "JSON data received", "data": data}), 200

        # @self.app.route('/pr/file', methods=['POST'])
        # def receive_file():
        #     if 'file' not in request.files:
        #         return jsonify({"error": "No file part in the request"}), 400
        #     file = request.files['file']
        #     if file.filename == '':
        #         return jsonify({"error": "No selected file"}), 400
        #     # Save the file or process it here
        #     file.save(f"./{file.filename}")
        #     return jsonify({"message": "File received", "filename": file.filename}), 200
