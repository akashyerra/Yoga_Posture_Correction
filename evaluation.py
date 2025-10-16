def init():
    angles_dict = {
        "armpit_left": 0,
        "armpit_right": 1,
        "elbow_left": 2,
        "elbow_right": 3,
        "hip_left": 4,
        "hip_right": 5,
        "knee_left": 6,
        "knee_right": 7,
    }
    return angles_dict

joint_angle_connections = {
    "armpit_left": ((5, 7), (7, 11)),   
    "armpit_right": ((6, 8), (8, 12)), 

    "elbow_left": ((5, 7), (7, 9)),    
    "elbow_right": ((6, 8), (8, 10)),   

    "hip_left": ((6, 12), (12, 14)),    
    "hip_right": ((5, 11), (11, 13)),   

    "knee_left": ((11, 13), (13, 15)),  
    "knee_right": ((12, 14), (14, 16)), 
}


def error_margin(control, value, difficulty):
    deviation_map = {
        "beginner": 30,
        "intermediate": 20,
        "advance": 10
    }
    
    deviation = deviation_map.get(difficulty.lower(), 20)  # Default to intermediate if invalid input
    return control - deviation <= int(value) <= control + deviation


def check_joint(angles, joint_name, threshold, body_position, difficulty):
    angles_dict = init()
    joint_index = angles_dict[joint_name]
    
    if error_margin(threshold, angles[joint_index], difficulty):
        return None, joint_name  # Joint is correctly aligned

    if angles[joint_index] > threshold:
        feedback = f"Bring {' '.join(joint_name.split('_')[::-1])} closer to {body_position}."
    else:
        feedback = f"Put {' '.join(joint_name.split('_')[::-1])} further away from {body_position}."
    
    return feedback, None


def check_pose_angle(pose_index, angles, df, difficulty):
    result = []
    correct_joints = set()
    incorrect_joints = set()

    joints = [
        ("armpit_right", "body"),
        ("armpit_left", "body"),
        ("elbow_right", "arm"),
        ("elbow_left", "arm"),
        ("hip_right", "pelvis"),
        ("hip_left", "pelvis"),
        ("knee_right", "calf"),
        ("knee_left", "calf"),
    ]

    for joint, body_position in joints:
        threshold = int(df.loc[pose_index, joint])
        feedback, correct_joint = check_joint(angles, joint, threshold, body_position, difficulty)

        if feedback:
            result.append(feedback)
            incorrect_joints.add(joint_angle_connections[joint][0])
            incorrect_joints.add(joint_angle_connections[joint][1])
        else:
            correct_joints.add(joint_angle_connections[correct_joint][0])
            correct_joints.add(joint_angle_connections[correct_joint][1])

    if not result:
        return ["Great job! Your pose is perfectly aligned."], correct_joints, incorrect_joints

    return result, correct_joints, incorrect_joints
