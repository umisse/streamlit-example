import streamlit as st
from markdown import markdown
import base64
import io
import zipfile
import re

# Function to separate metadata and content
def separate_metadata_content(content):
    lines = content.split('\n')
    metadata_lines = [line for line in lines if line.startswith('@ ')]
    content_lines = [line for line in lines if not line.startswith('@ ')]
    return '\n'.join(metadata_lines), re.sub('\n+', '\n', '\n'.join(content_lines).strip())

# Get session state
if 'files' not in st.session_state:
    st.session_state['files'] = {}

# User uploads multiple files
uploaded_files = st.file_uploader("Upload .txt files:", type="txt", accept_multiple_files=True)

if uploaded_files:
    # Update session state
    st.session_state['files'] = {file.name: file.getvalue().decode() for file in uploaded_files}

    # Use a number input to choose the current file index
    current_file_index = st.number_input('Select file index:', min_value=0, max_value=len(uploaded_files) - 1, step=1)

    # Get the current file name and content
    current_file_name = list(st.session_state['files'].keys())[current_file_index]
    content = st.session_state['files'][current_file_name]
    metadata, markdown_content = separate_metadata_content(content)

    # Display the metadata
    st.text_area('Metadata:', metadata, height=len(metadata.split('\n')) * 18)

    # Display a Markdown input box and an HTML output panel
    markdown_content = st.text_area('Markdown Content:', markdown_content, height=len(markdown_content.split('\n')) * 18)
    html_content = markdown(markdown_content)
    st.sidebar.markdown('HTML Preview:')
    st.sidebar.markdown(html_content, unsafe_allow_html=True)

    # User clicks save button to store the changes
    if st.button('Save Changes'):
        st.session_state['files'][current_file_name] = metadata + '\n' + markdown_content

    # User clicks download button to download all changes as a zip file
    if st.button('Download All'):
        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
            for file_name, file_content in st.session_state['files'].items():
                zf.writestr(file_name, file_content)
        zip_buffer.seek(0)

        # Generate download link for the zip file
        b64 = base64.b64encode(zip_buffer.getvalue()).decode()
        linko = f'<a href="data:application/zip;base64,{b64}" download="modified_files.zip">Download all modified files</a>'
        st.markdown(linko, unsafe_allow_html=True)
