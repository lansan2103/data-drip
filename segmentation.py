import torch
import facer
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import timm.layers
import mediapipe as mp


'''
@inproceedings{zheng2022farl,
  title={General facial representation learning in a visual-linguistic manner},
  author={Zheng, Yinglin and Yang, Hao and Zhang, Ting and Bao, Jianmin and Chen, Dongdong and Huang, Yangyu and Yuan, Lu and Chen, Dong and Zeng, Ming and Wen, Fang},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={18697--18709},
  year={2022}
}

https://github.com/FacePerceiver/facer
'''

# function that computes the mean hsv values
def compute_hsv(mask, hsv_image):
    masked_pixels = hsv_image[mask]  # Extract only masked pixels
    mean_hsv = np.mean(masked_pixels, axis=0) if masked_pixels.size > 0 else [0, 0, 0]
    return mean_hsv


# Define device (GPU or CPU)
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Read image

image_path = 'haerin.jpg'  # Update with your image (ideally jpg)
image = facer.hwc2bchw(facer.read_hwc(image_path)).to(device=device)  # Convert to tensor

# Load face detector (RetinaFace)
face_detector = facer.face_detector('retinaface/mobilenet', device=device)

# Perform face detection
with torch.inference_mode():
    faces = face_detector(image)

# Load Face Parsing model (FARL)
face_parser = facer.face_parser('farl/lapa/448', device=device)  # You can try "farl/celebm/448" as well

# Perform face parsing
with torch.inference_mode():
    faces = face_parser(image, faces)

# Extract segmentation logits
seg_logits = faces['seg']['logits']
seg_probs = seg_logits.softmax(dim=1)  # n_faces x n_classes x h x w

# Get segmentation mask (argmax gives class index per pixel)
seg_mask = seg_probs.argmax(dim=1).squeeze().cpu().numpy()  # Convert to numpy array

# Load original image in OpenCV for HSV conversion
cv_image = cv2.imread(image_path)  # OpenCV loads images as BGR
cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)  # Convert to RGB
hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2HSV)  # Convert to HSV

# Just to show the segmentation 

def show_segmentation(mask, title="Segmentation Mask"):
    plt.figure(figsize=(6, 6))
    plt.imshow(mask, cmap='jet')  # 'jet' colormap makes it easier to see regions
    plt.colorbar(label="Class Index")
    plt.title(title)
    plt.axis("off")
    plt.show()

# Show the segmentation mask
# show_segmentation(seg_mask)

# Creating a mapping of the features 

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

# filter by mapping
skin_mask = (seg_mask == features["skin"])
eye_mask = np.isin(seg_mask,features["eyes"])
hair_mask = (seg_mask == features["hair"])

# compute hsvs of each (these are numpy arrays)

skin_hsv = compute_hsv(skin_mask, hsv_image)
eye_hsv = compute_hsv(eye_mask, hsv_image)
hair_hsv = compute_hsv(hair_mask, hsv_image)

data = {
    "skin": skin_hsv.tolist(),
    "eyes": eye_hsv.tolist(),
    "hair": hair_hsv.tolist()
}

with open("hsv_data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)


# convert from hsv to korean season palette

def get_season(h, s, v):
    # h = Hue in degrees (0 - 360)
    # s = Saturation in % (0 - 100)
    # v = Value/Brightness in % (0 - 100)

    if 20 <= h <= 40 and s > 40 and v > 70:
        return "Spring"
    elif 10 <= h <= 30 and s < 40 and v > 60:
        return "Summer"
    elif 30 <= h <= 50 and s > 30 and v < 70:
        return "Autumn"
    elif 10 <= h <= 25 and s > 50 and v < 50:
        return "Winter"
    else:
        return "Neutral / Depends — Try Soft Tones"

def get_palette(season):
    palettes = {
        "Spring": ["#FFA07A", "#FFD700", "#98FB98", "#FFB6C1"],  # Coral, Yellow, Mint, Pink
        "Summer": ["#C8A2C8", "#F4A7B9", "#87CEEB", "#D3D3D3"],  # Lavender, Dusty Rose, Sky Blue, Light Grey
        "Autumn": ["#556B2F", "#D2691E", "#FF8C00", "#8B4513"],  # Olive, Rust, Mustard, Brown
        "Winter": ["#800020", "#003366", "#228B22", "#2F4F4F"],  # Burgundy, Navy, Emerald, Charcoal
        "Neutral / Depends — Try Soft Tones": ["#000000", "#FFFFFF", "#4B4B4B", "#D3D3D3"]
    }
    return palettes.get(season)

h, s, v = skin_hsv

season = get_season(h, s, v)
palette = get_palette(season)

print(f"Detected Season: {season}")
print(f"Recommended Color Palette: {palette}")

def display_palette(palette, season):
    n = len(palette)
    fig, ax = plt.subplots(figsize=(n * 2, 2))

    for i, color in enumerate(palette):
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))

    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.title(f'{season} Palette', fontsize=16)
    plt.show()

display_palette(palette, season)



