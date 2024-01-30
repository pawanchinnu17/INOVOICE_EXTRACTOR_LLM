from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load OpenAI model and get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to format numeric value as currency
def format_currency(value, currency_symbol='$'):
    return f"{currency_symbol}{value:,.2f}"

# Converting image into bytes
def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Gemini Application")

input_prompt = """
    You are an expert in understanding invoices.
    You will receive input images as invoices &
    you will have to answer questions based on the input image
"""

input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the image")

# If ask button is clicked
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, input_text)

        # Print the raw response
        st.subheader("Raw Response:")
        st.text(response)

        # Check if the response can be converted to a numeric value
        if response.replace('.', '', 1).isdigit():
            numeric_response = float(response)
            formatted_response = format_currency(numeric_response, currency_symbol='£')
            st.subheader("The Response is")
            st.write(formatted_response)
        else:
            st.warning("Warning: The response is not a numeric value. Displaying raw response.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
