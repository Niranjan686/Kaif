import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import webbrowser
import os

# 🔧 Disable OneDNN Optimization for TensorFlow Stability
def spotify():

    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

    # ✅ Load Model and Labels
    try:
        model = tf.keras.models.load_model("model.h5")
        label = np.load("labels.npy", allow_pickle=True)
        if label is None or not isinstance(label, np.ndarray) or len(label) == 0:
            raise ValueError("labels.npy is empty or invalid!")
    except Exception as e:
        st.error(f"Error loading model or labels: {e}")
        st.stop()

    # ✅ Initialize Mediapipe Modules
    holistic = mp.solutions.holistic
    holis = holistic.Holistic()
    drawing = mp.solutions.drawing_utils

    st.header("🎵 Emotion-Based Spotify Music Recommender")

    # ✅ Check and Load Emotion Data
    if "run" not in st.session_state:
        st.session_state["run"] = True

    try:
        emotion = np.load("emotion.npy", allow_pickle=True)[0]
    except FileNotFoundError:
        emotion = ""

    # 🎥 OpenCV Video Capture
    cap = cv2.VideoCapture(0)

    def process_emotion(frame):
        frame = cv2.flip(frame, 1)  # Mirror effect
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with Mediapipe
        res = holis.process(rgb_frame)
        lst = []

        if res.face_landmarks:
            for i in res.face_landmarks.landmark:
                lst.append(i.x - res.face_landmarks.landmark[1].x)
                lst.append(i.y - res.face_landmarks.landmark[1].y)

            # Process left hand landmarks
            if res.left_hand_landmarks:
                for i in res.left_hand_landmarks.landmark:
                    lst.append(i.x - res.left_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.left_hand_landmarks.landmark[8].y)
            else:
                lst.extend([0.0] * 42)  # Padding if no left hand detected

            # Process right hand landmarks
            if res.right_hand_landmarks:
                for i in res.right_hand_landmarks.landmark:
                    lst.append(i.x - res.right_hand_landmarks.landmark[8].x)
                    lst.append(i.y - res.right_hand_landmarks.landmark[8].y)
            else:
                lst.extend([0.0] * 42)  # Padding if no right hand detected

            # 🔥 Predict Emotion
            lst = np.array(lst).reshape(1, -1)

            if lst.shape[1] > 0:
                predictions = model.predict(lst)
                pred = label[np.argmax(predictions)]
                cv2.putText(frame, pred, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Save emotion
                np.save("emotion.npy", np.array([pred]))
                return frame, pred

        # Reset emotion if no face detected
        np.save("emotion.npy", np.array([""]))
        return frame, None

    # 🎥 Display Live Video
    lang = st.text_input("🌍 Enter Language")
    singer = st.text_input("🎤 Enter Singer Name")

    frame_placeholder = st.empty()

    if lang and singer:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Error: Could not access the camera!")
                break

            frame, detected_emotion = process_emotion(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            frame_placeholder.image(frame, channels="RGB")  # Display in Streamlit

            if detected_emotion:
                st.session_state["run"] = False
                break  # Exit loop when emotion is detected

    cap.release()
    cv2.destroyAllWindows()

    # 🎵 Recommendation Button
    btn = st.button("🎶 Recommend me songs")

    if btn:
        if not emotion:
            st.warning("⚠ Please let me capture your emotion first")
            st.session_state["run"] = True
        else:
            # 🔗 Open YouTube with Emotion-Based Search
            query = f"{lang} {emotion} song {singer}"
            webbrowser.open(f"https://open.spotify.com/search/query={lang}+{emotion}+song+{singer}")
            #webbrowser.open(youtube_url)

            # Reset Emotion
            np.save("emotion.npy", np.array([""]))
            st.session_state["run"] = False
spotify()