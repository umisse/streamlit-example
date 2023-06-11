import streamlit as st
from markdown import markdown

# User uploads a file
uploaded_file = st.file_uploader("Upload .txt file:", type="txt")

if uploaded_file is not None:
    # Read the file
    try:
        content = uploaded_file.read().decode()

        # Display a Markdown input box and an HTML output panel
        markdown_content = st.text_area('Markdown:', content)
        html_content = markdown(markdown_content)
        st.sidebar.markdown('HTML:')
        st.sidebar.code(html_content, language='html')

        # User clicks save button to write the content back to the file
        if st.button('Save Changes'):
            # Since we don't have access to the local filesystem, we can't overwrite the original file.
            # Instead, we generate a link that the user can click to download the modified file.
            b64 = base64.b64encode(markdown_content.encode()).decode()  # some strings
            linko= f'<a href="data:file/txt;base64,{b64}" download="modified.txt">Download modified file</a>'
            st.markdown(linko, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")