from django.shortcuts import render

# image processing
from pyimagesearch.transform import four_point_transform
import numpy as np
import cv2
import imutils
import base64


# encodes image data for frontend display
def image_encoder(img):
    _, buffer = cv2.imencode(".png", img)
    return base64.b64encode(buffer).decode("utf-8")


def process_file(uploaded_image):
    # Inspiration source - https://pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

    # resize image
    file_bytes = np.frombuffer(uploaded_image.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if image is None:
        return None, None, None, None, "Uploaded file is not a valid image"
    orig = image.copy()
    image = imutils.resize(image, height=500)
    ratio = orig.shape[0] / image.shape[0]

    # convert the image to grayscale, blur it, and find edges
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # encode
    originalImage = image_encoder(image)
    edgedImage = image_encoder(edged)

    # find contours and keep largest
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    # loop over the contours
    screenCnt = None
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # 4 points = found screen
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        error_message = "Could not detect document outline"
        return originalImage, edgedImage, None, None, error_message

    # encode
    contouredImage = image_encoder(cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2))

    # use 4 point transform on image
    warp = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    # encode
    warpedImage = image_encoder(warp)

    return originalImage, edgedImage, contouredImage, warpedImage, None


def index(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("uploaded_file")

        # if nothing is uploaded
        if uploaded_file is None:
            return render(request, "index.html", {"error": "No file was uploaded"})

        # call process function and assign vars
        originalImage, edgedImage, contouredImage, warpedImage, error = process_file(uploaded_file)

        return render(request, "index.html", {
            "originalImage": originalImage,
            "edgedImage": edgedImage,
            "contouredImage": contouredImage,
            "warpedImage": warpedImage,
            "error": error,
        })
    return render(request, "index.html")
