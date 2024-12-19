from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
import qrcode

def upload_to_drive(file_path, credentials_path):
    """
    Uploads a file to Google Drive and generates a shareable link.

    :param file_path: Path to the file to upload
    :param credentials_path: Path to the service account credentials JSON file
    :return: Shareable link of the uploaded file if successful, else None
    """
    try:
        # Authenticate using service account credentials
        creds = Credentials.from_service_account_file(credentials_path, scopes=["https://www.googleapis.com/auth/drive.file"])
        service = build('drive', 'v3', credentials=creds)

        # File metadata
        file_metadata = {'name': file_path.split("/")[-1]}

        # Media file upload
        media = MediaFileUpload(file_path, resumable=True)

        # Upload file
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')

        # Make the file shareable
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(fileId=file_id, body=permission).execute()

        # Generate shareable link
        shareable_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
        print("File uploaded successfully.")
        return shareable_link

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def generate_qrcode(link, output_file="qrcode.png"):
    """
    Generates a QR code for the given link and saves it to a file.

    :param link: The URL to encode in the QR code
    :param output_file: The file name to save the QR code image
    """
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output_file)
        print(f"QR code saved to {output_file}")
    except Exception as e:
        print(f"Failed to generate QR code: {e}")

# Example usage
if __name__ == "__main__":
    file_path = "qrcodegenerator/result.png"  # Replace with the path to your file
    credentials_path = "qrcodegenerator/link-generation-for-drive-8129446a251a.json"  # Replace with your credentials JSON file

    link = upload_to_drive(file_path, credentials_path)
    if link:
        print(f"File link: {link}")
        generate_qrcode(link)
    else:
        print("File upload failed.")

