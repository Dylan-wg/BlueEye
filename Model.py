import torch.cuda
from PIL.Image import Image
from ultralytics import YOLO


class Model:

    def __init__(self):
        self.model = YOLO("./best.pt")

    def predict(self, path: str) -> str:
        if torch.cuda.is_available():
            result = self.model.predict(path, device=0)
        else:
            result = self.model.predict(path, device="cpu")
        name = self.get_name(path)
        result[0].save("./runs/detect/predict/" + name)
        new_path = "./runs/detect/predict/" + name
        return new_path

    @staticmethod
    def get_name(path) -> str:
        rt = ""
        for i in path[::-1]:
            if i != "/":
                rt = i + rt
            else:
                break
        return rt

    def predict_img(self, img: Image) -> Image:
        result = self.model(img)
        result[0].save("./runs/detect/predict/v.jpg")
