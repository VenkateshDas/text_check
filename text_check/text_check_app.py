import streamlit as st
import requests

st.title("Text Check App")
st.subheader("Check your text for grammar errors")

examples = [
        "How was you doing?",
        "I going to the store.",
        "I am going to the store.",
]

st.write("Choose a text from the dropdown below")
text = st.selectbox(
    label="Choose a text",
    options=examples,
)

st.write("Or enter your own text below")
text = st.text_area("Enter your text here", value= text)


def get_correction(text: str) -> None:
    correction_url = "http://containerapi:8080/correct"
    response = requests.post(correction_url, json={"input_sentence": text})
    text_validation = response.json()
    st.write("Validation result:")
    st.write("Input text:", text_validation["text"])
    st.write("Has errors:", text_validation["has_errors"])
    if text_validation["has_errors"]:
        st.write("Suggestion:", text_validation["suggestion"])

submit = st.button("Check text")

if all([text.strip(), submit]):
    get_correction(text)
