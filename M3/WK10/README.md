# Week 10 — Image Processing (FreshTrack CV Pipeline)

This repository contains a completed computer vision assignment for the Fusemachines AI Fellowship. The work focuses on classical image-processing techniques using a real classroom image set and a Fruits-360 subset, with the full workflow implemented in a notebook.

## What this project covers

- Color-space inspection and fruit segmentation using HSV masks
- Morphological operations and image denoising
- Edge detection with a custom Canny pipeline and OpenCV comparison
- Feature detection with Harris corners, Hough circles, and a full fruit-detection pipeline

## Tech stack

Python · OpenCV · NumPy · Matplotlib · kagglehub

## Files in this workspace

- [assignment/W10_Image_Processing_Assignment.ipynb](assignment/W10_Image_Processing_Assignment.ipynb) — the main assignment notebook
- [W10_Image_Processing_Assignment_executed.ipynb](W10_Image_Processing_Assignment_executed.ipynb) — the executed version with outputs
- [docs/W10 Image Processing.pdf](docs/W10%20Image%20Processing.pdf) — reference material for the assignment
- [data](data) — workspace folder for supporting data assets
- [LICENSE](LICENSE) — project license

## Dataset and inputs

The notebook uses:

- Fruits-360 via kagglehub, mapped to six required classes: red_apple, green_apple, banana, strawberry, orange, and lime
- Instructor-provided images: morphology.png, chessboard.png, and mixed_fruit_bowl.jpeg

## Workflow summary

### Part A — Color Space & Fruit Segmentation
- Explores BGR vs RGB channel ordering
- Builds per-fruit HSV masks with inRange()
- Performs multi-class segmentation on the bowl image

### Part B — Morphology & Denoising
- Applies erosion, dilation, opening, closing, and gradient operations to morphology.png
- Adds and removes noise using Gaussian, median, and bilateral filters

### Part C — Edge Detection
- Implements Canny edge detection from scratch using Sobel gradients, non-max suppression, double thresholding, and hysteresis
- Compares the custom result with cv2.Canny()

### Part D — Feature Detection
- Detects corners with Harris corner response
- Uses Hough circles on the fruit bowl image
- Builds a complete single-fruit detection pipeline using masking, morphology, contours, and bounding boxes

## Notes from the completed run

- The notebook handles the real dataset naming mismatch by normalizing mixed_fruit_bowl.jpeg to mixed_bowl.jpg during upload.
- Hough circle parameters were tuned for real images instead of synthetic defaults to reduce false positives.
- The fruit-detection pipeline was improved to separate touching apples using connected-component analysis after initial segmentation.

## How to run

1. Open the assignment notebook in Colab or Jupyter.
2. Add Kaggle credentials using Colab Secrets or upload kaggle.json as shown in the notebook.
3. Note that the notebook uses the Kaggle legacy API, so the Kaggle CLI/API setup must be compatible with that workflow.
4. Upload the instructor images morphology.png, chessboard.png, and mixed_fruit_bowl.jpeg.
5. Run the notebook from top to bottom to generate the outputs.

## License

See [LICENSE](LICENSE).
