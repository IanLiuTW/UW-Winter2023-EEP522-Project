from fastapi import APIRouter, Response, status
from dotenv import load_dotenv
from .sftp_agent import SftpAgent
from .config import BACKUP_FILE_PATH, BACKUP_FILE_SIZE_LIMIT_BYTES
import os
import stat

load_dotenv() 

router = APIRouter()

# This endpoint returns the list of files in the specified directory
@router.get("/list", status_code=200)
async def sftpm_list(response: Response, dir: str = ''):
    sftp = None
    try:
        sftp = SftpAgent(host=os.getenv("SFTP_HOST") , username=os.getenv("SFTP_USERNAME"), password=os.getenv("SFTP_PASSWORD"),
                            default_path=f'/{dir}', port=os.getenv("SFTP_PORT"))
        result = sftp.listdir()
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"SFTP Manager: error - {e}"
    finally:
        if sftp:
            sftp.close()
    return result

# This endpoint uploads a file to the specified directory with the specified name and content
@router.get("/upload", status_code=201)
async def sftpm_upload(response: Response, file_name: str, content: str, dir: str = ''):
    sftp = None
    try:
        sftp = SftpAgent(host=os.getenv("SFTP_HOST") , username=os.getenv("SFTP_USERNAME"), password=os.getenv("SFTP_PASSWORD"),
                            default_path=f'/{dir}', port=os.getenv("SFTP_PORT"))
        sftp.putfo(file_name, content)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"SFTP Manager: error - {e}"
    finally:
        if sftp:
            sftp.close()
    return f"SFTP Manager: file {file_name} uploaded to {dir}"

# This endpoint removes a file from the specified directory
@router.get("/remove", status_code=200)
async def sftpm_remove(response: Response, file_name: str, dir: str = ''):
    sftp = None
    try:
        sftp = SftpAgent(host=os.getenv("SFTP_HOST") , username=os.getenv("SFTP_USERNAME"), password=os.getenv("SFTP_PASSWORD"),
                            default_path=f'/{dir}', port=os.getenv("SFTP_PORT"))
        sftp.remove(file_name)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"SFTP Manager: error - {e}"
    finally:
        if sftp:
            sftp.close()
    return f"SFTP Manager: file {file_name} removed from {dir}"

# This endpoint downloads files from the specified directory and stores them in the BACKUP_FILE_PATH directory
# The files are removed from the specified directory
# The files are backed up only if they are smaller than BACKUP_FILE_SIZE_LIMIT_BYTES
@router.get("/backup", status_code=200)
async def sftpm_backup(response: Response, dir: str = ''):
    sftp = None

    if not os.path.exists(BACKUP_FILE_PATH):
        os.makedirs(BACKUP_FILE_PATH)

    results = dict()
    try:
        sftp = SftpAgent(host=os.getenv("SFTP_HOST") , username=os.getenv("SFTP_USERNAME"), password=os.getenv("SFTP_PASSWORD"),
                            default_path=f'/{dir}', port=os.getenv("SFTP_PORT"))

        backup_list = []
        for file in sftp.listdir_attr():
            if stat.S_ISREG(file.st_mode) and file.st_size < BACKUP_FILE_SIZE_LIMIT_BYTES:
                backup_list.append(file.filename)
        for file in backup_list:
            try:
                sftp.get(file, localpath=f'{BACKUP_FILE_PATH}{file}')
                sftp.remove(file)
                results[file] = "status: backed up successfully"
            except Exception as e:
                results[file] = f"status: error - {e}"
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"SFTP Manager: error - {e}"
    finally:
        if sftp:
            sftp.close()
    return results