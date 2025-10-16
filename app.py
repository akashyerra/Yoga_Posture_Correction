from flask import Flask, render_template, request, redirect, url_for, session, flash, Response, jsonify
from pymongo import MongoClient
import cv2
from time import time
import pickle as pk
import pandas as pd
from werkzeug.security import generate_password_hash
import multiprocessing as mtp
import tensorflow as tf
import numpy as np
from tabulate import tabulate 

from landmarks import extract_landmarks
from calc_angles import rangles
from evaluation import check_pose_angle

app = Flask(__name__)
app.secret_key = ## Your Secret Key Here ## 

client = MongoClient("## MongoDB Connection String ##") 


db = client['yoga_app']  # Database name
users_collection = db['users'] 

EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}

def init_cam():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cam.set(cv2.CAP_PROP_FOCUS, 360)
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 130)
    cam.set(cv2.CAP_PROP_SHARPNESS, 125)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cam


def get_pose_index(pose):
    names = {
        'Adho Mukha Svanasana': 0, 
        'Anjaneyasana': 1, 
        'Ardha Chandrasana': 2, 'Ardha Pincha Mayurasana': 3, 'Bitilasana': 4, 'Camatkarasana': 5, 'Halasana': 6, 'Hanumanasana': 7, 'Marjaryasana': 8, 'Navasana': 9, 'Parsva Virabhadrasana': 10, 'Paschimottanasana': 11, 'Phalakasana': 12, 'Setu Bandha Sarvangasana': 13, 'Sivasana': 14, 'Trikonasana': 15, 'Urdhva Dhanurasana': 16, 'Urdhva Mukha Svsnssana': 17, 'Ustrasana': 18, 'Utkata_Konasana': 19, 'Utthita Hasta Padangusthasana': 20, 'Utthita Parsvakonasana': 21, 'Vasisthasana': 22, 'Virabhadrasana One': 23, 'Virabhadrasana Three': 24, 'Virabhadrasana Two': 25, 'Vrksasana': 26
        }
    return int(names[pose])


def init_dicts():
    landmarks_points = {
        "nose": 0,
        'left_shoulder': 5, 'right_shoulder': 6,
        'left_elbow': 7, 'right_elbow': 8,
        'left_wrist': 9, 'right_wrist': 10,
        'left_hip': 11, 'right_hip': 12,
        'left_knee': 13, 'right_knee': 14,
        'left_ankle': 15, 'right_ankle': 16,
    }
    landmarks_points_array = {
        "left_shoulder": [], "right_shoulder": [],
        "left_elbow": [], "right_elbow": [],
        "left_wrist": [], "right_wrist": [],
        "left_hip": [], "right_hip": [],
        "left_knee": [], "right_knee": [],
        "left_ankle": [], "right_ankle": [],
    }
    col_names = []
    for i in range(len(landmarks_points.keys())):
        name = list(landmarks_points.keys())[i]
        col_names.append(name + "_x")
        col_names.append(name + "_y")
    cols = col_names.copy()
    return cols, landmarks_points_array


# engine = pyttsx4.init()


# def tts(tts_q):
#     while True:
#         objects = tts_q.get()
#         if objects is None:
#             break
#         message = objects[0]
#         engine.say(message)
#         engine.runAndWait()
#     tts_q.task_done()


def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 4, (0,255,0), -1)

def draw_connections(frame, keypoints, edges, confidence_threshold, correct_joints, incorrect_joints):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))
    
    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]
        
        if (c1 > confidence_threshold) & (c2 > confidence_threshold):
            if edge in correct_joints:
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 2)
            elif edge in incorrect_joints:
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0,0,255), 2)
            else:    
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (182,93,27), 2)

def destory(cam, tts_proc, tts_q):
    cv2.destroyAllWindows()
    cam.release()
    tts_q.put(None)
    tts_q.close()
    tts_q.join_thread()
    tts_proc.join()

interpreter = tf.lite.Interpreter(model_path="models/t_3.tflite")
interpreter.allocate_tensors()

# tts_q = JoinableQueue()
# Start TTS Process
# tts_proc = Process(target=tts, args=(tts_q, ))
# tts_proc.start()

# Timing for putting text in the queue
# tts_last_exec = time() + 5


latest_feedback = {"message": "No feedback yet"}

