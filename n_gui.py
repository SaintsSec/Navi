from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, \
    QTextEdit, QLineEdit, QDialog, QListWidget
from PyQt5.QtGui import QPixmap
from commands.navi_chip_installer import get_installed_chips, about_chip
import webbrowser
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
        pixmap = QPixmap('images/Logo_SaintSec.png')
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size()))
        top_layout.addWidget(self.image_label)

        # Chips and Settings buttons
        self.chips_button = QPushButton("Chips")
        self.chips_button.clicked.connect(self.showChipsDialog)
        self.settings_button = QPushButton("Settings")
        self.wiki_button = QPushButton("Wiki")
        self.wiki_button.clicked.connect(lambda: webbrowser.open('https://github.com/SaintsSec/Navi/wiki'))
        top_layout.addWidget(self.chips_button)
        top_layout.addWidget(self.settings_button)
        top_layout.addWidget(self.wiki_button)
        
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
        navi.chat_with_navi(self.user_input.text())
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
        chips = get_installed_chips()
        if chips:
            self.list_widget.addItems([f"{module['name']}" for module in chips])
        else:
            no_chip_label = "No chips installed"
            self.list_widget.addItem(no_chip_label)
        self.list_widget.itemClicked.connect(self.showItemDetails)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)

    def showItemDetails(self, item):
        # Create a dialog for item details
        details_dialog = QDialog(self)
        details_dialog.setWindowTitle("Chip Details")
        details_layout = QVBoxLayout()

        chip_info = about_chip(item.text())

        chip_name = QLabel(f"<b>Name: </b>{chip_info["name"]}")
        chip_owner = QLabel(f"<b>Owner: </b>{chip_info["owner"]}")
        chip_description = QLabel(f"<b>Description: </b>{chip_info["description"]}")
        chip_version = QLabel(f"<b>Installed version: </b>{chip_info["version"]}")
        chip_url = QLabel(f"<b>URL: </b>{chip_info["html_url"]}")

        details_layout.addWidget(chip_name)
        details_layout.addWidget(chip_owner)
        details_layout.addWidget(chip_description)
        details_layout.addWidget(chip_url)
        details_layout.addWidget(chip_version)
        if chip_info['latest_version'] != chip_info['version']:
            chip_update_label = QLabel(f"<center><font color='green'>A later version is available: {chip_info["latest_version"]}.</font></center>")
            details_layout.addWidget(chip_update_label)
            button_chip_update = QPushButton("Update chip")
            details_layout.addWidget(button_chip_update)

        button_chip_uninstall = QPushButton("Uninstall chip")
        details_layout.addWidget(button_chip_uninstall)

        details_dialog.setLayout(details_layout)
        details_dialog.exec_()
