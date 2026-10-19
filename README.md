# Document Scanner

A Django web app that scans a photo of a document, automatically detects its edges, and crops, centers and aligns it into a flat, top-down image ready to download.

## How it works

1. Upload a photo of a document.
2. The image is resized, converted to grayscale and blurred, and edges are found with Canny edge detection.
3. The largest contours are checked for a four-sided outline, which is taken to be the document.
4. A four-point perspective transform flattens the document into a straight, cropped result.
5. Each step (original, edges, detected outline, final scan) is shown on the page, and the final scan can be downloaded as a PNG.

If no four-sided outline is found, or the upload isn't a valid image, the app shows an error message instead.

## Tech stack

- Python 3.12
- Django 5.2
- OpenCV, NumPy, imutils

## Getting started

### Locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

Then open http://127.0.0.1:8000.

### With Docker

```bash
docker compose up --build
```

Then open http://localhost:8000.

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key | Insecure development key |

The project ships with `DEBUG = True` and an empty `ALLOWED_HOSTS`, which is suitable for development only. Set a real secret key and adjust these settings before any public deployment.

## Tips for best results

- Photograph the document against a contrasting, plain background.
- Make sure all four corners of the document are visible.
- Use even lighting and avoid heavy shadows.

## Credits

The scanning approach is based on the PyImageSearch tutorial [Build Kick-Ass Mobile Document Scanner in Just 5 Minutes](https://pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/) by Adrian Rosebrock. The perspective transform helper in `pyimagesearch/transform.py` comes from a [Stack Overflow answer](https://stackoverflow.com/a/59990853) by Nielsou Akbrg, licensed CC BY-SA 4.0.
