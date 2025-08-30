"""
Generate demo data for testing the dance analysis application
"""
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_demo_pose_data(num_frames=100):
    """Generate realistic demo pose data"""
    
    # Define some common dance moves
    dance_moves = [
        "Right Hand Up", "Left Hand Up", "Both Hands Up",
        "Right Knee Bent", "Left Knee Bent", 
        "Step Left", "Step Right",
        "Left Arm Rotation", "Right Arm Rotation"
    ]
    
    demo_data = []
    start_time = datetime.now()
    
    for frame in range(num_frames):
        # Simulate timestamp
        timestamp = start_time + timedelta(seconds=frame * 0.033)  # ~30 FPS
        
        # Randomly select moves (simulate detection)
        num_moves = random.choices([0, 1, 2, 3], weights=[0.3, 0.4, 0.2, 0.1])[0]
        detected_moves = random.sample(dance_moves, min(num_moves, len(dance_moves)))
        
        # Generate synthetic landmark data (33 landmarks for MediaPipe)
        landmarks = []
        for i in range(33):
            # Add some realistic variation and movement
            base_x = 0.5 + 0.1 * np.sin(frame * 0.1 + i * 0.2)
            base_y = 0.5 + 0.1 * np.cos(frame * 0.1 + i * 0.3)
            base_z = random.uniform(-0.1, 0.1)
            
            landmarks.append((
                max(0, min(1, base_x + random.uniform(-0.05, 0.05))),
                max(0, min(1, base_y + random.uniform(-0.05, 0.05))),
                base_z + random.uniform(-0.02, 0.02)
            ))
        
        demo_data.append({
            'frame': frame,
            'timestamp': timestamp.timestamp(),
            'moves': detected_moves,
            'landmarks': landmarks
        })
    
    return demo_data

def save_demo_data():
    """Save demo data to JSON file"""
    demo_data = generate_demo_pose_data(200)
    
    with open('demo_pose_data.json', 'w') as f:
        # Convert timestamps to strings for JSON serialization
        serializable_data = []
        for item in demo_data:
            serializable_item = item.copy()
            serializable_item['timestamp'] = str(datetime.fromtimestamp(item['timestamp']))
            serializable_data.append(serializable_item)
        
        json.dump(serializable_data, f, indent=2)
    
    print(f"Demo data saved to demo_pose_data.json ({len(demo_data)} frames)")
    
    # Also create a CSV version
    csv_data = []
    for item in demo_data:
        row = {
            'frame': item['frame'],
            'timestamp': item['timestamp'],
            'moves_detected': ', '.join(item['moves']),
            'num_moves': len(item['moves'])
        }
        
        # Add landmark coordinates
        for j, (x, y, z) in enumerate(item['landmarks']):
            row[f'landmark_{j}_x'] = x
            row[f'landmark_{j}_y'] = y
            row[f'landmark_{j}_z'] = z
        
        csv_data.append(row)
    
    df = pd.DataFrame(csv_data)
    df.to_csv('demo_pose_data.csv', index=False)
    print(f"Demo data also saved to demo_pose_data.csv")

if __name__ == "__main__":
    save_demo_data()
