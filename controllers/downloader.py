from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class DownloadThread(QThread):
    download_complete = pyqtSignal(str)  # Signal to notify when download is complete

    def __init__(self, satellite, start_date, end_date, folder_name):
        super().__init__()
        self.satellite = satellite
        self.start_date = start_date
        self.end_date = end_date
        self.folder_name = folder_name

    def run(self):
        # Trigger the download images function
        print("Starting download...")
        self.satellite.download_images_for_range(self.start_date, self.end_date, self.folder_name)
        self.download_complete.emit(self.folder_name)