from pathlib import Path
import random


class ImageProvider:

    def __init__(self):
        self.image_dir = Path("/home/sb/web/klee_images/images")
        # self.image_dir = Path("/home/dinu/Pictures/wallpaper")
        if self.image_dir.is_dir():
            self.images = [i for i in self.image_dir.iterdir() if i.is_file() and i.suffix == ".jpg"]
        print(self.images)

    def get_random(self) -> Path | None:
        if len(self.images) != 0:
            file = random.choice(self.images)
            return file
        return None
