class ModelRegistry:
    def __init__(self):
        self.models = {}
        self.load_all()

    def load_all(self):
        from transformers import (
            BlipProcessor, BlipForConditionalGeneration,
            CLIPProcessor, CLIPModel,
            AutoTokenizer, AutoModelForSeq2SeqLM,
            VisionEncoderDecoderModel, ViTImageProcessor
        )
        from ultralytics import YOLO

        # Load all models and processors
        self.models = {
            "yolo": YOLO("yolov8s.pt"),

            "blip": {
                "processor": BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base"),
                "model": BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            },

            "clip": {
                "processor": CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32"),
                "model": CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            },

            "vit_gpt2": {
                "processor": ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning"),
                "model": VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning"),
                "tokenizer": AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
            },

            "flan_t5": {
                "tokenizer": AutoTokenizer.from_pretrained("google/flan-t5-large"),
                "model": AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large")
            }
        }

    def get(self, key):
        return self.models.get(key)
