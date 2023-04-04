import streamlit as st
from PIL import Image
import io
import zipfile

st.title("Image Resizer")
max_option = st.sidebar.selectbox("How much do you want to resize (in pixel square)?", [128, 256, 512, 1024, 2048])
maxsize = (max_option, max_option)

# Sidebar for uploading individual images and selecting output folder
st.sidebar.title("Select Images")
input_images = st.sidebar.file_uploader("Upload individual images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
output_folder = st.sidebar.selectbox("Output format:", ["JPEG", "PNG"])

# Process images and display them in a grid
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

        # Download button for resized images
        if len(output_files) == 1:
            st.download_button("Download resized image", data=output_files[0].getvalue(), file_name="resized_image.{}".format(output_folder.lower()))
        else:
            with io.BytesIO() as zip_buffer:
                with zipfile.ZipFile(zip_buffer, mode="w") as zip_file:
                    for i, output_buffer in enumerate(output_files):
                        zip_file.writestr("image_{}.{}".format(i, output_folder.lower()), output_buffer.getvalue())
                st.download_button("Download resized images", data=zip_buffer.getvalue(), file_name="resized_images.zip")
        for output_buffer in output_files:
            output_buffer.close()
