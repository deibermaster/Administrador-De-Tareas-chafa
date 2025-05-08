import sys
from PyQt5.QtWidgets import QApplication
from gui.catalog_ui import CatalogUI

def main():
    app = QApplication(sys.argv)
    window = CatalogUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 