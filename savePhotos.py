from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
from google.oauth2 import service_account
import io

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "./DetectionStatus/seraphic-plexus-387521-9058cfd29eea.json"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("drive", "v3", credentials=credentials)
moody_root_drive_id = "0AIdfwjhIIGWGUk9PVA"


def list_files_in_drive(drive_id):
    # Retrieve the files and folders in the specified drive
    results = (
        service.files()
        .list(
            driveId=drive_id,
            corpora="drive",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
            q="mimeType != 'application/vnd.google-apps.folder'",
            fields="files(name, mimeType)",
        )
        .execute()
    )

    files = results.get("files", [])

    # Print the name and MIME type of each file
    if not files:
        print("No files found in the specified drive.")
    else:
        print("Files in the specified drive:")
        for file in files:
            print(f"Name: {file['name']}, MIME Type: {file['mimeType']}")


def list_folders_in_drive(drive_id):
    query = "mimeType='application/vnd.google-apps.folder' and trashed=false"
    response = (
        service.files()
        .list(
            q=query,
            spaces="drive",
            driveId=drive_id,
            corpora="drive",
            fields="files(id, name, parents)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    )

    folders = response.get("files", [])

    if folders:
        print("Folders in Drive:")
        for folder in folders:
            print(
                f"Folder ID: {folder['id']}, Name: {folder['name']}, Parents: {folder['parents']}"
            )
    else:
        print("No folders found in Drive.")


def upload_to_file_path(
    input, file_name, folder_path, isBytes=True, drive_id=moody_root_drive_id
):
    folder_id = get_folder_id_by_wholepath(folder_path, drive_id=drive_id)

    if folder_id:
        file_metadata = {"name": file_name, "parents": [folder_id]}
        media = ""
        if isBytes:
            media = MediaIoBaseUpload(
                io.BytesIO(input), mimetype="application/octet-stream"
            )
        else:
            media = MediaFileUpload(input, resumable=True)

        file = (
            service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id",
                supportsAllDrives=True,
            )
            .execute()
        )

        print(
            f"File '{file_name}' uploaded to folder with path: {folder_path}, File ID: {file.get('id')}"
        )
    else:
        print(
            f"Folder with path '{folder_path}' not found in Drive with ID: {drive_id}"
        )


## this follows the whole hierarchy of folder_path
## TO ADD: something with creating folders if they don't exist
def get_folder_id_by_wholepath(folder_path, drive_id=moody_root_drive_id):
    folder_names = folder_path.split("/")
    folder_ids = []
    parent_id = get_folder_id_by_name(folder_names.pop(0), drive_id=drive_id)
    # return parent_id

    for folder_name in folder_names:
        folder_id = get_folder_id_by_name(folder_name, parent_id=parent_id)
        if folder_id:
            folder_ids.append(folder_id)
            parent_id = folder_id
        else:
            return "folder path does not exist"

    return parent_id


def get_folder_id_by_name(folder_name, parent_id=None, drive_id=moody_root_drive_id):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    if parent_id:
        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and '{parent_id}' in parents and trashed=false"

    response = (
        service.files()
        .list(
            q=query,
            spaces="drive",
            driveId=drive_id,
            corpora="drive",
            fields="files(id)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
    )

    files = response.get("files", [])
    if files:
        return files[0]["id"]
    else:
        return None


### Call the upload_bytes_to_folder_path function with the opened bytes, file name, Drive ID, and folder path
def savePhotoBytes(input_bytes, file_name, parent_folder="moody053023/bad"):
    upload_to_file_path(
        input_bytes,
        file_name,
        parent_folder,
        isBytes=True,
        drive_id=moody_root_drive_id,
    )


### Call the upload_bytes_to_folder_path function with the opened bytes, file name, Drive ID, and folder path
def savePhotoFile(file, file_name, parent_folder):
    upload_to_file_path(
        file, file_name, parent_folder, isBytes=False, drive_id=moody_root_drive_id
    )


# savePhotoFile("app/hooch/data/corvette.jpg", "corvette.jpg", "lily/moody_053023")
# with open("app/hooch/data/corvette.jpg", "rb") as image:
#     image_bytes = image.read()
#     savePhotoBytes(image_bytes, "corvette.jpg", "lily/moody_053023/percy")

# print(list_folders_in_drive(drive_id=moody_root_drive_id))
