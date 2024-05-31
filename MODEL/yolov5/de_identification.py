import numpy as np
import cv2
import torch
from PIL import Image, ImageDraw


class Deident:
    def __init__(self, im, pil=False):
        """Initialize the Annotator class with image and line width along with color palette for keypoints and limbs."""
        # non_ascii = not is_ascii(example)  # non-latin labels, i.e. asian, arabic, cyrillic
        input_is_pil = isinstance(im, Image.Image)
        self.pil = pil or input_is_pil
        if self.pil:  # use PIL
            self.im = im if input_is_pil else Image.fromarray(im)
            self.draw = ImageDraw.Draw(self.im)
        else:  # use cv2
            assert (
                im.data.contiguous
            ), "Image not contiguous. Apply np.ascontiguousarray(im) to Annotator input images."
            self.im = im if im.flags.writeable else im.copy()

    def add_padding(self, image, pad, color=(0, 0, 0)):
        """Add padding to the image."""
        return cv2.copyMakeBorder(
            image, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=color
        )

    def remove_padding(self, image, pad):
        """Remove padding from the image."""
        h, w = image.shape[:2]
        return image[pad : h - pad, pad : w - pad]

    def enlarge_roi(self, box, scale=1.2):
        """Enlargement of the roi."""
        pad_flag = False
        x, y, w, h = (
            int(box[0]),
            int(box[1]),
            int(box[2] - box[0]),
            int(box[3] - box[1]),
        )
        center_x, center_y = x + w // 2, y + h // 2
        new_w, new_h = int(w * scale), int(h * scale)
        new_x = center_x - new_w // 2
        new_y = center_y - new_h // 2
        if (
            new_x < 0
            or new_y < 0
            or self.im.shape[0] < (new_y + new_h)
            or self.im.shape[1] < (new_x + new_w)
        ):
            pad_flag = True
        return (new_x, new_y, new_w, new_h, pad_flag)

    def mosaic_func(self, roi, w, h):
        """Mosaic function."""
        mosaic_scale = round(0.13 - ((min(w, h) // 10) * 0.005), 3)
        mosaic_scale = np.clip(mosaic_scale, 0.03, 0.1)
        while True:
            try:
                mosaic_roi = cv2.resize(
                    roi,
                    None,
                    fx=mosaic_scale,
                    fy=mosaic_scale,
                    interpolation=cv2.INTER_NEAREST,
                )
                break
            except cv2.error:
                mosaic_scale += 0.001
        mosaic_roi = cv2.resize(mosaic_roi, (w, h), interpolation=cv2.INTER_NEAREST)
        return mosaic_roi

    def blur_func(self, roi, w, h):
        """Blur function."""
        blur_scale = 3
        k1, k2 = (w // blur_scale, h // blur_scale)
        kernel = ((k1 if k1 % 2 == 1 else k1 + 1), (k2 if k2 % 2 == 1 else k2 + 1))
        blur_roi = cv2.GaussianBlur(roi, kernel, 0)
        return blur_roi

    def apply_rectangle_mosaic(self, box):
        """Add one mosaic box to image."""
        if isinstance(box, torch.Tensor):
            box = box.tolist()
        x, y, w, h = (
            int(box[0]),
            int(box[1]),
            int(box[2] - box[0]),
            int(box[3] - box[1]),
        )
        roi = self.im[y : y + h, x : x + w]
        mosaic_roi = self.mosaic_func(roi, w, h)
        self.im[y : y + h, x : x + w] = mosaic_roi

    def apply_ellipse_mosaic(self, box):
        """Add one mosaic ellipse to image."""
        if isinstance(box, torch.Tensor):
            box = box.tolist()
        x, y, w, h, pad_flage = self.enlarge_roi(box)
        if pad_flage:
            pad = max(w, h)
            image = self.add_padding(self.im, pad)
            x, y = x + pad, y + pad
        else:
            image = self.im
        roi = image[y : y + h, x : x + w]
        mask = np.zeros((h, w), dtype=np.uint8)
        center = (w // 2, h // 2)
        axes = (w // 2, h // 2)
        cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)

        mosaic_roi = self.mosaic_func(roi, w, h)
        mosaic_result = cv2.bitwise_and(mosaic_roi, mosaic_roi, mask=mask)
        background = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))
        combined = cv2.add(mosaic_result, background)

        image[y : y + h, x : x + w] = combined
        self.im = self.remove_padding(image, pad) if pad_flage else image

    def apply_rectangle_blur(self, box):
        """Add one blur box to image."""
        if isinstance(box, torch.Tensor):
            box = box.tolist()
        x, y, w, h = (
            int(box[0]),
            int(box[1]),
            int(box[2] - box[0]),
            int(box[3] - box[1]),
        )
        roi = self.im[y : y + h, x : x + w]
        blur_roi = self.blur_func(roi, w, h)
        self.im[y : y + h, x : x + w] = blur_roi

    def apply_ellipse_blur(self, box):
        """Add one blur ellipse to image."""
        if isinstance(box, torch.Tensor):
            box = box.tolist()
        x, y, w, h, pad_flag = self.enlarge_roi(box)
        if pad_flag:
            pad = max(w, h)
            image = self.add_padding(self.im, pad)
            x, y = x + pad, y + pad
        else:
            image = self.im
        roi = image[y : y + h, x : x + w]
        mask = np.zeros((h, w), dtype=np.uint8)
        center = (w // 2, h // 2)
        axes = (int(w // 2), int(h // 2))
        cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)

        blur_roi = self.blur_func(roi, w, h)
        mosaic_result = cv2.bitwise_and(blur_roi, blur_roi, mask=mask)
        background = cv2.bitwise_and(roi, roi, mask=cv2.bitwise_not(mask))
        combined = cv2.add(mosaic_result, background)

        image[y : y + h, x : x + w] = combined
        self.im = self.remove_padding(image, pad) if pad_flag else image

    def result(self):
        """Return annotated image as array."""
        return np.asarray(self.im)
