"""
Module with text2image model
inference using HuggingFace
Inference API
"""
import requests

from utils import retry
from io import BytesIO
from PIL import Image

class Model(object):
    """
    Class just to make queries
    using HuggingFace Inference API
    with Python requests
    """
    def __init__(
        self,
        hf_token: str,
        api_url: str,
        name: str,
        device: str = "cpu",
    ) -> None:
        self.device = device
        self.api_url = api_url
        self.name = name
        self.headers = {
            "Authorization": f"Bearer {hf_token}",
            "Content-Type": "application/json", "Accept": "image/png"
        }

    @retry(num_retries=5, wait_time=2)
    def generate(self, prompt: str) -> Image:
        payload = {"inputs": prompt}
        response = requests.post(
            self.api_url, headers=self.headers, json=payload
        )
        image = Image.open(BytesIO(response.content))
        
        return image

    @staticmethod
    def img2bytes(image: Image) -> BytesIO:
        image_bytes = BytesIO()
        image_bytes.name = "last_generated_image.jpeg"
        image.save(image_bytes, "JPEG")
        image_bytes.seek(0)
        
        return image_bytes
    
    def __repr__(self) -> str:
        return f"Model {self.name} from {self.api_url[len('https://api-inference.huggingface.co/models/'):]} on {self.device}"
    
    