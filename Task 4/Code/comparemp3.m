% Folder path containing the .wv file
inputFolder = 'C:\matlab\';

% Base name of the file without extension
name = 'output_lossless';

% Paths to the files
wvFile      = fullfile(inputFolder, [name, '.wv']);
wavFile     = fullfile(inputFolder, [name, '.wav']);
mp3File     = fullfile(inputFolder, [name, '.mp3']);
decodedWav  = fullfile(inputFolder, [name, '_decoded.wav']);

% Check if the .wv file exists
if exist(wvFile, 'file') ~= 2
    error('The .wv file does not exist!');
end

% Check the current folder path
disp(['Current working folder: ', inputFolder]);

% Decompress .wv to .wav using ffmpeg
ffmpegPath = '"C:\matlab\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"';
status = system(sprintf('%s -y -i "%s" "%s"', ffmpegPath, wvFile, wavFile));
if status ~= 0
    error('Error during .wv to .wav conversion');
end

% Verify that the .wav file was created correctly
if exist(wavFile, 'file') ~= 2
    error('The .wav file was not created correctly!');
end

% Load the original .wav file
[original, Fs1] = audioread(wavFile);
disp('File .wav loaded successfully!');

% Compress the .wav file to .mp3 using ffmpeg
status = system(sprintf('%s -y -i "%s" "%s"', ffmpegPath, wavFile, mp3File));
if status ~= 0
    error('Error during .wav to .mp3 conversion');
end

% Decode the .mp3 file back to .wav using ffmpeg
status = system(sprintf('%s -y -i "%s" "%s"', ffmpegPath, mp3File, decodedWav));
if status ~= 0
    error('Error during .mp3 to .wav conversion');
end

% Load the decoded .mp3 file (now a .wav)
[decoded, Fs2] = audioread(decodedWav);

% Resample if the sample rates are different
if Fs1 ~= Fs2
    decoded = resample(decoded, Fs1, Fs2);
end

% Trim both signals to the same length
minLen = min(size(original,1), size(decoded,1));
original = original(1:minLen, :);
decoded  = decoded(1:minLen, :);

% Calculate the Mean Squared Error (MSE)
mse = mean((original - decoded).^2, 'all');

% Calculate the peak value (maximum value) of the original signal
peak = max(abs(original), [], 'all');

% Calculate PSNR (Peak Signal-to-Noise Ratio)
psnrValue = 10 * log10(peak^2 / mse);

% Display the PSNR result
fprintf('File: %s | PSNR = %.2f dB\n', name, psnrValue);

% Plot the analysis results
t = (0:minLen-1) / Fs1;

figure('Name', ['Analysis for ', name], 'NumberTitle', 'off');

% Plot the waveform
subplot(3,1,1);
plot(t, original, 'b'); hold on;
plot(t, decoded, 'r');
title('Waveform'); legend('Original (.wv)', 'Decoded (.mp3)');
xlabel('Time (s)'); ylabel('Amplitude');

% Plot the frequency spectrum
subplot(3,1,2);
N = length(original);
f = Fs1*(0:(N/2))/N;
Y1 = abs(fft(original(:,1), N));
Y2 = abs(fft(decoded(:,1), N));
plot(f, Y1(1:N/2+1), 'b'); hold on;
plot(f, Y2(1:N/2+1), 'r');
title('Frequency Spectrum'); legend('Original', 'Decoded');
xlabel('Frequency (Hz)'); ylabel('Magnitude');

% Plot the error signal
subplot(3,1,3);
plot(t, original - decoded, 'k');
title('Error Signal (Original - Decoded)');
xlabel('Time (s)'); ylabel('Difference');

sgtitle(['PSNR = ', num2str(psnrValue, '%.2f'), ' dB']);

% Delete the intermediate .wav file
delete(wavFile);
