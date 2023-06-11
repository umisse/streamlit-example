import streamlit as st
from markdown import markdown
import base64

# Function to separate metadata and content
def separate_metadata_content(content):
    lines = content.split('\n')
    metadata_lines = [line for line in lines if line.startswith('@ ')]
    content_lines = [line for line in lines if not line.startswith('@ ')]
    return '\n'.join(metadata_lines), '\n'.join(content_lines)

# User uploads multiple files
uploaded_files = st.file_uploader("Upload .txt files:", type="txt", accept_multiple_files=True)

# Store the current file index
current_file_index = st.empty()

if uploaded_files:
    # Use a number input as a makeshift slider
    current_file_index = st.number_input('Select file index:', min_value=0, max_value=len(uploaded_files) - 1, step=1)

    # Read the current file
    try:
        content = uploaded_files[current_file_index].read().decode()
        metadata, markdown_content = separate_metadata_content(content)

        # Display the metadata
        st.text_area('Metadata:', metadata)

        # Display a Markdown input box and an HTML output panel
        markdown_content = st.text_area('Markdown Content:', markdown_content)
        html_content = markdown(markdown_content)
        st.sidebar.markdown('HTML Preview:')
        st.sidebar.markdown(html_content, unsafe_allow_html=True)

        # User clicks save button to write the content back to the file
        if st.button('Save Changes'):
            # Since we don't have access to the local filesystem, we can't overwrite the original file.
            # Instead, we generate a link that the user can click to download the modified file.
            b64 = base64.b64encode((metadata + '\n' + markdown_content).encode()).decode()  # some strings
            filename = f"modified_{uploaded_files[current_file_index].name}"
            linko= f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download modified file</a>'
            st.markdown(linko, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
