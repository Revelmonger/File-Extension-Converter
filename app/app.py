from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtCore import QObject, QUrl, pyqtSlot, pyqtSignal, Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtGui import QIcon, QGuiApplication
import glob
import sys
import os

# Receives the responce from HTML and handles it
class CallHandler(QObject):

    directoryPathSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot()
    def directorySelectorButtonClicked(self):
        directory = QFileDialog.getExistingDirectory(None, "Select Directory")
        if directory:
            self.directoryPathSelected.emit(directory)

    @pyqtSlot(str, str, str)
    def convertButtonClicked(self, directory, fromExtension, toExtension):
        renameExtensions.find_files_with_extension_non_recursive(directory, fromExtension, toExtension)



class HTMLWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Sets the window information
        self.setWindowTitle("File Extension Converter")
        self.setWindowIcon(QIcon('static/icons/icon-transparent.png'))
        self.setFixedSize(900, 500)

        # Initializes the Webview
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Sets up requirments for handling HTML responces
        self.channel = QWebChannel()
        self.handler = CallHandler()
        self.channel.registerObject("handler", self.handler)
        self.browser.page().setWebChannel(self.channel)

        # Sets the path to the html doc using relative pathing
        relative_path = "static/site/index.html"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, relative_path)
        self.browser.setUrl(QUrl.fromLocalFile(file_path))


    '''
        # Confirmation of the page loading successfully
        self.browser.page().loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, ok):
        if ok:
            print("HTML loaded successfully!")
    '''


class renameExtensions:
    def find_files_with_extension_non_recursive(directory, fromExtension, toExtension):
        search_pattern = os.path.join(directory, f'*{fromExtension}')
        for file_path in glob.glob(search_pattern):
            renameExtensions.change_file_extension_os(file_path, toExtension)

    def change_file_extension_os(file_path, toExtension):
        base_name, _ = os.path.splitext(file_path)
        new_file_path = base_name + toExtension
        os.rename(file_path, new_file_path)



if __name__ == "__main__":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    window = HTMLWindow()
    window.show()
    sys.exit(app.exec())