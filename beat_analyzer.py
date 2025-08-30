import librosa

STYLE_SONGS = {
    'bhajan': 'songfolder/NepaliVajan.mp3',
    'bollywood': 'songfolder/BollywoodSong.mp3',
    'bhojpuri': 'songfolder/BhojpuriSong.mp3',
    'pop': 'songfolder/PopSong.mp3',
    'hiphop': 'songfolder/HipHopSong.mp3',
}

def analyze_beats(song_path):
    """
    Returns tempo (BPM) and list of beat timestamps (in seconds).
    """
    y, sr = librosa.load(song_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return float(tempo), beat_times.tolist()

if __name__ == "__main__":
    print("Select dance style for beat analysis:")
    style_options = list(STYLE_SONGS.keys())
    for i, s in enumerate(style_options):
        print(f"  {i+1}: {s}")
    while True:
        try:
            style_idx = int(input("Enter style number (1-5): ")) - 1
            if 0 <= style_idx < len(style_options):
                style = style_options[style_idx]
                break
            else:
                print("Invalid option. Try again.")
        except Exception:
            print("Invalid input. Enter a number 1-5.")
    song_path = STYLE_SONGS[style]
    print(f"Analyzing beats for {style} song: {song_path}")
    tempo, beat_times = analyze_beats(song_path)
    print(f"Detected Tempo: {tempo:.2f} BPM")
    print(f"Total Beats: {len(beat_times)}")
    # Save beat data for tracker
    import json
    with open("beat_data.json", "w") as f:
        json.dump({"style": style, "song": song_path, "tempo": tempo, "beats": beat_times}, f, indent=2)
    print("Beat data saved to beat_data.json. Now run the tracker.")
