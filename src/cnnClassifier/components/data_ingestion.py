
import os
import urllib.request as request
import zipfile
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
import gdown
from cnnClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config


    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            if self.config.option == 'google':
                # Use gdown for Google Drive downloads
                logger.info("Downloading file from Google Drive...")
                # Construct the download URL
                download_url = f"https://drive.google.com/uc?id={self.config.fileid}"
                gdown.download(download_url, self.config.local_data_file, quiet=False)
            elif self.config.option == 'url':
                # Use urllib for URL downloads
                logger.info("Downloading file from URL...")
                filename, headers = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=self.config.local_data_file
                )
                logger.info(f"{filename} downloaded with the following info: \n{headers}")
            else:
                logger.error("Invalid option. Use 'google' or 'url'.")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

