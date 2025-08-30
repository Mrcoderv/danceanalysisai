import pyttsx3
from math import atan2, degrees

# ---- Text-to-speech engine ----
engine = pyttsx3.init()
engine.setProperty("rate", 160)
engine.setProperty("volume", 1.0)

def speak(text):
    """Speaks a given text using TTS."""
    engine.say(text)
    engine.runAndWait()

def calculate_angle(a, b, c):
    """Returns angle (in degrees) between 3 points (landmarks a, b, c)."""
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    cx, cy = c.x, c.y
    angle = degrees(atan2(cy - by, cx - bx) - atan2(ay - by, ax - bx))
    return abs(angle)

