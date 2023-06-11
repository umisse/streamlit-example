import os
import streamlit as st
from markdown import markdown

# Let user select directory
directory = st.text_input('Enter directory path:')

# Fetch .txt files from the directory
files = [f for f in os.listdir(directory) if f.endswith('.txt')]
file_index = st.slider('Choose a file:', 0, len(files) - 1, 0)
current_file = files[file_index]

# Display next and previous buttons
if st.button('Previous File'):
    file_index = max(0, file_index - 1)
if st.button('Next File'):
    file_index = min(len(files) - 1, file_index + 1)

# Load the selected file
with open(os.path.join(directory, current_file), 'r') as file:
    content = file.read()

# Display a Markdown input box and an HTML output panel
markdown_content = st.text_area('Markdown:', content)
html_content = markdown(markdown_content)
st.sidebar.markdown('HTML:')
st.sidebar.code(html_content, language='html')

# Write the content back to the file
if st.button('Save Changes'):
    with open(os.path.join(directory, current_file), 'w') as file:
        file.write(markdown_content)
