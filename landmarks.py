import cv2
import numpy as np
import pandas as pd
import tensorflow as tf


def extract_landmarks(image, interpreter, cols):
    pre_list = []
    
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (256, 256))  # MoveNet requires 256x256 input
    img_expanded = np.expand_dims(img_resized.astype(np.float32), axis=0)
    
    # Setup input and output
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Make predictions
    interpreter.set_tensor(input_details[0]['index'], img_expanded)
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])[0, 0]
    
    try:
        for keypoint in keypoints_with_scores:
            x, y, score = keypoint[:3]
            pre_list.append((x, y, score))
        predict = True
    except AttributeError:
        return True, pd.DataFrame(), None
    
    if predict:
        gen0510 = np.array([
            [pre_list[m][0], pre_list[m][1]] for m in range(5, 11)
        ]).flatten().tolist()
        
        gen1116 = np.array([
            [pre_list[m][0], pre_list[m][1]] for m in range(11, 17)
        ]).flatten().tolist()
        
        gen0510.extend(gen1116)
        
        all_list = [pre_list[0][0], pre_list[0][1]]
        all_list.extend(gen0510)
        
        return False, pd.DataFrame([all_list], columns=cols), keypoints_with_scores