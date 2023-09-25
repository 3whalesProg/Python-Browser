import sys
from PyQt6.QtWidgets import QApplication
from main import TabbedBrowser

def main():
    app = QApplication(sys.argv)
    window = TabbedBrowser()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()