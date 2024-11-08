import cv2
from PIL import Image, ImageOps


class Camera_interface:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.image: Image = None

    def cap_enable(self) -> bool:
        return self.cap.isOpened()

    def update_image(self) -> bool:
        ret, frame = self.cap.read()
        if not ret:
            return False

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        self.image = image
        # self.image = ImageOps.mirror(image)
        return True

    @staticmethod
    def list_cameras():
        index = 0
        available_cameras = []
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                available_cameras.append(index)
            cap.release()
            index += 1
        return available_cameras
