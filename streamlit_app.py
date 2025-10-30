import streamlit as st
import requests

API_URL = "https://ajjriyaqwyxyopzhcmlq.supabase.co/functions/v1/generate-qr"

st.title("Custom QR Code Generator")

st.markdown("""
Generate a QR code with advanced customization options.  
QR types supported:  
- URL  
- Text  
- Excel (CSV/XLSX file URL, will create a download link QR)  
""")

# --- Main form ---
with st.form("qr_form"):
    qr_type = st.selectbox(
        "QR Type",
        ["url", "text", "excel"],
        help="Select the type of QR code to generate."
    )
    content = st.text_input(
        "Content",
        value="https://example.com" if qr_type == "url" else "",
        help="For 'url', enter a valid URL. For 'excel', enter the public file URL."
    )
    size = st.slider("Size (px)", 100, 800, 300, help="QR code image size in pixels")
    foreground_color = st.color_picker("Foreground Color", "#000000")
    background_color = st.color_picker("Background Color", "#FFFFFF")
    error_correction = st.selectbox("Error Correction Level", ["L", "M", "Q", "H"], index=1)
    border_width = st.number_input("Border Width", min_value=0, max_value=20, value=4)
    dot_style = st.selectbox("Dot Style", ["square", "circle"], index=0)
    submit_btn = st.form_submit_button("Generate QR Code")

if submit_btn:
    customization = {
        "size": size,
        "foreground_color": foreground_color,
        "background_color": background_color,
        "error_correction": error_correction,
        "border_width": border_width,
        "dot_style": dot_style
    }
    payload = {
        "content": content,
        "qr_type": qr_type,
        "customization": customization
    }
    with st.spinner("Generating QR code..."):
        resp = requests.post(API_URL, json=payload)
    if resp.status_code == 200:
        data = resp.json()
        qr_url = data.get("qr_data_url")
        processed_content = data.get("processed_content")
        st.image(qr_url, caption=f"QR ({qr_type})")
        st.code(processed_content, language="text")
        st.markdown(f"[Direct QR Image Link]({qr_url})")
    else:
        st.error(f"Error: {resp.json().get('error', 'Unknown error')}")
        st.code(resp.text)
else:
    st.info("Fill the form and click 'Generate QR Code'.")
