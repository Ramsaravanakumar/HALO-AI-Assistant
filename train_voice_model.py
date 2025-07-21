import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import librosa
from sklearn.svm import SVC
import joblib

def record_voice(filename):
    print(f"Recording: {filename}")
    fs = 44100
    duration = 3
    print("Speak now...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    print(f"Saved: {filename}")

def extract_features(file):
    audio, sr = librosa.load(file)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)

# Record samples
samples = ["ram1.wav", "ram2.wav", "other1.wav", "other2.wav"]
for sample in samples:
    record_voice(sample)

# Prepare training data
X = [extract_features(f) for f in samples]
y = [1, 1, 0, 0]

# Train and save model
model = SVC(probability=True)
model.fit(X, y)
joblib.dump(model, "voice_authentication_model.pkl")
print("✅ Model trained and saved.")