def analyze_frames(pose, difficulty):
    global latest_feedback
    cam = init_cam()
    cols, landmarks_points_array = init_dicts()
    # angles_df = pd.read_csv("./csv_files/4_angles_poses_angles.csv")
    angles_df = pd.read_csv("angles_classwise_avg.csv")
    

    # tts_q = mtp.JoinableQueue()

    # tts_proc = mtp.Process(target=tts, args=(tts_q, ))
    # tts_proc.start()

    # tts_last_exec = time() + 5

    
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        

        key = cv2.waitKey(1)
        if key == ord("q"):
            # destory(cam, tts_proc, tts_q)
            break

        if ret:
            err, df, landmarks = extract_landmarks(
                frame,
                interpreter,
                cols
            )

            if err == False:
                # print(landmarks)
                draw_keypoints(frame, landmarks, 0.4)
                
                # print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

                angles = rangles(df, landmarks_points_array)
                position = get_pose_index(pose)
                suggestions, correct_joints, incorrect_joints = check_pose_angle(position, angles, angles_df, difficulty)
                
                draw_connections(frame, landmarks, EDGES, 0.4, correct_joints, incorrect_joints)

                
                latest_feedback['message'] = suggestions[0]

                # if time() > tts_last_exec:
                #     tts_q.put([
                #         suggestions[0]
                #     ])
                #     tts_last_exec = time() + 5
                
                
            flipped = cv2.flip(frame, 1)

            # Reshape image
            img = flipped.copy()
            # cv2.imshow("Yoga Pose Analysis", img)
            ret, buffer = cv2.imencode('.jpg', img)
            img = buffer.tobytes()

            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')


# def tts(tts_q):
#     """
#     Simulated TTS Function:
#     Continuously puts audio data in the queue.
#     Replace this with your actual TTS logic.
#     """
#     while True:
#         if not tts_q.empty():
#             text = tts_q.get()
#             # Simulate audio data generation (replace with real TTS output)
#             audio_data = text.encode()  # This is a placeholder
#             tts_q.task_done()
#             yield audio_data
#         else:
#             time.sleep(0.1)  # Small delay when there's no data

# def audio_stream():
#     global tts_last_exec

#     # Continuously stream audio data
#     while True:
#         # Check if it's time to generate TTS for new text
#         if time() > tts_last_exec:
#             tts_q.put(['This is a sample feedback message'])  # Example text
#             tts_last_exec = time() + 5
        
#         # Get audio data from the queue and stream it
#         if not tts_q.empty():
#             audio_data = tts_q.get()
#             tts_q.task_done()
#             yield audio_data
#         else:
#             time.sleep(0.1)


# @app.route('/stream-audio')
# def stream_audio():
#     return Response(audio_stream(), mimetype='audio/mpeg')

# @app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in MongoDB
        user = users_collection.find_one({'email': email})

        if user and user['password'] == password:
            session['user'] = email  # Store user email in session
            return redirect(url_for('home'))  # Redirect to home page
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        experience = request.form['experience']

        # Check if the email is already registered
        if users_collection.find_one({'email': email}):
            flash('Email already registered. Please login.', 'error')
            
            return redirect(url_for('login'))

        # Save user data to MongoDB
        user_data = {
            'name': name,
            'email': email,
            'password': password,
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'experience': experience
        }
        users_collection.insert_one(user_data)

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

try:
    # Try to fetch database names (ensures connection is successful)
    client.list_database_names()
    print("✅ MongoDB Connected Successfully!")  # Message will appear in the terminal
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)  # Error message

# Route for the home page
@app.route('/')
def home():
    # Check if the user is logged in
    if 'user' not in session:
        flash('Please login to access the home page.', 'error')
        return redirect(url_for('login'))
    
    # Retrieve the user's difficulty level from the database
    user_email = session['user']
    user = users_collection.find_one({'email': user_email})
    difficulty = user.get('experience', 'beginner')  # Default to 'beginner' if not found

    return render_template('homepage.html', difficulty=difficulty)

# Route for logout
@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear the session
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/index')
def index():
    pose = request.args.get('pose')
    difficulty = request.args.get('difficulty')
    if pose and difficulty:
        session['pose'] = pose
        session['difficulty'] = difficulty
    
    pose_image = f"/Images/{pose.replace(' ', '_')}/image.jpeg"
    return render_template('index.html', pose=pose, pose_image=pose_image)

@app.route('/video')
def video():
    pose = session.get('pose')
    difficulty = session.get('difficulty')
    if pose and difficulty:
        print(f"Pose: {pose}, Difficulty: {difficulty}")
    return Response(analyze_frames(pose, difficulty), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/feedback')
def feedback():
    return jsonify(latest_feedback)
    # return jsonify({"message": "Great job! Your pose is perfectly aligned."})
    

if __name__ == "__main__":
    app.run(debug=True)