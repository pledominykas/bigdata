import pandas as pd
import matplotlib.pyplot as plt

grayscale_results = pd.read_csv(r'C:\Users\dominykas.pleseviciu\Desktop\BigData\grayscale_results.csv', header=None).values
blur_results = pd.read_csv(r'C:\Users\dominykas.pleseviciu\Desktop\BigData\blur_results.csv', header=None).values
noise_results = pd.read_csv(r'C:\Users\dominykas.pleseviciu\Desktop\BigData\noise_results.csv', header=None).values

avg_seq_gray = grayscale_results[:, 0].mean()
avg_seq_blur = blur_results[:, 0].mean()
avg_seq_noise = noise_results[:, 0].mean()

plt.title('Image Processing Time Comparison')
plt.plot(range(1, 24), grayscale_results[:, 1], color='blue', label='B&W Conversion - Parallel')
plt.axhline(avg_seq_gray, color='blue', linestyle='--', label='B&W Conversion - Sequential')
plt.plot(range(1, 24), blur_results[:, 1], color='orange', label='Blurring - Parallel')
plt.axhline(avg_seq_blur, color='orange', linestyle='--', label='Blurring - Sequential')
plt.plot(range(1, 24), noise_results[:, 1], color='green', label='Noise Addition - Parallel')
plt.axhline(avg_seq_noise, color='green', linestyle='--', label='Noise Addition - Sequential')
plt.legend()
plt.xlabel('Number of Processes')
plt.ylabel('Time (s)')
plt.gcf().set_size_inches(10, 8)
plt.xticks(range(1, 24))

plt.show()

plt.pause(5)