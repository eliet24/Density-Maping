import torch
from PIL import Image
import ModelRegistry

"""
class that handles all the requests prompt creation and models input and output
"""

class PromptGenerator:
    def __init__(self, business_categories_file, registry: ModelRegistry):
        self.models = registry
        self.business_categories = self.load_business_categories(business_categories_file)


    def load_business_categories(self, file_path:str):
        with open(file_path, "r", encoding="utf-8") as file:
            return set(line.strip() for line in file if line.strip())

    def find_relevant_categories(self, object_name:str, max_categories=30):
        object_name = object_name.lower()
        relevant = [cat for cat in self.business_categories if object_name in cat.lower]
        return relevant[:max_categories]

    def generate_prompt(self, object_name, object_description):
        categories = self.find_relevant_categories(object_name)
        categories_text = ", ".join(categories) if categories else "various businesses"
        return f"In what kind of businesses can i find a {object_name}? {object_description}" #f"Choose from: {categories_text}"

    def get_nlp_response(self, prompt):
        tokenizer = self.models.get("flan_t5")["tokenizer"]
        model = self.models.get("flan_t5")["model"]
        inputs = tokenizer(prompt, return_tensors = "pt")
        output = model.generate(**inputs, max_length=100)
        return tokenizer.decode(output[0], skip_special_tokens=True)

    def recognize_with_yolo(self, image_path):
        model = self.models.get("yolo")
        image = Image.open(image_path)
        results = model(image, conf=0.5, iou=0.4)

        if not results or not results[0].boxes:
            return None

        result = results[0]
        boxes = result.boxes.xywh.cpu().numpy()
        labels = result.boxes.cls.cpu().numpy()
        sizes = [w * h for _, _, w, h in boxes]
        largest_idx = sizes.index(max(sizes))
        return result.names[int(labels[largest_idx])]

    def recognize_with_blip(self, image_path):
        processor = self.models.get("blip")["processor"]
        model = self.models.get("blip")["model"]
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")
        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)

    def recognize_with_clip(self, image_path):
        processor = self.models.get("clip")["processor"]
        model = self.models.get("clip")["model"]

        texts = ["car", "chair", "dog", "wrench", "tool", "machine part", "laptop", "phone",
                 "pizza", "burger", "bicycle", "motorcycle", "keyboard", "coffee cup",
                 "television", "microwave", "airplane", "train", "refrigerator", "backpack",
                 "umbrella", "lamp", "stapler", "watch", "glasses", "hat", "shirt", "shoe",
                 "bottle", "cup", "wine glass", "fork", "knife", "spoon", "sandwich",
                 "banana", "apple", "orange", "broccoli", "carrot", "hot dog", "couch",
                 "bed", "toilet", "door", "window", "flower", "plant", "tree", "painting",
                 "clock", "mirror", "headphones", "drone", "tablet", "game controller"]

        inputs = processor(
            text=texts,
            images=Image.open(image_path).convert("RGB"),
            return_tensors="pt",
            padding=True,
            truncation=True
        )

        outputs = model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
        best_idx = probs.argmax().item()
        return texts[best_idx]

    def recognize_with_vit_gpt2(self, image_path):
        processor = self.models.get("vit_gpt2")["processor"]
        model = self.models.get("vit_gpt2")["model"]
        tokenizer = self.models.get("vit_gpt2")["tokenizer"]

        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(**inputs)

        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    def process_image(self, image_path:str, object_description:str):
        recognizers = [
            self.recognize_with_yolo,
            self.recognize_with_blip,
            self.recognize_with_clip,
            self.recognize_with_vit_gpt2
        ]

        for recognize in recognizers:
            found_object = recognize(image_path)
            if found_object:
                prompt = self.generate_prompt(found_object, object_description)
                response = self.get_nlp_response(prompt)
                return found_object, prompt, response

        return None, None, None




