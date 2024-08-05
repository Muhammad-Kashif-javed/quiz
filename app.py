import streamlit as st
import requests
from ai71 import AI71
import os 
import json


FALCON_API_URL = "https://api.ai71.ai/v1/chat/completions" 
 
  
AI71_API_KEY = os.getenv("API_KEY")


    


def generate_quiz(text):
    headers = {
        "Authorization": f"Bearer {AI71_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "tiiuae/falcon-180B-chat",
        "messages": [
            {"role": "system", "content": "."},
            {"role": "user", "content": f"Generate a quiz based on the following text:\n\n{text}"}
        ]
    }
    response = requests.post(FALCON_API_URL, headers=headers, json=payload)
    return response.json()

st.title("Quiz Generator")

# Text input from the user
user_input = st.text_area("Enter the text for quiz generation:")
# Button to generate quiz
if st.button("Generate Quiz"):
    if user_input:
        with st.spinner("Generating quiz..."):
            try:
                # Invoke the AI model to generate the quiz
                response = generate_quiz(user_input)
                
                st.write("response:", response)
                if 'choices' in response and len(response['choices']) > 0:
                    
                    message = response['choices'][0].get('message', {})
                    content = message.get('content', None)
                    
                    if content:
                        # Display the generated quiz
                        st.markdown("### Generated Quiz")
                        st.write(content)
                        st.markdown("### Download Quiz")
                        st.download_button(
                            label="Download Quiz as Text",
                            data=content,
                            file_name="generated_quiz.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("The API response did not include quiz content. Please check the input and try again.")
                else:
                    st.error("Unexpected API response format. Please check the API response.")
            except Exception as e:
                st.error(f"An error occurred while generating the quiz: {e}")
    else:
        st.error("Please enter some text to generate a quiz.")


                
                
               


































