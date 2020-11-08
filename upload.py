from remarkable2 import Remarkable2
from os.path import isfile
from os import environ
from sys import argv
import logging
import coloredlogs

"""
This script has been tested on reMarkable 2 version 2.4.1.30
Find it at https://github.com/droberin/reMarkable2-tools

Based on info from https://remarkablewiki.com/tech/webinterface
"""

reMarkable_ip_address = environ.get('REMARKABLE_HOST', '10.11.99.1')

logger = logging.getLogger(__name__)
coloredlogs.install("INFO", logger=logger)

if len(argv) < 1:
    logger.error(f"No arguments received. Usage: {argv[0]} file_to_upload.pdf")

rM = Remarkable2(address=reMarkable_ip_address)

for count, file in enumerate(argv[1:]):
    _count_idiom = count + 1
    if not isfile(file):
        logger.warning(f"File #{count + 1} «{file}» not found. Won't upload")
        continue
    logger.info(f"[{count + 1}] trying to upload «{file}»")
    rM.filename = file
    if rM.upload():
        logger.info(f"[{count + 1}] file «{file}» upload successfully")
    else:
        logger.critical(f"[{count + 1}] file «{file}» upload failed")
