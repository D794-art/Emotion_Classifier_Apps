import streamlit as st
import altair as alt
import pandas as pd
import joblib
from datetime import datetime
from track_utils import add_page_visited_details, view_all_page_visited_details, add_prediction_details, view_all_prediction_details


pipe_lr = joblib.load("emotion_classifier_pipe_lr_with_new_emotions.pkl")

emotions_emoji_dict = {
    "anger": "😠", 
    "disgust": "🤮", 
    "fear": "😨😱", 
    "joy": "😂", 
    "sadness": "😔", 
    "neutral": "😐", 
    "shame": "😳", 
    "surprise": "😮",
    "anxiety": "😰",
    "envy": "😒",
    "embarrassment": "😳",
    "boredom": "😴"
}

import os

images_dict = {
    "joy": "images/joy.png",
    "sadness": "images/sadness.png",
    "anger": "images/anger.png",
    "fear": "images/fear.png",
    "disgust": "images/disgust.png",
    "neutral": "images/neutral.png",
    "shame": "images/embarrassment.png",
    "surprise": "images/joy.png",
    "anxiety": "images/anxiety.png",
    "envy": "images/jelous.png",
    "embarrassment": "images/embarrassment.png",
    "boredom": "images/boredom.png"
}

def display_image(prediction):
    image_file = images_dict.get(prediction)
    if image_file and os.path.exists(image_file):  
        st.image(image_file, caption=f"Emotion: {prediction} {emotions_emoji_dict[prediction]}",  use_container_width=True)
    else:
        st.warning(f"Image for {prediction} not found!")

# Prediction function
def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]

def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results

# Streamlit main app
def main():
    st.title("Emotion Classifier App")
    menu = ["Home", "Monitor", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    # Track page visit with current timestamp
    add_page_visited_details(choice, datetime.now())

    if choice == "Home":
        st.subheader("Inside Out Emotions: Analyzing Text Sentiments")
        with st.form(key='emotion_clf_form'):
            raw_text = st.text_area("Type Here")
            submit_text = st.form_submit_button(label='Submit')

        if submit_text:
            # Predict Emotion
            prediction = predict_emotions(raw_text)
            probability = get_prediction_proba(raw_text)
            add_prediction_details(raw_text, prediction, max(probability[0]), datetime.now())

            col1, col2 = st.columns(2)

            with col1:
                st.success("Original Text")
                st.write(raw_text)
                st.success("Prediction")
                emoji_icon = emotions_emoji_dict[prediction]
                st.write(f"{prediction}: {emoji_icon}")
                st.write(f"Confidence: {max(probability[0]):.2f}")

                # Example of using the display function
                display_image(prediction)  

            with col2:
                st.success("Prediction Probability")
                proba_df = pd.DataFrame(probability, columns=pipe_lr.classes_)
                proba_df_clean = proba_df.T.reset_index()
                proba_df_clean.columns = ["Emotions", "Probability"]
                fig = alt.Chart(proba_df_clean).mark_bar().encode(x='Emotions', y='Probability', color='Emotions')
                st.altair_chart(fig, use_container_width=True)

    elif choice == "Monitor":
        st.subheader("Monitor App")

        with st.expander("Page Metrics"):
            page_visited_details = pd.DataFrame(view_all_page_visited_details(), columns=['Pagename', 'Time_of_Visit'])
            st.dataframe(page_visited_details)

            pg_count = page_visited_details['Pagename'].value_counts().rename_axis('Pagename').reset_index(name='Counts')
            c = alt.Chart(pg_count).mark_bar().encode(x='Pagename', y='Counts', color='Pagename')
            st.altair_chart(c, use_container_width=True)

        with st.expander('Emotion Classifier Metrics'):
            df_emotions = pd.DataFrame(view_all_prediction_details(), columns=['Rawtext', 'Prediction', 'Probability', 'Time_of_Visit'])
            st.dataframe(df_emotions)

            prediction_count = df_emotions['Prediction'].value_counts().rename_axis('Prediction').reset_index(name='Counts')
            pc = alt.Chart(prediction_count).mark_bar().encode(x='Prediction', y='Counts', color='Prediction')
            st.altair_chart(pc, use_container_width=True)

    else:
        st.subheader("About")
        st.write("This is an Emotion Classifier App that classifies emotions based on the text entered by the user.")

if __name__ == '__main__':
    main()
