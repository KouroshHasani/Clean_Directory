import shutil
import sys
from collections import defaultdict
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR


class Manage_Directory:
    def __init__(self):
        """
        :param directory: directory path
        :param dest: Path of the folder that you want to move files to, None means the curent directory
        """

        self.class_names = {}
        path_ = DATA_DIR / "AllFormatTypes.csv"
        with open(path_, encoding='utf-8-sig') as fp:
            for line in fp:
                format_, class_ = line.split(',')
                format_ = format_.strip()
                class_ = class_.strip()
                self.class_names[format_] = class_


    def stat(self) -> dict:
        """ Returns statistics by files extention """

        logger.info('Load data')
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} dose not exist")

        logger.info('Calculating...')
        file_ext = defaultdict(int)

        for file in self.directory.iterdir():
            file_ext[file.suffix] += 1

        return file_ext


    def __call__ (self, directory, dest=None):
        """ Clasifies all file that exists in a directory """

        logger.info('Load data')
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} dose not exist")

        if dest == None:
            self.dest = Path(directory)
        else:
            self.dest = Path(dest)

        logger.info('Moving files...')
        self.dest.mkdir(exist_ok=True)

        for file in self.directory.iterdir():
            if file.is_dir():
                continue

            if file.suffix in self.class_names:
                dest_dir = self.dest / self.class_names[file.suffix]
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest_dir))

            else:
                dest_dir = self.dest / 'Others'
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest_dir))



if __name__ == '__main__':
    clean = Manage_Directory() # sys.argv is a list of terminal inputs when main.py is runed

    if len(sys.argv) == 2:
        clean(directory=sys.argv[1])

    if len(sys.argv) == 3:
        clean(directory=sys.argv[1], dest=sys.argv[2])

    else:
        raise IOError('First argument is your files path and second argument should be the path of your preferred destination.\
        If the second argument is not defined, it means the destination is the same as the first argument.')
