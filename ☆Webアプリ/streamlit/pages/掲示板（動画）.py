import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import dotenv

# Load environment variables from .env file (recommended)
load_dotenv()

# Google Drive API authentication details
google_service_account_key_file = os.environ['GOOGLE_SERVICE_ACCOUNT_KEY_FILE']
credentials = Credentials.from_service_account_file(
    google_service_account_key_file,
    scopes=['https://www.googleapis.com/auth/drive'],
)

drive_service = build('drive', 'v3', credentials=credentials)


# Function to upload videos to a specific folder in Google Drive
def upload_video_to_folder(folder_id, video_file):
    file_metadata = {
        'name': video_file.name,
        'parents': [folder_id],
    }
    media = MediaFileUpload(video_file.name, mimetype='video/mp4')  # Adjust MIME type as needed

    try:
        drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
        ).execute()
        st.success(f"Video {video_file.name} uploaded successfully.")
    except Exception as e:
        # Capture detailed error message
        error_details = e.args[0]
        if 'message' in error_details:
            error_message = error_details['message']
        else:
            error_message = 'Unknown error occurred.'

        st.error(f"Error uploading video {video_file.name}: {error_message}")


# Main application logic
def main():
    # Define the target folder ID for video uploads
    folder_id = '1oEyH8MMILXXDyXxbOEGPkQK_fzARbPVF'

    st.title('Simple Video Uploader')

    # Upload videos using a file uploader
    uploaded_files = st.file_uploader("Upload videos", type=['mp4', 'avi', 'mov', 'wmv', 'flv', 'mpg', 'mpeg'])
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            upload_video_to_folder(folder_id, uploaded_file)


if __name__ == '__main__':
    main()

        
