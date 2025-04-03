import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from ultralytics import YOLO
from transformers import CLIPProcessor, CLIPModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import VisionEncoderDecoderModel, ViTImageProcessor

# Load YOLOv8 Model
yolo_model = YOLO("yolov8s.pt")  # YOLOv8 (small version)

# Load BLIP-Image-Captioning Model
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load CLIP Model
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Load ViT-GPT2 Image Captioning Model
vit_gpt2_model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
vit_gpt2_processor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
vit_gpt2_tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

# Load NLP Model (FLAN-T5)
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
nlp_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")

# Load Business Categories from File
def load_business_categories(file_path):
    """Load business categories from a text file."""
    with open(file_path, "r", encoding="utf-8") as file:
        categories = [line.strip() for line in file.readlines() if line.strip()]
    return set(categories)

# Path to Business Categories file
business_categories_file = "/ML_PromptCode/BusinessCategories.txt"
business_categories = load_business_categories(business_categories_file)

# Function to find relevant business categories
def find_relevant_categories(object_name, max_categories=30):
    """Find business categories related to the detected object."""
    object_name = object_name.lower()
    relevant = [cat for cat in business_categories if object_name in cat.lower()]
    return relevant[:max_categories]  # Limit categories for better NLP performance

# Function to generate business prompt with explanation
def generate_business_prompt(object_name, object_description):
    """Generate NLP prompt with the detected object + user-provided explanation."""
    relevant_categories = find_relevant_categories(object_name)
    categories_text = ", ".join(relevant_categories) if relevant_categories else "various businesses"

    return (
        f"In what kind of businesses can I find a {object_name}? {object_description} "
        #f"Choose from: {categories_text}"
    )

# Function to get NLP response
def get_nlp_response(prompt):
    """Get a response from FLAN-T5 with object + description."""
    inputs = tokenizer(prompt, return_tensors="pt")
    output = nlp_model.generate(**inputs, max_length=100)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return response

# YOLOv8 Object Detection
def recognize_with_yolo(image_path):
    """YOLOv8 object detection"""
    image = Image.open(image_path)
    results = yolo_model(image, conf=0.5, iou=0.4)

    if not results or not results[0].boxes:
        return None

    result = results[0]
    boxes = result.boxes.xywh.cpu().numpy()
    labels = result.boxes.cls.cpu().numpy()
    sizes = [w * h for _, _, w, h in boxes]

    largest_idx = sizes.index(max(sizes))
    largest_label = result.names[int(labels[largest_idx])]

    return largest_label

# BLIP-Image-Captioning for Object Recognition
def recognize_with_blip(image_path):
    """BLIP image captioning"""
    image = Image.open(image_path).convert("RGB")

    inputs = blip_processor(images=image, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)

    return caption

# CLIP Image Classification
def recognize_with_clip(image_path):
    """CLIP image classification"""
    texts = ["car", "chair", "dog", "wrench", "tool", "machine part", "laptop", "phone",
    "pizza", "burger", "bicycle", "motorcycle", "keyboard", "coffee cup",
    "television", "microwave", "airplane", "train", "refrigerator", "backpack",
    "umbrella", "lamp", "stapler", "watch", "glasses", "hat", "shirt", "shoe",
    "bottle", "cup", "wine glass", "fork", "knife", "spoon", "sandwich",
    "banana", "apple", "orange", "broccoli", "carrot", "hot dog", "couch",
    "bed", "toilet", "door", "window", "flower", "plant", "tree", "painting",
    "clock", "mirror", "headphones", "drone", "tablet", "game controller"]

    inputs = clip_processor(
        text=texts,
        images=Image.open(image_path).convert("RGB"),
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    outputs = clip_model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)
    best_idx = probs.argmax().item()

    return texts[best_idx]

# ViT-GPT2 Image Captioning
def recognize_with_vit_gpt2(image_path):
    """ViT-GPT2 image captioning"""
    image = Image.open(image_path).convert("RGB")

    inputs = vit_gpt2_processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = vit_gpt2_model.generate(**inputs)

    caption = vit_gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return caption

# Main function
def main():
    image_path = "/ML_PromptCode/TestFiles/shoes.jpg"

    # Example explanation input from user (For now, just a variable)
    object_description = "This is a type of footwear used for running and walking."

    # Try YOLO first
    found_object = recognize_with_yolo(image_path)
    if found_object:
        print("Detected by YOLO:", found_object)
        prompt = generate_business_prompt(found_object, object_description)
        print("Generated Prompt:", prompt)

        # Get NLP Response
        response = get_nlp_response(prompt)
        print("NLP Model Response:", response)

    # Try BLIP Image Captioning
    found_object = recognize_with_blip(image_path)
    if found_object:
        print("Detected by BLIP:", found_object)
        prompt = generate_business_prompt(found_object, object_description)
        print("Generated Prompt:", prompt)

        response = get_nlp_response(prompt)
        print("NLP Model Response:", response)

    # Try CLIP Classification
    found_object = recognize_with_clip(image_path)
    if found_object:
        print("Detected by CLIP:", found_object)
        prompt = generate_business_prompt(found_object, object_description)
        print("Generated Prompt:", prompt)

        response = get_nlp_response(prompt)
        print("NLP Model Response:", response)

    # Try ViT-GPT2 Image Captioning
    found_object = recognize_with_vit_gpt2(image_path)
    if found_object:
        print("Detected by ViT-GPT2:", found_object)
        prompt = generate_business_prompt(found_object, object_description)
        print("Generated Prompt:", prompt)

        response = get_nlp_response(prompt)
        print("NLP Model Response:", response)

if __name__ == "__main__":
    main()
