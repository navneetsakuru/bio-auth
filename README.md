Multimodal Biometric Security System

This project presents a deep learning–based multimodal biometric authentication system that integrates fingerprint and iris recognition for secure and reliable user verification.

Overview
Traditional unimodal biometric systems suffer from limitations such as noise, spoofing attacks, and reduced accuracy. This project addresses these issues by combining fingerprint and iris biometrics. CNN-based feature extraction and biometric fusion are used to improve authentication performance. A Streamlit interface enables real-time enrollment and verification.

Key Features
- Multimodal authentication (Fingerprint + Iris)
- CNN-based feature extraction
- Biometric fusion
- Automatic modality classification
- Real-time enrollment and verification
- Streamlit-based user interface

System Architecture
Input → Preprocessing → CNN Feature Extraction → Feature Embedding → Fusion → Matching → Decision

Technologies Used
TensorFlow, Keras, Python, Streamlit, OpenCV, NumPy

Project Structure
biometric_app/
  streamlit_biometric.py
  pages/2_Access_portal.py
  models/modality_classifier.h5
  enroll_images/
  templates/
  requirements.txt

How to Run
pip install -r requirements.txt
streamlit run streamlit_biometric.py

Working
Enrollment: Upload fingerprint and iris → features extracted → stored as templates  
Verification: Upload query images → compared with templates → result displayed

Advantages
- Higher accuracy than unimodal systems
- Improved security
- Robust performance

Limitations
- Depends on image quality
- No liveness detection
- Limited dataset

Future Scope
- Feature-level fusion
- Liveness detection
- Larger datasets
- Performance metrics (FAR, FRR, EER)

Author
-Navneet Sakuru
