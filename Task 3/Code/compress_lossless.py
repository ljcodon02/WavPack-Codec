import subprocess
import os
import time

def compress_lossless(input_wav, output_wv):
    cmd = ["wavpack", input_wav, "-o", output_wv]
    print("Đang nén (lossless) với lệnh:", " ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("Nén lossless thành công!")
    else:
        print("Gặp lỗi khi nén lossless:")
        print(result.stderr)

def decompress_lossless(input_wv, output_wav):
    cmd = ["wvunpack", input_wv, "-o", output_wav]
    print("Đang giải nén (lossless) với lệnh:", " ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("Giải nén lossless thành công!")
    else:
        print("Gặp lỗi khi giải nén lossless:")
        print(result.stderr)

def measure_compression_time(func, *args):
    start_time = time.time()
    func(*args)
    return time.time() - start_time

# Gọi hàm nén và tính thời gian
time_taken = measure_compression_time(compress_lossless, "input.wav", "output_lossless.wv")

# Tính tỷ lệ nén
input_size = os.path.getsize("input.wav")
output_size = os.path.getsize("output_lossless.wv")
compression_ratio = (output_size / input_size) * 100

print(f"Thời gian nén lossless: {time_taken:.2f} giây")
print(f"Tỷ lệ nén: {compression_ratio:.1f}%")

decompress_lossless("output_lossless.wv", "decompressed_lossless.wav")