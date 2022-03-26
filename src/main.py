import shutil
from collections import defaultdict
from pathlib import Path

from src.data import DATA_DIR


class Manage_Directory:
    def __init__(self, directory, dest=None):
        """
        :param directory: directory path
        :param dest: Path of the folder that you want to move files to, None means the curent directory
        """

        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} dose not exist")
        
        self.class_names = {}
        path_ = DATA_DIR / "AllFormatTypes.csv"
        with open(path_, encoding='utf-8-sig') as fp:
            for line in fp:
                format_, class_ = line.split(',')
                format_ = format_.strip()
                class_ = class_.strip()
                self.class_names[format_] = class_
        
        if dest == None:
            self.dest = Path(directory)

        else:
            self.dest = Path(dest)
    


    def stat(self) -> dict:
        """
        Returns statistics by files extention
        """

        file_ext = defaultdict(int)

        for file in self.directory.iterdir():
            file_ext[file.suffix] += 1

        return file_ext
    

    def clasify (self):
        """
        Clasifies all file that exists in a directory
        """

        self.dest.mkdir(exist_ok=True)

        for file in self.directory.iterdir():
            if file.is_dir():
                continue
            
            if file.suffix in self.class_names:                    
                dest_dir = self.dest / self.class_names[file.suffix]
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest_dir))
            
            else:
                dest_dir = self.dest / 'others'
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest_dir)) 


if __name__ == '__main__':
    clean = Manage_Directory(directory="/mnt/d/New folder (3)")
    print(clean.stat())
    