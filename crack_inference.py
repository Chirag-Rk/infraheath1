import torch
import torchvision.transforms as T
from torchvision.models import resnet18
from PIL import Image
import io
import cv2
import numpy as np

from physics_filters.orientation import dominant_orientation
from physics_filters.continuity import crack_length
from physics_filters.mask_utils import generate_binary_mask

MODEL_PATH = "models/baseline_resnet/resnet18_sdnet_baseline.pth"
device = "cpu"

model = resnet18()
model.fc = torch.nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

CRACK_THRESHOLD = 0.6


def run_crack_inference(image_bytes):

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)
        prediction = torch.argmax(probs, dim=1).item()
        confidence = probs[0][prediction].item()

    crack_confirmed = (prediction == 1) and (confidence > CRACK_THRESHOLD)

    # Physics layer
    np_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    mask = generate_binary_mask(np_img)
    angle = dominant_orientation(mask)
    length = crack_length(mask)

    # Risk logic
    if not crack_confirmed:
        risk_label = "LOW"
    else:
        severity = length * confidence
        if severity < 50:
            risk_label = "LOW"
        elif severity < 150:
            risk_label = "MONITOR"
        elif severity < 300:
            risk_label = "MODERATE"
        else:
            risk_label = "HIGH"

    return {
        "crack_confirmed": crack_confirmed,
        "cnn_confidence": round(float(confidence), 4),
        "crack_length": float(length),
        "crack_orientation": float(angle),
        "crack_risk_label": risk_label,
    }