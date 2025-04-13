import subprocess
import os
import time

def compress_hybrid(input_wav, output_wv):
    cmd = ["wavpack", "-b256", "-c", input_wav, "-o", output_wv]
    print("Đang nén (hybrid) với lệnh:", " ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("Nén hybrid thành công!")
    else:
        print("Gặp lỗi khi nén hybrid:")
        print(result.stderr)

def decompress_hybrid(input_wv, output_wav):
    cmd = ["wvunpack", input_wv, "-o", output_wav]
    print("Đang giải nén (hybrid) với lệnh:", " ".join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        print("Giải nén hybrid thành công!")
    else:
        print("Gặp lỗi khi giải nén hybrid:")
        print(result.stderr)

def measure_compression_time(func, *args):
    start_time = time.time()
    func(*args)
    return time.time() - start_time

# Gọi hàm nén và tính thời gian
time_taken = measure_compression_time(compress_hybrid, "input.wav", "output_hybrid.wv")

# Tính tỷ lệ nén (bao gồm cả file correction)
input_size = os.path.getsize("input.wav")
output_size = os.path.getsize("output_hybrid.wv") + os.path.getsize("output_hybrid.wvc")
compression_ratio = (output_size / input_size) * 100

print(f"Thời gian nén hybrid: {time_taken:.2f} giây")
print(f"Tỷ lệ nén: {compression_ratio:.1f}%")

decompress_hybrid("output_hybrid.wv", "decompressed_hybrid.wav")