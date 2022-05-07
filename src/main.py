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


    def stat(self, directory, by_format_class=True) -> dict:
        """ Returns statistics by files extention
        :param directory: Directory path
        """

        logger.info('Load data')
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} dose not exist")

        logger.info('Calculating...')
        file_ext = defaultdict(int)

        for file in self.directory.iterdir():
            file_ext[file.suffix] += 1

        if by_format_class:
            for item, val in file_ext.items():
                print(f"{self.class_names[item]:20} {val}")
        else:
            for item, val in file_ext.items():
                print(f"{item:20} {val}")


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
    print(len(sys.argv))

    if len(sys.argv) == 2:
        clean.stat(directory=sys.argv[1])

    elif len(sys.argv) == 3:
        clean.stat(directory=sys.argv[1], dest=sys.argv[2])

    else:
        raise IOError('First argument is your files path and second argument should be the path of your preferred destination.\
        If the second argument is not defined, it means the destination is the same as the first argument.')
