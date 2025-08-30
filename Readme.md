# 🕺 AI Dance Tutor with Beat Synchronization

This project is an **AI-powered Dance Tutor** that uses your webcam to track body movements, syncs with the **beats of a song**, and gives **step-by-step dance instructions** in real time.

## Features
- 🎥 **Pose tracking** (MediaPipe & OpenCV)
- 🎶 **Beat analysis** (Librosa)
- 🔊 **Audio playback & speech instructions** (playsound + pyttsx3)
- 📝 **Data recording** (landmark CSV file for later analysis)

---

## 📂 Project Structure

```
dance-tutor/
├── dance_tracker.py           # Main program (tracks body & gives instructions)
├── dance_instructions.py      # Dance step logic & instructions
├── beat_analysis.py           # Beat & tempo detection using librosa
├── utils.py                   # Helper functions (angle calculation & TTS)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── song.mp3                   # Your dance song (place here)
├── dance_tracking_data.csv    # Generated output after running
```

---

## ⚙️ Installation

### 1. Clone the project or copy files

```bash
git clone https://github.com/mrcoderv/danceanalyseai.git
cd dance-tutor
```

### 2. Install dependencies

Make sure you have Python 3.8+.

```bash
pip install -r requirements.txt
```

### 3. Add a song

Put your dance song in the project folder as:

```
song.mp3
```

---

## ▶️ Running the Program

Run the main script:

```bash
python dance_tracker.py
```

### Controls
- Press `q` → Quit the program.

The webcam window will open showing your skeleton pose.

On each beat of the song, the program will:
- Highlight **"🎵 On Beat! 🎵"** on screen.
- Give dance instructions (e.g., “Raise your right hand”, “Step left”).

---

## 📊 Output

### Real-time display
- Webcam feed with body landmarks
- Beat markers & instructions overlayed

### CSV File (`dance_tracking_data.csv`)
Records body landmarks for each frame:

```
frame, x_0, y_0, z_0, visibility_0, x_1, y_1, ...
1, 0.45, 0.23, -0.12, 0.99, ...
2, ...
```

### Voice instructions
Uses pyttsx3 to speak dance moves in sync with music.

---

## 🎶 How Beat-Synced Dance Works

- `beat_analysis.py` detects tempo (BPM) and beat timestamps.
- While the song plays, the program checks if the current time ≈ beat time.
- If yes → shows "On Beat!" and triggers a dance instruction.
- Instructions cycle across beats to create a choreography.

---

## 📋 Dependencies

Installed automatically from `requirements.txt`:


- `opencv-python` → webcam video & drawing
- `mediapipe` → pose tracking (33 landmarks)
- `playsound` → music playback
- `pyttsx3` → text-to-speech instructions
- `librosa` → beat/tempo analysis

---

## 🚀 Possible Extensions

- Map specific steps to specific beats (choreography timeline)
- Add scoring system → compare user’s moves with reference moves
- Visualize dance history (charts of accuracy)
- Multiplayer dance battles 🎉

---

## 📝 License

MIT License. Free to use & modify.