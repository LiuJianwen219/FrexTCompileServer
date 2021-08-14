import os
import logging
logger = logging.getLogger(__name__)

# read file interface, maybe DFS future
def file_reader(file_path):
    if os.path.exists(file_path):
        file = open(file_path, 'rb')
        file_content = file.read()
        file.close()
        return file_content
    logger.error("Read FILE error: file not found: " + file_path)
    return None


# write file interface, maybe DFS future
def file_writer(fire_dir, file_name, file_content):
    if not os.path.exists(fire_dir):
        os.makedirs(fire_dir)
    with open(os.path.join(fire_dir, file_name), 'wb+') as destination:
        for chunk in file_content.chunks():
            destination.write(chunk)
