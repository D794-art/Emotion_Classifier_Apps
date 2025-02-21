import joblib
# Saving a model
joblib.dump(pipe_lr, 'emotion_classifier_pipe_lr_with_new_emotions.pkl')
# Loading a model
model = joblib.load('emotion_classifier_pipe_lr_with_new_emotions.pkl')
