from PyQt5.QtCore import QThread, pyqtSignal

class DownloadThread(QThread):
    download_complete = pyqtSignal(str)  # Signal to notify when download is complete
    download_cancelled = pyqtSignal()  # Signal to notify when download is cancelled

    def __init__(self, satellite, start_date, end_date, folder_name):
        super().__init__()
        self.satellite = satellite
        self.start_date = start_date
        self.end_date = end_date
        self.folder_name = folder_name
        self.is_cancelled = False  # Flag to check for cancellation

    def run(self):
        print("Starting download...")
        # Trigger the download and periodically check if the thread has been cancelled
        for step in self.satellite.download_images_for_range(self.start_date, self.end_date, self.folder_name):
            if self.is_cancelled:
                print("Download cancelled.")
                self.download_cancelled.emit()
                return
            # Simulate step-wise download
            print(f"Processing step: {step}")
            # You can insert sleep or other tasks that happen in steps
        self.download_complete.emit(self.folder_name)

    def cancel(self):
        self.is_cancelled = True
