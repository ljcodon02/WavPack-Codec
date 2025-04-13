import subprocess
import os
import time

def compress_lossy(input_wav, output_wv):
    cmd = ["wavpack", "-b192", input_wav, "-o", output_wv]
    print("Đang nén (lossy) với lệnh:", " ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("Nén lossy thành công!")
    else:
        print("Gặp lỗi khi nén lossy:")
        print(result.stderr)

def decompress_lossy(input_wv, output_wav):
    cmd = ["wvunpack", input_wv, "-o", output_wav]
    print("Đang giải nén (lossy) với lệnh:", " ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("Giải nén lossy thành công!")
    else:
        print("Gặp lỗi khi giải nén lossy:")
        print(result.stderr)

def measure_compression_time(func, *args):
    start_time = time.time()
    func(*args)
    return time.time() - start_time

# Gọi hàm nén và tính thời gian
time_taken = measure_compression_time(compress_lossy, "input.wav", "output_lossy.wv")

# Tính tỷ lệ nén
input_size = os.path.getsize("input.wav")
output_size = os.path.getsize("output_lossy.wv")
compression_ratio = (output_size / input_size) * 100

print(f"Thời gian nén lossy: {time_taken:.2f} giây")
print(f"Tỷ lệ nén: {compression_ratio:.1f}%")

decompress_lossy("output_lossy.wv", "decompressed_lossy.wav")