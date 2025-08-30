import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import pygame
import tempfile
import os
from datetime import datetime
import pandas as pd
import time
import math

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize pygame mixer for audio
pygame.mixer.init()

# Page configuration
st.set_page_config(
    page_title="AI Dance Analysis Studio",
    page_icon="💃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Import DM Sans font */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
    
    /* Global styles */
    .main {
        background: linear-gradient(135deg, #fefce8 0%, #ecfeff 100%);
        font-family: 'DM Sans', sans-serif;
    }
    
    /* Header styles */
    .hero-header {
        background: linear-gradient(135deg, #d97706 0%, #6366f1 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Card styles */
    .dance-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 2px solid transparent;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .dance-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #d97706;
    }
    
    .dance-card.selected {
        border-color: #d97706;
        background: linear-gradient(135deg, #fef3c7 0%, #fefce8 100%);
    }
    
    /* Style selection cards */
    .style-card {
        background: white;
        padding: 1rem;
        border-radius: 0.75rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #e5e7eb;
        margin: 0.5rem;
    }
    
    .style-card:hover {
        border-color: #6366f1;
        transform: scale(1.02);
    }
    
    .style-card.selected {
        border-color: #d97706;
        background: linear-gradient(135deg, #fef3c7 0%, #fefce8 100%);
    }
    
    .style-emoji {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .style-name {
        font-weight: 600;
        color: #374151;
    }
    
    /* Metrics */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.75rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #d97706;
    }
    
    .metric-label {
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed #d97706;
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        background: white;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        background: #fef3c7;
        border-color: #92400e;
    }
    
    /* Buttons */
    .primary-button {
        background: linear-gradient(135deg, #d97706 0%, #92400e 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .primary-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(217, 119, 6, 0.3);
    }
    
    .secondary-button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.5rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .secondary-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    
    /* Status indicators */
    .status-success {
        color: #10b981;
        font-weight: 600;
    }
    
    .status-warning {
        color: #f59e0b;
        font-weight: 600;
    }
    
    .status-error {
        color: #ef4444;
        font-weight: 600;
    }
    
    /* Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Dance styles configuration
DANCE_STYLES = {
    "Hip Hop": {
        "emoji": "🎤",
        "description": "Urban street dance with strong beats",
        "characteristics": ["High energy", "Sharp movements", "Rhythm focus"],
        "move_threshold": 0.15,
        "energy_multiplier": 1.2
    },
    "Ballet": {
        "emoji": "🩰",
        "description": "Classical dance with graceful movements",
        "characteristics": ["Graceful", "Controlled", "Precise"],
        "move_threshold": 0.08,
        "energy_multiplier": 0.8
    },
    "Contemporary": {
        "emoji": "🌊",
        "description": "Modern expressive dance style",
        "characteristics": ["Fluid", "Expressive", "Creative"],
        "move_threshold": 0.12,
        "energy_multiplier": 1.0
    },
    "Latin": {
        "emoji": "💃",
        "description": "Passionate Latin American dances",
        "characteristics": ["Passionate", "Rhythmic", "Energetic"],
        "move_threshold": 0.18,
        "energy_multiplier": 1.3
    },
    "Bhajan Nepali": {
        "emoji": "🙏",
        "description": "Traditional Nepali devotional dance",
        "characteristics": ["Spiritual", "Traditional", "Meditative"],
        "move_threshold": 0.10,
        "energy_multiplier": 0.9
    }
}

class DanceAnalyzer:
    def __init__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.previous_landmarks = None
        self.movement_history = []
        self.move_count = 0
        self.session_start = time.time()
        
    def calculate_movement_energy(self, landmarks):
        """Calculate movement energy based on landmark changes"""
        if self.previous_landmarks is None:
            self.previous_landmarks = landmarks
            return 0
        
        total_movement = 0
        key_points = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]  # Key body points
        
        for i in key_points:
            if i < len(landmarks) and i < len(self.previous_landmarks):
                curr = landmarks[i]
                prev = self.previous_landmarks[i]
                movement = math.sqrt(
                    (curr.x - prev.x)**2 + 
                    (curr.y - prev.y)**2 + 
                    (curr.z - prev.z)**2
                )
                total_movement += movement
        
        self.previous_landmarks = landmarks
        return total_movement
    
    def detect_dance_moves(self, landmarks, style_config):
        """Detect dance moves based on movement patterns"""
        energy = self.calculate_movement_energy(landmarks)
        self.movement_history.append(energy)
        
        # Keep only recent history
        if len(self.movement_history) > 30:
            self.movement_history.pop(0)
        
        # Detect moves based on energy spikes
        if len(self.movement_history) >= 5:
            recent_avg = sum(self.movement_history[-5:]) / 5
            if recent_avg > style_config["move_threshold"]:
                self.move_count += 1
                return True
        
        return False
    
    def get_performance_metrics(self, style_config):
        """Calculate performance metrics"""
        session_duration = time.time() - self.session_start
        
        if session_duration > 0:
            moves_per_minute = (self.move_count / session_duration) * 60
            avg_energy = sum(self.movement_history) / len(self.movement_history) if self.movement_history else 0
            
            # Style-specific scoring
            energy_score = min(100, avg_energy * style_config["energy_multiplier"] * 1000)
            rhythm_score = min(100, moves_per_minute * 2)
            
            return {
                "moves_per_minute": round(moves_per_minute, 1),
                "average_energy": round(avg_energy * 1000, 2),
                "energy_score": round(energy_score, 1),
                "rhythm_score": round(rhythm_score, 1),
                "total_moves": self.move_count,
                "session_duration": round(session_duration, 1)
            }
        
        return {
            "moves_per_minute": 0,
            "average_energy": 0,
            "energy_score": 0,
            "rhythm_score": 0,
            "total_moves": 0,
            "session_duration": 0
        }

def draw_pose_landmarks(image, landmarks):
    """Draw pose landmarks on image"""
    if landmarks:
        # Draw connections
        connections = [
            (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),  # Arms
            (11, 23), (12, 24), (23, 24),  # Torso
            (23, 25), (25, 27), (24, 26), (26, 28),  # Legs
        ]
        
        h, w = image.shape[:2]
        
        # Draw connections
        for connection in connections:
            if connection[0] < len(landmarks) and connection[1] < len(landmarks):
                start_point = landmarks[connection[0]]
                end_point = landmarks[connection[1]]
                
                if start_point.visibility > 0.5 and end_point.visibility > 0.5:
                    start_pos = (int(start_point.x * w), int(start_point.y * h))
                    end_pos = (int(end_point.x * w), int(end_point.y * h))
                    cv2.line(image, start_pos, end_pos, (0, 255, 0), 3)
        
        # Draw landmarks
        for i, landmark in enumerate(landmarks):
            if landmark.visibility > 0.5:
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                confidence_color = (0, int(255 * landmark.visibility), int(255 * (1 - landmark.visibility)))
                cv2.circle(image, (x, y), 5, confidence_color, -1)
    
    return image

def main():
    # Initialize session state
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = DanceAnalyzer()
    if 'selected_style' not in st.session_state:
        st.session_state.selected_style = "Hip Hop"
    if 'music_playing' not in st.session_state:
        st.session_state.music_playing = False
    if 'uploaded_music' not in st.session_state:
        st.session_state.uploaded_music = None
    
    # Hero Header
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">AI Dance Analysis Studio</div>
        <div class="hero-subtitle">Upload your music, select your style, and let AI analyze your dance moves</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎵 Music Upload")
        
        # Music upload
        uploaded_file = st.file_uploader(
            "Choose your music file",
            type=['mp3', 'wav', 'ogg'],
            help="Upload MP3, WAV, or OGG files"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_music = uploaded_file
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_path = tmp_file.name
            
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            
            # Music controls
            col1, col2 = st.columns(2)
            with col1:
                if st.button("▶️ Play", key="play_btn"):
                    try:
                        pygame.mixer.music.load(temp_path)
                        pygame.mixer.music.play(-1)  # Loop indefinitely
                        st.session_state.music_playing = True
                        st.success("🎵 Music playing!")
                    except Exception as e:
                        st.error(f"Error playing music: {e}")
            
            with col2:
                if st.button("⏹️ Stop", key="stop_btn"):
                    pygame.mixer.music.stop()
                    st.session_state.music_playing = False
                    st.info("🔇 Music stopped")
        
        st.markdown("---")
        
        # Dance style selection
        st.markdown("### 💃 Select Dance Style")
        
        for style_name, style_info in DANCE_STYLES.items():
            is_selected = st.session_state.selected_style == style_name
            
            if st.button(
                f"{style_info['emoji']} {style_name}",
                key=f"style_{style_name}",
                help=style_info['description']
            ):
                st.session_state.selected_style = style_name
                st.session_state.analyzer = DanceAnalyzer()  # Reset analyzer
        
        # Show selected style info
        if st.session_state.selected_style:
            style_info = DANCE_STYLES[st.session_state.selected_style]
            st.markdown(f"""
            <div class="dance-card selected">
                <div style="text-align: center; font-size: 2rem;">{style_info['emoji']}</div>
                <h4>{st.session_state.selected_style}</h4>
                <p>{style_info['description']}</p>
                <div style="font-size: 0.9rem; color: #6b7280;">
                    <strong>Characteristics:</strong><br>
                    {' • '.join(style_info['characteristics'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📹 Live Dance Analysis")
        
        # Camera input
        camera_input = st.camera_input("Start dancing!", key="dance_camera")
        
        if camera_input is not None:
            # Process the image
            image = cv2.imdecode(np.frombuffer(camera_input.getvalue(), np.uint8), cv2.IMREAD_COLOR)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Pose detection
            results = st.session_state.analyzer.pose.process(image_rgb)
            
            if results.pose_landmarks:
                # Draw pose landmarks
                annotated_image = draw_pose_landmarks(image.copy(), results.pose_landmarks.landmark)
                
                # Detect moves
                style_config = DANCE_STYLES[st.session_state.selected_style]
                move_detected = st.session_state.analyzer.detect_dance_moves(
                    results.pose_landmarks.landmark, 
                    style_config
                )
                
                # Show annotated image
                st.image(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB), caption="Pose Detection")
                
                if move_detected:
                    st.success("🔥 Great move detected!")
            else:
                st.image(image, caption="No pose detected")
                st.warning("⚠️ No pose detected. Make sure you're visible in the camera.")
    
    with col2:
        st.markdown("### 📊 Performance Metrics")
        
        # Get current metrics
        style_config = DANCE_STYLES[st.session_state.selected_style]
        metrics = st.session_state.analyzer.get_performance_metrics(style_config)
        
        # Display metrics
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['total_moves']}</div>
            <div class="metric-label">Total Moves</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['moves_per_minute']}</div>
            <div class="metric-label">Moves/Minute</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['energy_score']}%</div>
            <div class="metric-label">Energy Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['rhythm_score']}%</div>
            <div class="metric-label">Rhythm Score</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Session info
        st.markdown("### ⏱️ Session Info")
        st.info(f"Duration: {metrics['session_duration']}s")
        st.info(f"Style: {st.session_state.selected_style}")
        
        if st.session_state.music_playing:
            st.success("🎵 Music: Playing")
        else:
            st.warning("🔇 Music: Stopped")
        
        # Export data
        if st.button("📥 Export Session Data"):
            session_data = {
                "timestamp": datetime.now().isoformat(),
                "dance_style": st.session_state.selected_style,
                "total_moves": metrics['total_moves'],
                "session_duration": metrics['session_duration'],
                "moves_per_minute": metrics['moves_per_minute'],
                "energy_score": metrics['energy_score'],
                "rhythm_score": metrics['rhythm_score']
            }
            
            df = pd.DataFrame([session_data])
            csv = df.to_csv(index=False)
            
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"dance_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
