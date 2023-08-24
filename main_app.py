import streamlit as st
from PIL import Image
import io
import zipfile

st.title("Image Resizer")
max_option = st.sidebar.selectbox("How much do you want to resize (in pixel square)?", [128, 256, 512, 1024, 2048])
maxsize = (max_option, max_option)

# Sidebar for uploading individual images and selecting output folder
st.sidebar.title("Upload & Settings")
# Accept broader range of image formats
input_images = st.sidebar.file_uploader("Upload images", type=["jpg", "jpeg", "png", "bmp", "tiff", "gif"], accept_multiple_files=True)

# Process images and display them in a grid
download_data = None
download_filename = None

if input_images:
    st.header("Processed Images")
    with st.spinner("Processing images..."):
        output_files = []
        for input_img in input_images:
            format_detected = Image.open(input_img).format  # Detect format of the image
            with Image.open(input_img) as im:
                im.thumbnail(maxsize)
                output_buffer = io.BytesIO()
                im.save(output_buffer, format=format_detected)  # Save image in its original format
                st.image(im, caption=input_img.name, use_column_width=True)
                output_files.append((output_buffer, format_detected))  # Save format for later use in filename
        st.success("Done!")

        # Prepare download data
        if len(output_files) == 1:
            download_data = output_files[0][0].getvalue()
            download_filename = "resized_image.{}".format(output_files[0][1].lower())
        else:
            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, mode="w") as zip_file:
                    for i, (output_buffer, format_detected) in enumerate(output_files):
                        zip_file.writestr("image_{}.{}".format(i, format_detected.lower()), output_buffer.getvalue())
                download_data = zip_buffer.getvalue()
                download_filename = "resized_images.zip"
            for output_buffer, _ in output_files:
                output_buffer.close()

# Download button on the sidebar
if download_data and download_filename:
    st.sidebar.download_button("Download Resized Images", data=download_data, file_name=download_filename)
