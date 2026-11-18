# Image Processing Toolkit

A Python project that demonstrates core digital image-processing techniques without relying on high-level image transformation functions. The project works with grayscale images and produces saved output images for each experiment.

## Features

- **Spatial sampling and reconstruction** — downsamples images by factors of 2, 8, and 32, then reconstructs them with nearest-neighbor upsampling.
- **Gamma correction** — applies gamma values of 0.5, 1.0, and 2.0 to compare tonal changes.
- **Histogram equalization** — calculates a histogram and cumulative distribution manually, then remaps image intensities.
- **Noise reduction** — implements 3×3 and 7×7 average and median filters with clamped borders.

## Tech stack

Python, NumPy, Pillow, and Matplotlib.

## Run locally

```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
python "Project 1.py"
```

The script regenerates the output images in the repository root. Close the histogram chart windows after Task 3 for the script to continue.

## Project structure

| File | Purpose |
| --- | --- |
| `Project 1.py` | Main image-processing implementation and runner |
| `WALL-E.png`, `banker.jpeg`, `wizardofoznoisesquare.pgm` | Source images used by the experiments |
| `task*.png` | Generated results for the four image-processing tasks |

## Highlights

This work emphasizes understanding the underlying operations by implementing pixel transformations, histogram calculations, and filtering logic directly with loops.
