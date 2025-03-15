import torch
from PIL import Image
import cv2
from ultralytics import YOLO
from transformers import DetrImageProcessor, DetrForObjectDetection, CLIPProcessor, CLIPModel
from torchvision import transforms  # Add this import
import numpy as np

# Load Models
yolo_model = YOLO("yolov8s.pt")  # YOLOv8 model (small version)
detr_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
detr_processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def preprocess_for_yolo(image_path):
    """Pre-processing for YOLO"""
    # Read and resize the image
    image = cv2.imread(image_path)
    image = cv2.resize(image, (416, 416))  # Resize to YOLO's expected input size
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    image = image / 255.0  # Normalize to [0, 1]
    return image


def preprocess_for_detr(image_path):
    """Pre-processing for DETR"""
    image = Image.open(image_path).convert("RGB")

    # Resize and normalize
    transform = transforms.Compose([
        transforms.Resize((800, 800)),
        transforms.ToTensor(),  # Convert the image to tensor
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalization
    ])

    # Apply the transform and ensure the image is properly normalized
    image = transform(image)

    # Ensure the values are between [0, 1] after normalization
    image = torch.clamp(image, min=0.0, max=1.0)

    return image


def preprocess_for_clip(image_path, texts):
    """Pre-processing for CLIP"""
    image = Image.open(image_path).convert("RGB")

    # Resize and normalize image for CLIP
    inputs = clip_processor(text=texts, images=image, return_tensors="pt", padding=True)
    return inputs


def recognize_with_yolo(image_path):
    """YOLOv8 object detection with pre-processing"""
    image = Image.open(image_path)

    # Apply necessary pre-processing steps here (e.g., resizing, normalization)
    image = image.resize((640, 640))  # Example resizing, adjust as needed

    results = yolo_model(image, conf=0.5, iou=0.4)  # Adjust confidence and NMS threshold

    if not results or not results[0].boxes:
        return None  # No objects detected

    # Get the largest object
    result = results[0]
    boxes = result.boxes.xywh.cpu().numpy()
    labels = result.boxes.cls.cpu().numpy()
    sizes = [w * h for _, _, w, h in boxes]

    largest_idx = sizes.index(max(sizes))
    largest_label = result.names[int(labels[largest_idx])]

    return largest_label


def recognize_with_detr(image_path):
    """DETR object detection with better pre-processing"""
    image = Image.open(image_path).convert("RGB")

    # Apply transformations, such as resizing and normalization
    image = image.resize((800, 800))  # Resize image for DETR

    inputs = detr_processor(images=image, return_tensors="pt", do_rescale=False)  # Ensure no additional scaling
    outputs = detr_model(**inputs)

    target_sizes = torch.tensor([[image.size[1], image.size[0]]])  # Correct target size (height, width)
    results = detr_processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.5)[0]

    if len(results['boxes']) == 0:
        return None

    boxes = results['boxes'].detach().cpu().numpy()
    labels = results['labels'].detach().cpu().numpy()

    sizes = [w * h for _, _, w, h in boxes]
    largest_idx = sizes.index(max(sizes))
    largest_label = labels[largest_idx]

    label_name = detr_model.config.id2label[largest_label]

    return label_name


def recognize_with_clip(image_path):
    """CLIP image classification"""
    texts = ["a car", "a chair", "a dog", "a wrench", "a tool", "an object", "a machine part"]

    inputs = preprocess_for_clip(image_path, texts)  # Pre-process the image for CLIP
    outputs = clip_model(**inputs)

    probs = outputs.logits_per_image.softmax(dim=1)  # Convert logits to probabilities
    best_idx = probs.argmax().item()

    return texts[best_idx]  # Best matching label


def generate_business_prompt(object_name):
    """Generate NLP prompt"""
    return f"In what kind of businesses can I find a {object_name}?"


def main():
    image_path = "D:/PycharmProjects/Density-Maping/NewProject/TestFiles/test4.jpg"

    # Try YOLO first
    found_object = recognize_with_yolo(image_path)
    if found_object:
        prompt = generate_business_prompt(found_object)
        print("Generated Prompt:", prompt)
    else:
        print("No object detected by YOLO")

    # If YOLO fails, try DETR
    found_object = recognize_with_detr(image_path)
    if found_object:
        prompt = generate_business_prompt(found_object)
        print("Generated Prompt:", prompt)
    else:
        print("No object detected by DETR")

    # If DETR also fails, try CLIP
    found_object = recognize_with_clip(image_path)
    if found_object:
        prompt = generate_business_prompt(found_object)
        print("Generated Prompt:", prompt)
    else:
        print("No object detected by CLIP")


if __name__ == "__main__":
    main()
