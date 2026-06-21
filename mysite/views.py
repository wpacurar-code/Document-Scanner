from django.shortcuts import render
from django.http import HttpResponse

# image processing
from pyimagesearch.transform import four_point_transform
import numpy as np
import argparse
import cv2
import imutils
import base64


def image_encoder(img):
    _, buffer = cv2.imencode(".png", img)
    return base64.b64encode(buffer).decode("utf-8")


def process_file(uploaded_image):
    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    file_bytes = np.frombuffer(uploaded_image.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)
    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # encode
    image = image_encoder(image)
    edged = image_encoder(edged)

    return image, edged


def index(request):
    if request.method == "POST":
        uploaded_file = request.FILES["uploaded_file"]

        image, edged = process_file(uploaded_file)

        return render(request, "index.html", {
            "image": image,
            "edged": edged
        })

    return render(request, "index.html")
