from requests import post, get
from requests.exceptions import HTTPError, RequestException, ConnectionError, Timeout
from os.path import isfile, isdir, basename, join
from os import getcwd
from re import findall
import logging
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install("INFO", logger=logger)


class Remarkable2:
    web_ui_upload_endpoint = 'upload'
    web_ui_schema = 'http'

    known_files = {
        'pdf': 'application/pdf',
        'epub': 'application/epub+zip'
    }

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    def __init__(self, address: str = '10.11.99.1'):
        self._filename = None
        self.address = address

    def guess_mime_type(self):
        extension = str(self.filename).split('.')[-1]
        logger.debug(f"Mime type for file {self.filename}: {extension}")
        return self.known_files.get(extension)

    def upload(self):
        url = f'{self.web_ui_schema}://{self.address}/{self.web_ui_upload_endpoint}'
        if not isfile(self.filename):
            raise FileNotFoundError(f"can't upload file {self.filename}: not found")
        guessed_mime_type = self.guess_mime_type()
        if not guessed_mime_type:
            logger.warning("Unknown mime type by extension")
            return False
        files = {'file': (basename(self.filename), open(self.filename, 'rb'))}
        logger.info(f"Uploading {self.filename} to {url}")
        try:
            _response = post(url, files=files)
        except (HTTPError, RequestException, ConnectionError, Timeout) as e:
            logger.critical(f"Error uploading file to device at {self.address}: {e}")
            return False
        if _response.status_code == 201:
            if _response.json():
                if 'status' in _response.json():
                    logger.info(_response.json()['status'])
            return True
        else:
            logger.info(f"[{_response.status_code}]: {_response.text}")

    def ls(self, folder: str = None):
        url = f'{self.web_ui_schema}://{self.address}/documents/'
        if folder:
            url += folder
        try:
            response = get(url, timeout=5)
        except (HTTPError, RequestException, ConnectionError, Timeout) as e:
            logger.critical(f"Error obtaining info from device at {self.address}: {e}")
            return False
        data = response.json()
        if type(data) == list:
            return data

    def download(self, document_uuid: str, target_file: str = None):
        url = f'{self.web_ui_schema}://{self.address}/download/{document_uuid}/placeholder'
        try:
            get_document = get(url)
        except (HTTPError, RequestException, ConnectionError, Timeout) as e:
            logger.critical(f"Error obtaining file from device at {self.address}: {e}")
            return False
        if not target_file:
            target_file = getcwd()
        if get_document.status_code == 200:
            _file_name_matches = findall('filename="(.+)"', get_document.headers['Content-Disposition'])
            if len(_file_name_matches) != 1:
                logger.critical("Could not obtain name from server that is weird!!!")
            file_name_from_server = _file_name_matches[0]
            if isdir(target_file):
                destination_file = join(target_file, file_name_from_server)
            else:
                destination_file = file_name_from_server
            with open(destination_file, 'wb') as _saving_file:
                logger.info(f'Saving obtained file "{file_name_from_server}" at "{destination_file}"')
                _saving_file.write(get_document.content)
            return destination_file
