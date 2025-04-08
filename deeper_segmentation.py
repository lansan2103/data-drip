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

# creating function to detect and draw facial landmarks using Mediapipe

def draw_facial_landmarks(image):
    """
    Draws facial landmark on original image
    """
    # Initializing Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode = True,
                                      max_num_faces = 1,
                                      min_detection_confidence = 0.5)

    # Processes image to get facial landmarks
    results = face_mesh.process(image)

    # check if faces are detected
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                cv2.circle(image, (x, y), 1, (0, 255, 0), -1) # draws green circles at landmarks

    return image

def draw_skin_landmarks(image):
    """
    Draws facial landmark on original image, specifically for skin

    - Forehead
    - Jawline
    - Right Cheek
    - Left Cheek

    https://storage.googleapis.com/mediapipe-assets/documentation/mediapipe_face_landmark_fullsize.png

    used this as a reference for the facial landmark areas

    """
    # Initializing Face Mesh
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode = True,
                                      max_num_faces = 1,
                                      min_detection_confidence = 0.5)

    # Processes image to get facial landmarks
    results = face_mesh.process(image)

    # forehead indices
    forehead_indices = [109, 108, 151, 337, 338, 10]

    # jawline indices
    jawline_indices = [208, 199, 428, 171, 396, 148, 152, 377]

    # right cheek indices
    right_cheek_indices = [266, 330, 280, 425, 266]
    # left cheek indices
    left_cheek_indices = [118, 101, 36, 205, 50]


    # check if faces are detected
    if results.multi_face_landmarks:
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # convert to hsv

        landmarks = results.multi_face_landmarks[0].landmark
        # Extract (x, y) coordinates of the forehead region from the landmark points
        forehead_points = np.array([(int(landmarks[i].x * image.shape[1]), 
                             int(landmarks[i].y * image.shape[0])) for i in forehead_indices])
        jawline_points = np.array([(int(landmarks[i].x * image.shape[1]), 
                             int(landmarks[i].y * image.shape[0])) for i in jawline_indices])
        right_cheek_points = np.array([(int(landmarks[i].x * image.shape[1]), 
                             int(landmarks[i].y * image.shape[0])) for i in right_cheek_indices])
        left_cheek_points = np.array([(int(landmarks[i].x * image.shape[1]), 
                             int(landmarks[i].y * image.shape[0])) for i in left_cheek_indices])
        # create a mask around the region specified
        # forehead
        forehead_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(forehead_mask, [forehead_points], 255)
        forehead_mean_hsv = np.array(cv2.mean(hsv_image, mask = forehead_mask)[:3])

        # jawline
        jawline_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(jawline_mask, [jawline_points], 255)
        jawline_mean_hsv = np.array(cv2.mean(hsv_image, mask = jawline_mask)[:3])

        # right cheek
        right_cheek_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(right_cheek_mask, [right_cheek_points], 255)
        right_cheek_mean_hsv = np.array(cv2.mean(hsv_image, mask = right_cheek_mask)[:3])

        # left cheek

        left_cheek_mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(left_cheek_mask, [left_cheek_points], 255)
        left_cheek_mean_hsv = np.array(cv2.mean(hsv_image, mask = left_cheek_mask)[:3])

        # for display only (test if indices are correct)
        '''
        #forehead_image = cv2.bitwise_and(image, image, mask=forehead_mask)
        # cv2.imshow("Masked Forehead Region", forehead_image)

        #jawline_image = cv2.bitwise_and(image, image, mask=jawline_mask)
        #cv2.imshow("Masked Jawline Region", jawline_image)

        #right_cheek_image = cv2.bitwise_and(image, image, mask=right_cheek_mask)
        #cv2.imshow("Masked Right Cheek Region", right_cheek_image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        '''

    return forehead_mean_hsv, jawline_mean_hsv, right_cheek_mean_hsv, left_cheek_mean_hsv


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
hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)  # Convert to HSV

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

# extract only the skin of image 
'''
skin_only_image = cv2.bitwise_and(cv_image, cv_image, mask=skin_mask.astype(np.uint8))
plt.imshow(skin_only_image)
plt.show()
'''

# get the mean hsvs of the skin 
temp_image = cv2.imread(image_path)
forehead_hsv, jawline_hsv, right_cheek_hsv, left_cheek_hsv = draw_skin_landmarks(temp_image)


data = {
    #"skin": skin_hsv.tolist(),
    "forehead": forehead_hsv.tolist(),
    "jawline": jawline_hsv.tolist(),
    "right_cheek": right_cheek_hsv.tolist(),
    "left_cheek": left_cheek_hsv.tolist(),
    "eyes": eye_hsv.tolist(),
    "hair": hair_hsv.tolist()
}

def get_season(h, s, v):
    # h = Hue in degrees (0 - 360)
    # s = Saturation in % (0 - 100)
    # v = Value/Brightness in % (0 - 100)

    if h >= 20 and h <= 40 and s > 40 and v > 70:
        return "Spring"
    elif h >= 10 and h <= 30 and s < 40 and v > 60:
        return "Summer"
    elif h >= 30 and h <= 50 and s > 30 and v < 70:
        return "Autumn"
    elif h >= 10 and h <= 25 and s > 50 and v < 50:
        return "Winter"
    else:
        return "Neutral / Depends — Try Soft Tones"

def get_palette(season):
    palettes = {
        "Spring": ["#FFD8A9", "#FFCBA4", "#F9C66E", "#FF9999"],
        "Summer": ["#D3E0EA", "#C3B1E1", "#AEC6CF", "#F4DADA"],
        "Autumn": ["#A0522D", "#C19A6B", "#8B4000", "#D2691E"],
        "Winter": ["#003366", "#660066", "#990000", "#004953"],
        "Neutral / Depends — Try Soft Tones": ["#CFCFCF", "#B0A999", "#D9C9B9", "#AFAFAF"]
    }
    return palettes.get(season)

# Example Usage
# Example Skin HSV input
h = 30   # Hue in degrees
s = 35   # Saturation in %
v = 85   # Value/Brightness in %

season = get_season(h, s, v)
palette = get_palette(season)

print(f"Detected Season: {season}")
print(f"Recommended Color Palette: {palette}")


with open("hsv_data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)