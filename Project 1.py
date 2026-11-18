import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

#Helper functions: loading and saving grayscale images
def load_grayscale(path):
    #Load an image and convert to grayscale array
    image = Image.open(path).convert('L')
    return np.array(image)

def save_grayscale(arr, path):
    #Save a grayscale array as an image.
    image = Image.fromarray(arr.astype(np.uint8), mode='L')
    image.save(path)
"--------------------------------------------------------------------------"
#Task 1: Spatial Sampling and Reconstruction
def downsample(image, factor):
    #Manual downsampling by selecting every factor-th pixel.
    h, w = image.shape
    new_h, new_w = h // factor, w // factor
    out = np.zeros((new_h, new_w), dtype = image.dtype)

    for i in range(new_h):
        for j in range(new_w):
            out[i, j] = image[i * factor, j * factor]

    return out

def upsample_nn(image, factor):
    #Manual nearest-neighbour upsampling using pixel replication.
    h, w = image.shape
    new_h, new_w = h * factor, w * factor
    out = np.zeros((new_h, new_w), dtype = image.dtype)

    for i in range(new_h):
        for j in range(new_w):
            out[i, j] = image[i // factor, j // factor]

    return out

def run_task1():
    print("Running Task 1...")
    original = load_grayscale("WALL-E.png")

    for factor in [2, 8, 32]:
        down = downsample(original, factor)
        up = upsample_nn(down, factor)

        save_grayscale(down, f"task1_down_{factor}.png")
        save_grayscale(up, f"task1_up_{factor}.png")

    print("Task 1 Completed. \n")
"-----------------------------------------------------------------------------"
#Task 2: Gamma Correction
def gamma_correct(image, gamma):
    #Manual gamma correction using loops.
    h, w = image.shape
    out = np.zeros_like(image)

    for i in range(h):
        for j in range(w):
            norm = image[i, j] / 255.0
            corrected = norm ** gamma
            val = int(corrected * 255)
            out[i, j] = max(0, min(255, val))

    return out

def run_task2():
    print("Running Task 2...")
    banker = load_grayscale("banker.jpeg")

    for g in [0.5, 1.0, 2.0]:
        gc = gamma_correct(banker, g)
        save_grayscale(gc, f"task2_gamma_{g}.png")

    print("Task 2 Completed. \n")
"-----------------------------------------------------------------------------"
#Task 3: Histogram Equalisation
def compute_histogram(image):
    #Manual histogram counting.
    hist = [0] * 256
    h, w = image.shape
    for i in range(h):
        for j in range(w):
            hist[int(image[i, j])] += 1
    return hist

def cumulative(hist):
    #Manual cumulative distribution function.
    cdf = [0] * 256
    total = 0
    for i in range(256):
        total += hist[i]
        cdf[i] = total
    return cdf

def build_equalization_mapping(hist):
    #Build intensity mapping for histogram equalisation.
    cdf = cumulative(hist)
    total_pixels = cdf[-1]
    mapping = [0] * 256

    for v in range(256):
        mapped = int(cdf[v] / total_pixels * 255)
        mapping[v] = max(0, min(255, mapped))
    return mapping

def apply_mapping(image, mapping):
    #Apply intensity mapping to image.
    h, w = image.shape
    out = np.zeros_like(image)
    for i in range(h):
        for j in range(w):
            out[i, j] = mapping[int(image[i, j])]
    return out

def plot_hist(hist, title):
    #Plot histogram using my own counts.
    plt.figure()
    plt.bar(range(256), hist)
    plt.title(title)
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")
    plt.xlim(0, 255)
    plt.show()

def run_task3():
    print("Running Task 3...")
    banker = load_grayscale("banker.jpeg")

    hist_original = compute_histogram(banker)
    mapping = build_equalization_mapping(hist_original)
    banker_eq = apply_mapping(banker, mapping)

    save_grayscale(banker_eq, "task3_equalised.png")

    #Plot histograms
    hist_eq = compute_histogram(banker_eq)
    plot_hist(hist_original, "Original banker histogram")
    plot_hist(hist_eq, "Equalized banker histogram")

    print("Task 3 Completed. \n")
"-----------------------------------------------------------------------------"
#Task 4: Average and Median Filters
def get_window(image, i, j, k):
    #Collect a kxk window with clamped borders.
    pad = k // 2
    h, w = image.shape
    window = []

    for a in range(-pad, pad + 1):
        for b in range(-pad, pad + 1):
            x = min(max(i + a, 0), h - 1)
            y = min(max(j + b, 0), w - 1)
            window.append(int(image[x, y]))
    return window

def average_filer(image, k):
    #Manual average filter.
    h, w = image.shape
    out = np.zeros_like(image)

    for i in range(h):
        for j in range(w):
            window = get_window(image, i, j, k)
            out[i, j] = sum(window) // len(window)
    return out

def median_filer(image, k):
    #Manual median filter using sort.
    h, w = image.shape
    out = np.zeros_like(image)

    for i in range(h):
        for j in range(w):
            window = get_window(image, i, j, k)
            window.sort()
            out[i, j] = window[len(window) // 2]
    return out

def run_task4():
    print("Running Task 4...")

    wiz = load_grayscale("wizardofoznoisesquare.pgm")

    for k in [3, 7]:
        avg = average_filer(wiz, k)
        med = median_filer(wiz, k)

        save_grayscale(avg, f"task4_avg_{k}x{k}.png")
        save_grayscale(med, f"task4_med_{k}x{k}.png")
    print("Task 4 Completed. \n")
"-----------------------------------------------------------------------------"
def main():
    print("Starting Integrated Image Processing Project...\n")

    #Image Preparation Step
    print("Preparing supplied image for Task 1...")

    img = Image.open("Wall-e(ML).jpg")

    #Square crop
    side = min(img.size)
    img = img.crop((0, 0, side, side))

    #Resize to 1024 x 1024
    img = img.resize((1024, 1024))

    #Convert to grayscale
    img = img.convert("L")
    img.save("WALL-E.png")

    print("Image preparation completed. \n")

    #Run all the tasks
    run_task1()
    run_task2()
    run_task3()
    run_task4()

    print("All tasks completed.")

if __name__ == "__main__":
    main()