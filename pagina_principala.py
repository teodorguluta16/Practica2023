import streamlit as st
from PIL import Image
import base64

st.set_page_config(
    page_title="Preferinte",
    page_icon="🏡",
)

image_path = r'C:\Users\Teo G\Desktop\im.png'

# Read the image file as bytes
with open(image_path, 'rb') as f:
    image_bytes = f.read()

# Encode the image bytes to base64
image_base64 = base64.b64encode(image_bytes).decode()

st.markdown(
    """
    <style>
    .image-container {
        display: grid;
        grid-template-columns: auto auto;
        align-items: center;
    }
    .image-container img {
        grid-column: 1;
        margin-right: 10px;
    }
    .image-container h1 {
        grid-column: 2;
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create the image and title layout
st.markdown(
    f"""
    <div class="image-container">
        <img src="data:image/png;base64,{image_base64}" width="100">
        <h1>PAGINA PRINCIPALA</h1>
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.success("Meniu")

st.write("Add a team: ")

text_input = st.text_input('Introduce Team Name: ')
if st.button('Add team'):
    f = r'C:\Users\Teo G\Desktop\proiect2\coduri.txt'
    file = open(f, "a")
    file.write(text_input + "\n")
    file.close()
    st.write("Succesfully introduced")

st.write("Remove a team: ")
text_input = st.text_input('Introduce Team Name Removable: ')
if st.button('Remove Team'):
    f = r'C:\Users\Teo G\Desktop\proiect2\coduri.txt'
    file = open(f, "r")
    lines = file.readlines()
    file.close()
    modified_lines = [line for line in lines if line.strip() != text_input.strip()]

    if len(modified_lines) < len(lines):
        with open(f, 'w') as file:
            file.writelines(modified_lines)
        st.write("Succesfully removed")

st.write("Remove a championship: ")
text_input = st.text_input('Introduce Championship Removable: ')
if st.button('Remove Championship'):
    f = r'C:\Users\Teo G\Desktop\proiect2\nume_ligi'
    file = open(f, "r")
    lines = file.readlines()
    file.close()
    modified_lines = [line for line in lines if line.strip() != text_input.strip()]

    if len(modified_lines) < len(lines):
        with open(f, 'w') as file:
            file.writelines(modified_lines)
        st.write("Succesfully removed")

text_input = st.text_input('Introduce Championship: ')
if st.button('Add Championship'):
    f = r'C:\Users\Teo G\Desktop\proiect2\nume_ligi'
    file = open(f, "a")
    file.write(text_input + "\n")
    file.close()
    st.write("Succesfully introduced")

st.write("Remove a team: ")
