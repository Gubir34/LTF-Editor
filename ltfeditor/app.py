import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class LTFEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LTF Editor")
        self.setGeometry(100, 100, 300, 200)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("Welcome to LTF Editor")
        layout.addWidget(label)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = LTFEditor()
    editor.show()
    sys.exit(app.exec_())
