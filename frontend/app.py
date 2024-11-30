import streamlit as st
import requests

# Streamlit frontend
def main():
    st.title("Code Generator")

    # Input text from user
    prompt = st.text_area("Enter your prompt", height=150)
    
    # Button to submit the prompt
    if st.button('Generate Code'):
        if prompt:
            # Send a POST request to FastAPI
            api_url = "http://localhost:5000/generate-code"  # Adjust the URL if deploying to cloud
            response = requests.post(api_url, json={"prompt": prompt})

            if response.status_code == 200:
                # Show the generated code in Streamlit
                generated_code = response.json().get('generated_code', '')
                st.text_area("Generated Code", value=generated_code, height=250)
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        else:
            st.warning("Please enter a prompt.")

if __name__ == "__main__":
    main()
