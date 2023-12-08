# app/routes/predict_routes.py
from flask import Blueprint, request, jsonify
import torch

from ultralytics import YOLO

predict_bp = Blueprint("predict", __name__)
model = YOLO('https://storage.cloud.google.com/sehatin-ml-model/best.pt')


@predict_bp.route("/predict", methods=["POST"])
def predict():
    if "url" in request.json:
        # Decode base64 to image
        photo_base64 = request.json["url"]
        # photo_decoded = base64.b64decode(photo_base64)
        # img = Image.open(BytesIO(photo_decoded))

        # Perform inference
        with torch.no_grad():
            output = model.predict(photo_base64, conf=0.3, imgsz=720)
            names = model.names

        # Process the output as needed
        detected_objects = {}

        for r in output:
            for c in r.boxes.cls:
                class_name = names[int(c)]
                detected_objects[class_name] = detected_objects.get(class_name, 0) + 1

        # Convert the detected_objects dictionary to the desired format
        formatted_detected_objects = [{"food_name": key, "count": value} for key, value in detected_objects.items()]

        return jsonify({"detected_objects": formatted_detected_objects, })

    return jsonify({"error": "No photo_base64 provided"}), 400
