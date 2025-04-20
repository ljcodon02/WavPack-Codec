% Load the audio file
[audio_signal, Fs] = audioread('Datacompression.wav');

%% 1. Time domain analysis of the full signal
figure;
t_full = (0:length(audio_signal)-1)/Fs; % Time vector in seconds
plot(t_full, audio_signal);
xlabel('Time (s)');
ylabel('Amplitude');
title('Full Waveform in Time Domain');
grid on;

%% 2. Truncate signal to first 20 seconds and plot
% Calculate number of samples for 20 seconds
samples_20sec = min(20 * Fs, length(audio_signal));
truncated_signal = audio_signal(1:samples_20sec);
t_truncated = (0:samples_20sec-1)/Fs; % Time vector for truncated signal

figure;
plot(t_truncated, truncated_signal);
xlabel('Time (s)');
ylabel('Amplitude');
title('First 20 Seconds of Audio Signal');
grid on;

%% 3. FFT and Power Spectrum
N = length(truncated_signal);

% Compute the FFT
Y = fft(truncated_signal);

% Compute frequency axis (in Hz)
f = (0:N-1)*(Fs/N);

% Compute power spectrum
power_spectrum = (abs(Y).^2)/N;

%Power spectrum - human voice range (log scale)
figure;
voice_range_indices = find(f >= 80 & f <= 3500);
plot(f(voice_range_indices), power_spectrum(voice_range_indices));
xlabel('Frequency (Hz)');
ylabel('Power');
title('Power Spectrum');
grid on;

%% 4. Single-sided spectrum (positive frequencies only)
% For a real signal, we only need the first half of the spectrum
N_half = ceil(N/2);
f_single = f(1:N_half); % Positive frequencies only

% Single-sided magnitude spectrum (multiply by 2 to conserve energy, except DC component)
magnitude_single = abs(Y(1:N_half))/N;
magnitude_single(2:end) = 2*magnitude_single(2:end);

figure;
plot(f_single, magnitude_single);
xlabel('Frequency (Hz)');
ylabel('Magnitude');
title('Single-Sided Magnitude Spectrum');
grid on;
xlim([0 5000]); % Limit x-axis for better visualization of speech frequencies

%% 5. PSD Estimation using three different methods

% Method 1: PSD computed directly from FFT
psd_direct = power_spectrum;
psd_direct_half = psd_direct(1:N_half);
psd_direct_half(2:end) = 2*psd_direct_half(2:end); % Multiply by 2 (except DC)

figure;
plot(f_single, 10*log10(psd_direct_half));
xlabel('Frequency (Hz)');
ylabel('Power/Frequency (dB/Hz)');
title('PSD Directly from FFT');
grid on;
xlim([0 5000]);

% Method 2: Periodogram-based PSD estimate
[pxx_periodogram, f_periodogram] = periodogram(truncated_signal, [], [], Fs);

figure;
plot(f_periodogram, 10*log10(pxx_periodogram));
xlabel('Frequency (Hz)');
ylabel('Power/Frequency (dB/Hz)');
title('Periodogram-based PSD Estimate');
grid on;
xlim([0 5000]);

