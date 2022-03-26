import shutil
from collections import defaultdict
from pathlib import Path

class Manage_Directory:
    def __init__(self, directory, dest=None):
        """
        :param directory: directory path
        :param dest: Path of the folder that you want to move files to, None means the curent directory
        """

        self.directory = Path(directory)
        self.class_names = {
            '.csv': 'data',
            '.json': 'data',
            '.srt': 'data',
            '.pdf': 'documents',
            '.txt': 'documents',
            '.docx': 'documents',
            '.ttf': 'fonts',
            '.otf': 'fonts',
            '.webm': 'videos',
            '.pptx': 'presentation',
            '.exe': 'exe',
            '.jpg': 'pictures',
            '.zip': 'compressed',
            }
        
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
    