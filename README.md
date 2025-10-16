# Yoga Posture Correction

## About the Project

This is an intelligent yoga posture correction system that uses computer vision and machine learning to help users practice yoga correctly. The system can:
- Detect and track human body landmarks in real-time using webcam
- Analyze yoga poses by calculating joint angles
- Compare user's pose with standard poses
- Provide real-time feedback and recommendations for pose corrections
- Support multiple yoga poses (27 different asanas)
- Track user progress through a web interface

## Technologies Used

- **Frontend**:
  - HTML/CSS/JavaScript
  - Flask templates
  - Bootstrap for responsive design

- **Backend**:
  - Python 3.10
  - Flask web framework
  - MongoDB for user data storage
  - OpenCV for image processing
  - TensorFlow Lite for pose detection
  - NumPy and Pandas for data analysis

- **Machine Learning**:
  - MoveNet model for pose estimation
  - TensorFlow Lite for model deployment
  - Custom angle-based pose evaluation system

## Uses of the Project

1. **Personal Yoga Practice**:
   - Practice yoga at home with real-time feedback
   - Get instant corrections for improper postures
   - Track progress over time

2. **Yoga Education**:
   - Learn new yoga poses with proper alignment
   - Understand common mistakes in different poses
   - Visual feedback for better learning

3. **Health and Wellness**:
   - Prevent injuries from incorrect pose execution
   - Improve flexibility and strength safely
   - Monitor progress in pose accuracy

## Setup Instructions

1. **Prerequisites**:
   - Python 3.10 or higher
   - Webcam
   - MongoDB installed and running
   - Git (for cloning the repository)

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/akashyerra/Yoga_Posture_Correction.git
   cd Yoga_Posture_Correction
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Model Setup**:
   - Create a `models` directory in the project root
   - Download the MoveNet TFLite model
   - Place the model file as `models/t_3.tflite`

5. **Dataset Setup**:
   - The project uses a custom yoga poses dataset
   - Download the dataset from Kaggle or use your own dataset
   - Place the images in the following structure:
     ```
     poses_dataset/
     └── Dataset/
         ├── Adho Mukha Svanasana/
         ├── Anjaneyasana/
         └── ... (other pose folders)
     ```

6. **Environment Configuration**:
   - Create a MongoDB database named `yoga_app`
   - Update the MongoDB connection string in `app.py`
   - Set the Flask secret key in `app.py`

7. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`

## Features

- Real-time pose detection and analysis
- Support for 27 different yoga poses
- User authentication and progress tracking
- Detailed angle-based pose evaluation
- Visual feedback with skeleton overlay
- Timer functionality for pose holding
- Responsive web interface

## Supported Yoga Poses

The system currently supports the following poses:
1. Adho Mukha Svanasana (Downward-Facing Dog)
2. Anjaneyasana (Low Lunge)
3. Ardha Chandrasana (Half Moon)
4. Ardha Pincha Mayurasana
5. Bitilasana (Cow Pose)
6. Camatkarasana
7. Halasana (Plow Pose)
8. Hanumanasana (Splits)
9. Marjaryasana (Cat Pose)
10. Navasana (Boat Pose)
11. Parsva Virabhadrasana
12. Paschimottanasana (Seated Forward Bend)
13. Phalakasana (Plank Pose)
14. Setu Bandha Sarvangasana (Bridge Pose)
15. Sivasana (Corpse Pose)
16. Trikonasana (Triangle Pose)
17. Urdhva Dhanurasana (Wheel Pose)
18. Urdhva Mukha Svanasana (Upward-Facing Dog)
19. Ustrasana (Camel Pose)
20. Utkata Konasana (Goddess Pose)
21. Utthita Hasta Padangusthasana
22. Utthita Parsvakonasana (Extended Side Angle)
23. Vasisthasana (Side Plank)
24. Virabhadrasana I (Warrior I)
25. Virabhadrasana II (Warrior II)
26. Virabhadrasana III (Warrior III)
27. Vrksasana (Tree Pose)