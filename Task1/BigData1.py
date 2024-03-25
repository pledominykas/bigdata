import os
import time
from multiprocessing import Pool
from multiprocessing import Queue
from multiprocessing import Process
from multiprocessing import cpu_count
import cv2
import numpy as np
import glob

def get_output_path(image_path, output_dir, image_suffix):
    image_name = os.path.basename(image_path)
    image_path = os.path.join(output_dir, image_name.replace('.jpg', f'_{image_suffix}.jpg'))
    return image_path

def convert_to_BW(args):
    image_path, output_dir = args
    image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imwrite(get_output_path(image_path, output_dir, 'BW'), im_bw)

def apply_blur(args):
    image_path, output_dir = args
    image = cv2.imread(image_path)
    blurred = cv2.GaussianBlur(image, (13, 13), 0)

    cv2.imwrite(get_output_path(image_path, output_dir, 'BLUR'), blurred)

def add_noise(args):
    image_path, output_dir = args
    image = cv2.imread(image_path)
    im_bw = cv2.imread(get_output_path(image_path, output_dir, 'BW'))

    black_pixel_count = np.sum(im_bw == 0)
    noise_pixel_count = black_pixel_count * 0.1

    noise = np.zeros(image.shape, np.uint8)
    noise_coord_x = np.random.randint(0, image.shape[0], int(noise_pixel_count))
    noise_coord_y = np.random.randint(0, image.shape[1], int(noise_pixel_count))
    noise_coords = np.column_stack((noise_coord_x, noise_coord_y))
    noise[noise_coords[:, 0], noise_coords[:, 1]] = 255
    noisy = cv2.add(image, noise)

    cv2.imwrite(get_output_path(image_path, output_dir, 'NOISE'), noisy)

def process_images_sequentially(image_directory, output_directory, process_function):
    start_time = time.time()
    for image_filename in os.listdir(image_directory):
        if image_filename.endswith('.jpg'):
            image_path = os.path.join(image_directory, image_filename)
            process_function((image_path, output_directory))
    end_time = time.time()
    return end_time - start_time

def process_images_in_parallel(image_directory, output_directory, process_function, cpu_count):
    start_time = time.time()
    image_paths = [os.path.join(image_directory, f) for f in os.listdir(image_directory) if f.endswith('.jpg')]
    with Pool(processes=cpu_count) as pool:
        pool.map(process_function, zip(image_paths, [output_directory] * len(image_paths)))
    end_time = time.time()
    return end_time - start_time

def dynamic_worker(input_queue):
    while not input_queue.empty():
        image_path, output_directory, process_function = input_queue.get()
        process_function((image_path, output_directory))

if __name__ == '__main__':
    image_dir = r'C:\Users\dominykas.pleseviciu\Desktop\BigData\data_set_VU_test1\Images'
    output_dir = r'C:\Users\dominykas.pleseviciu\Desktop\BigData\Output'

    grayscale_results = []
    blur_results = []
    noise_results = []

    time_sequential_gray = process_images_sequentially(image_dir, output_dir, convert_to_BW)
    time_sequential_blur = process_images_sequentially(image_dir, output_dir, apply_blur)
    time_sequential_noise = process_images_sequentially(image_dir, output_dir, add_noise)

    for process_count in range(1, 24):
        print(f"Process Count: {process_count}")

        # Testing Grayscale Conversion
        time_parallel_gray = process_images_in_parallel(image_dir, output_dir, convert_to_BW, process_count)
        grayscale_results.append([time_sequential_gray, time_parallel_gray])
        print(f"Grayscale Conversion - Sequential: {time_sequential_gray}s, Parallel: {time_parallel_gray}s")

        # Testing Blur
        time_parallel_blur = process_images_in_parallel(image_dir, output_dir, apply_blur, process_count)
        blur_results.append([time_sequential_blur, time_parallel_blur])
        print(f"Blurring - Sequential: {time_sequential_blur}s, Parallel: {time_parallel_blur}s")

        # Testing Noise Addition
        time_parallel_noise = process_images_in_parallel(image_dir, output_dir, add_noise, process_count)
        noise_results.append([time_sequential_noise, time_parallel_noise])
        print(f"Noise Addition - Sequential: {time_sequential_noise}s, Parallel: {time_parallel_noise}s")

        files = glob.glob(os.path.join(output_dir, '*'))
        for f in files:
            os.remove(f)

    grayscale_results = np.array(grayscale_results)
    blur_results = np.array(blur_results)
    noise_results = np.array(noise_results)

    np.savetxt('grayscale_results.csv', grayscale_results, delimiter=',')
    np.savetxt('blur_results.csv', blur_results, delimiter=',')
    np.savetxt('noise_results.csv', noise_results, delimiter=',')