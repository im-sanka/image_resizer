import streamlit as st
from PIL import Image
import io
import zipfile

st.title("Image Resizer")
st.subheader("It's an easy app to resize your image. Just upload and download it! That's it!")
max_option = st.sidebar.selectbox("How much do you want to resize (in pixel square)?", [128, 256, 512, 1024, 2048])
maxsize = (max_option, max_option)

# Sidebar for uploading individual images and selecting output folder
st.sidebar.title("Upload & Settings")
input_images = st.sidebar.file_uploader("Upload individual images", type=["jpg", "jpeg"], accept_multiple_files=True)
output_folder = st.sidebar.selectbox("Output format:", ["JPEG", "PNG"])

# Process images and display them in a grid
download_data = None
download_filename = None

if input_images and output_folder:
    st.header("Processed Images")
    with st.spinner("Processing images..."):
        output_files = []
        for input_img in input_images:
            with Image.open(input_img) as im:
                im.thumbnail(maxsize)
                output_buffer = io.BytesIO()
                im.save(output_buffer, format=output_folder, optimize=True)
                st.image(im, caption=input_img.name, use_column_width=True)
                output_files.append(output_buffer)
        st.success("Done!")

        # Prepare download data
        if len(output_files) == 1:
            download_data = output_files[0].getvalue()
            download_filename = "resized_image.{}".format(output_folder.lower())
        else:
            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, mode="w") as zip_file:
                    for i, output_buffer in enumerate(output_files):
                        zip_file.writestr("image_{}.{}".format(i, output_folder.lower()), output_buffer.getvalue())
                download_data = zip_buffer.getvalue()
                download_filename = "resized_images.zip"
        for output_buffer in output_files:
            output_buffer.close()

# Download button on the sidebar
if download_data and download_filename:
    st.sidebar.download_button("Download Resized Images!", data=download_data, file_name=download_filename)
