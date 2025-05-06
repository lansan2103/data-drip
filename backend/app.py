from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import torch
import facer
import cv2
import numpy as np
import pandas as pd
import random

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load models and data once when the server starts
device = 'cuda' if torch.cuda.is_available() else 'cpu'
face_detector = facer.face_detector('retinaface/mobilenet', device=device)
face_parser = facer.face_parser('farl/lapa/448', device=device)
# catalog = pd.read_csv('data/cleaned_handm.csv')

# Seasonal palettes from palettechart.py
seasonal_palettes_hex = {
    "Spring": [
        ("Bright yellow", "#FFEA00"), ("Gold yellow", "#FFD700"), ("Pastel yellow", "#FFFF99"),
        ("Yellow gold", "#FADA5E"), ("Baby pink", "#FFC0CB"), ("Light pink", "#FFB6C1"),
        ("Salmon", "#FA8072"), ("Coral", "#FF7F50"), ("Light blue", "#ADD8E6"),
        ("Sky blue", "#87CEEB"), ("Light green", "#90EE90"), ("Mint", "#98FF98"),
        ("Peach", "#FFE5B4"), ("Amber", "#FFBF00"), ("Lemon", "#FFF44F")
    ],
    "Summer": [
        ("Cobalt blue", "#0047AB"), ("Indigo", "#4B0082"), ("Blue gray", "#6699CC"),
        ("Gray white", "#D3D3D3"), ("Ivory", "#FFFFF0"), ("Ecru", "#C2B280"),
        ("Stone", "#837060"), ("Dusty pink", "#DCAE96"), ("Rose", "#FF007F"),
        ("Mauve", "#E0B0FF"), ("Light purple", "#CBC3E3"), ("Lilac", "#C8A2C8"),
        ("Pastel purple", "#B39EB5"), ("Pastel blue", "#AEC6CF"), ("Pastel green", "#77DD77"),
        ("Pastel pink", "#FFD1DC"), ("Dusty rose", "#C08081"), ("Light red", "#FF6961")
    ],
    "Autumn": [
        ("Charcoal", "#36454F"), ("Mahogany", "#C04000"), ("Rust", "#B7410E"),
        ("Cream", "#FFFDD0"), ("Taupe", "#483C32"), ("Wheat", "#F5DEB3"),
        ("Mustard", "#FFDB58"), ("Khaki green", "#78866B"), ("Olive", "#808000"),
        ("Terracotta", "#E2725B"), ("Dark maroon", "#800000"), ("Dark red", "#8B0000"),
        ("Burnt orange", "#CC5500"), ("Copper", "#B87333"), ("Dark green", "#006400"),
        ("Sea green", "#2E8B57"), ("Dark gray", "#A9A9A9"), ("Gray silver", "#C0C0C0"),
        ("Amber", "#FFBF00"), ("Gold yellow", "#FFD700"), ("Ecru", "#C2B280")
    ],
    "Winter": [
        ("Bright blue", "#0096FF"), ("Dark blue", "#00008B"), ("Navy blue", "#000080"),
        ("Royal blue", "#4169E1"), ("White gray", "#F5F5F5"), ("Gray white", "#D3D3D3"),
        ("Bright pink", "#FF007F"), ("Neon pink", "#FF6EC7"), ("Hot pink", "#FF69B4"),
        ("Fuchsia", "#FF00FF"), ("Dark purple", "#301934"), ("Violet", "#8F00FF"),
        ("Bright red", "#FF0000"), ("Ruby red", "#9B111E"), ("Magenta", "#FF00FF"),
        ("Cyan", "#00FFFF"), ("Aquamarine", "#7FFFD4"), ("Emerald green", "#50C878"),
        ("Teal", "#008080"), ("Neon green", "#39FF14"), ("Plum", "#8E4585"), ("Maroon", "#800000")
    ]
}

# Create hex_to_color mapping
hex_to_color = {}
for season_colors in seasonal_palettes_hex.values():
    for color_name, hex_value in season_colors:
        hex_to_color[hex_value] = color_name

features = {
    "skin": 1,
    "eyebrows": [2, 3],
    "eyes": [4, 5],
    "nose": 6,
    "upper lip": 7,
    "lower lip": 8,
    "inner mouth": 9,
    "hair": 10,
    "ears": 11
}

def compute_hsv(mask, hsv_image):
    masked_pixels = hsv_image[mask]
    mean_hsv = np.mean(masked_pixels, axis=0) if masked_pixels.size > 0 else [0, 0, 0]
    return mean_hsv

def get_season(h, s, v):
    # return "h: ", h, " s: ", s, " v: ", v
    spring = 0
    summer = 0
    autumn = 0
    winter = 0
    # if 20 <= h <= 40 and s > 40 and v > 70:
    #     return "Spring"
    # elif 10 <= h <= 30 and s < 40 and v > 60:
    #     return "Summer"
    # elif 30 <= h <= 50 and s > 30 and v < 70:
    #     return "Autumn"
    # elif 10 <= h <= 25 and s > 50 and v < 50:
    #     return "Winter"
    # Points for h value
    if 14 <= h <= 31:
        spring += 1
    if 0 <= h <= 17:
        summer += 1
    if 21 <= h <= 42:
        autumn += 1
    if 0 <= h <= 10 or 198 <= h <= 255:
        winter += 1
    # Points for s value
    if 40 <= s <= 80:
        spring += 1
    if 10 <= s <= 40:
        summer += 1
    if 20 <= s <= 60:
        autumn += 1
    if 30 <= s <= 100:
        winter += 1
    # Points for v value
    if 65 <= v <= 100:
        spring += 1
    if 60 <= v <= 90:
        summer += 1
    if 30 <= v <= 75:
        autumn += 1
    if 15 <= v <= 75:
        winter += 1
    seasons = {'spring': spring,
               'summer': summer,
               'autumn': autumn,
               'winter': winter}
    max_value = spring
    max_key = 'spring'
    for key, value in seasons.items():
        if value > max_value:
            max_value = value
            max_key = key
    return max_key
    

def get_palette(season):
    return seasonal_palettes_hex.get(season, [])

@app.route('/test', methods=['GET'])
def test():
    return 'test', 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        image = facer.hwc2bchw(facer.read_hwc(filepath)).to(device=device)
        with torch.inference_mode():
            faces = face_detector(image)
            faces = face_parser(image, faces)

        seg_logits = faces['seg']['logits']
        seg_probs = seg_logits.softmax(dim=1)
        seg_mask = seg_probs.argmax(dim=1)[0].cpu().numpy()

        cv_image = cv2.imread(filepath)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)

        skin_mask = (seg_mask == features["skin"])
        skin_hsv = compute_hsv(skin_mask, hsv_image)

        h, s, v = skin_hsv

        # 💥 ADD THIS: if no good skin found, default
        if h == 0 and s == 0 and v == 0:
            return jsonify({
                "season": "Neutral",
                "palette": [
                    ["Gray", "#D3D3D3"],
                    ["Ivory", "#FFFFF0"],
                    ["Stone", "#837060"],
                    ["Dusty pink", "#DCAE96"],
                    ["Light blue", "#ADD8E6"]
                ]
            })

        season = get_season(h, s, v)
        palette = get_palette(season)

        return jsonify({
            "season": season,
            "palette": palette
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)