import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, \
    QTextEdit, QLineEdit, QDialog, QListWidget
from PyQt5.QtGui import QPixmap
from .commands.navi_chip_installer import about_chip

navi = None


class NaviGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Top Layout for Image and Settings
        top_layout = QHBoxLayout()

        # Image placeholder
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)
        pixmap = QPixmap('images/Logo_SaintSec.png')  # Replace 'image.png' with your image file path
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size()))
        top_layout.addWidget(self.image_label)

        # Chips and Settings buttons
        self.chips_button = QPushButton("Chips")
        self.chips_button.clicked.connect(self.showChipsDialog)
        self.settings_button = QPushButton("Settings")
        top_layout.addWidget(self.chips_button)
        top_layout.addWidget(self.settings_button)

        main_layout.addLayout(top_layout)

        # Layout for Queries and Options
        queries_layout = QHBoxLayout()

        # Queries options
        # options_layout = QVBoxLayout()
        # self.option_buttons = []
        # for i in range(5):
        #     btn = QPushButton(f"Option {i+1}")
        #     options_layout.addWidget(btn)
        #     self.option_buttons.append(btn)
        # 
        # queries_layout.addLayout(options_layout)

        # Scrollable text area
        text_area_layout = QVBoxLayout()
        self.scroll_area = QScrollArea()
        self.text_edit = QTextEdit()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.text_edit)
        text_area_layout.addWidget(self.scroll_area)

        # User input area directly below the text area
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Talk to Navi")
        self.user_input.returnPressed.connect(self.submitText)
        text_area_layout.addWidget(self.user_input)

        queries_layout.addLayout(text_area_layout)

        main_layout.addLayout(queries_layout)

        # Set the layout to the main window
        self.setLayout(main_layout)
        self.setWindowTitle("Navi")
        self.setGeometry(100, 100, 800, 600)

    def showChipsDialog(self):
        dialog = ChipsDialog(self)
        dialog.exec_()

    def submitText(self):
        global navi
        response = navi.chat_with_navi(self.user_input.text())
        self.user_input.clear()

    def append_text(self, text):
        self.text_edit.append(text)

    def set_navi_instance(self,navi_instance):
        global navi
        navi = navi_instance


class ChipsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Chips")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.addItems([f"Item {i + 1}" for i in range(10)])
        self.list_widget.itemClicked.connect(self.showItemDetails)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def showItemDetails(self, item):
        # Create a dialog for item details
        details_dialog = QDialog(self)
        details_dialog.setWindowTitle("Item Details")
        details_layout = QVBoxLayout()

        info_label = QLabel(f"Details for {item.text()}")
        details_layout.addWidget(info_label)

        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        details_layout.addWidget(button1)
        details_layout.addWidget(button2)

        details_dialog.setLayout(details_layout)
        details_dialog.exec_()
