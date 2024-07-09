import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="collapsed", menu_items=None)
import numpy as np
from menu import menu
import pandas as pd
from io import StringIO
from transformers import pipeline
from PIL import Image

# st.markdown(
#     r"""
#     <style>
#     .stDeployButton {
#             visibility: hidden;
#         }
#     </style>
#     """, unsafe_allow_html=True
# )

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

pillow_image1 = ''
pillow_image2 = ''


def remove_background(image_path, input):
    global pillow_image1
    global pillow_image2

    # from transformers import pipeline

    pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)
    pillow_mask = pipe(image_path, return_mask = True) # outputs a pillow mask
    if input == 1:
        pillow_image1 = pipe(image_path) # applies mask on input and returns a pillow image
    elif input == 2:
        pillow_image2 = pipe(image_path) # applies mask on input and returns a pillow image
        


menu()
st.html('<h1 style="text-align: center">Image Segmentation</h1>')
st.html('<h4 style="text-align: center">This makes us of an open source transformer model.</h4>')
st.html('<h4 style="text-align: center">This image segmentation model is trained to remove the background of an image.</h4>')
st.html('<h4 style="text-align: center">Select an Image From the Dropdown</h4>')


# image_path1 = "https://farm5.staticflickr.com/4007/4322154488_997e69e4cf_z.jpg"
# image_path2 = "cat2.jpg"
# image_path3 = "https://static.streamlit.io/examples/dog.jpg"
pillow_image = ''
row1 = st.columns(2)
row1_left_margin, row1_col1, row1_col2, row1_right_margin = st.columns([.1, .4, .4, .1])
row1_col1_tile = row1_col1.container(height=600, border=True)   

row1_col1_tile.html('<h4 style="text-align: center">Before</h4>')
option = row1_col1_tile.selectbox(
    "Select an image:",
    ("Cat", "Giraffe"),
    key="image_selection")         
image_path = ''
if option == 'Cat':
    image_path = "cat2.jpg"
else:
    image_path = "giraffe.jpg"
row1_col1_tile.image(image_path, width=300)

with row1_col1_tile:
    with st.spinner("In Progress"):
        remove_clicked1 = row1_col1_tile.button("Remove Background", \
                                        key='remove_button1', \
                                        on_click=remove_background(image_path, 1))

row1_col2_tile = row1_col2.container(height=600, border=True)   
row1_col2_tile.html('<h4 style="text-align: center">After</h4>')

if remove_clicked1:
    row1_col2_tile.image(pillow_image1, width=300)
else:
    row1_col2_tile.write('', ) 

  
st.html('<br/>')
st.html('<h4 style="text-align: center">Upload an Image</h4>')
row2_left_margin, row2_col1, row2_col2, row2_right_margin = st.columns([.1, .4, .4, .1])

row2_col1_tile = row2_col1.container(height=800, border=True)
uploaded_file = ''
remove_clicked2 = ''

row2_col1_tile .html('<h4 style="text-align: center">Before</h4>')
uploaded_file = row2_col1_tile .file_uploader("Upload an image", \
                                              type=['jpeg', 'jpg', 'png'], \
                                                label_visibility="hidden")

if uploaded_file != '' and uploaded_file is not None:
    image = Image.open(uploaded_file)
    row2_col1_tile .image(uploaded_file, width=400)
    row2_col1_tile .write('')

    with st.spinner("In Progress"):
        
        remove_clicked2 = row2_col1_tile .button("Remove Background", \
                                    key='remove_button2', \
                                        on_click=remove_background(image_path2, 2))

row2_col2_tile = row2_col2.container(height=800, border=True)
row2_col2_tile.html('<h4 style="text-align: center">After</h4>')
if remove_clicked2:
    row2_col2_tile.image(pillow_image2, width=400)
else:
    row2_col2_tile.write('', )    

