import streamlit as st
from markdown import markdown

# Function to separate metadata and content
def separate_metadata_content(content):
    lines = content.split('\n')
    metadata_lines = [line for line in lines if line.startswith('@ ')]
    content_lines = [line for line in lines if not line.startswith('@ ')]
    return '\n'.join(metadata_lines), '\n'.join(content_lines).strip()

# User uploads a single file
uploaded_file = st.file_uploader("Upload .txt file:", type="txt")

if uploaded_file:
    # Read the uploaded file content
    content = uploaded_file.getvalue().decode()
    metadata, markdown_content = separate_metadata_content(content)

    # Display the metadata
    st.text_area('Metadata:', metadata, height=len(metadata.split('\n')) * 18)

    # Display a Markdown input box and an HTML output panel
    markdown_content = st.text_area('Markdown Content:', markdown_content, height=len(markdown_content.split('\n')) * 18)
    html_content = markdown(markdown_content)
    st.sidebar.markdown('HTML Preview:')
    st.sidebar.markdown(html_content, unsafe_allow_html=True)
