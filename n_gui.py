from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, \
    QTextEdit, QLineEdit, QDialog, QListWidget, QListWidgetItem, QDesktopWidget, QSplitter
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtCore import pyqtSlot, Qt
from commands.navi_chip_installer import get_installed_chips, about_chip, search_for_chips, get_latest_release
import webbrowser
navi = None


class NaviGUI(QWidget):

    def __init__(self):
        super().__init__()
        self.wiki_button = None
        self.settings_button = None
        self.chips_button = None
        self.dialog = None
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

        self.chips_button = QPushButton("Chips")
        self.chips_button.clicked.connect(self.show_chips_dialog)
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
        self.user_input.returnPressed.connect(self.submit_user_input)
        text_area_layout.addWidget(self.user_input)

        queries_layout.addLayout(text_area_layout)

        main_layout.addLayout(queries_layout)

        # Set the layout to the main window
        self.setLayout(main_layout)
        self.setWindowTitle("Navi")
        self.setGeometry(100, 100, 800, 600)
        center(self)

    def show_chips_dialog(self):
        self.dialog = ChipsDialog()
        self.dialog.show()

    def submit_user_input(self):
        global navi
        navi.chat_with_navi(self.user_input.text())
        self.user_input.clear()

    def append_text(self, text):
        self.text_edit.append(text)

    def set_navi_instance(self,navi_instance):
        global navi
        navi = navi_instance


class ChipsDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_button = None
        self.chip_list = None
        self.search_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chips")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.open_search_window)

        self.chip_list = QListWidget()
        chips = get_installed_chips()
        if chips:
            self.chip_list.addItems([f"{module['name']}" for module in chips])
        else:
            no_chip_label = "No chips installed"
            self.chip_list.addItem(no_chip_label)
        self.chip_list.itemClicked.connect(self.show_chip_details)
        layout.addWidget(self.search_button)
        layout.addWidget(self.chip_list)

        self.setLayout(layout)
        center(self)


    @pyqtSlot()
    def open_search_window(self):
        self.search_window = SearchWindow()
        self.search_window.show()

    def show_chip_details(self, item):
        # Create a dialog for item details
        details_dialog = QDialog(self)
        details_dialog.setWindowTitle("Chip Details")
        details_layout = QVBoxLayout()

        chip_info = about_chip(item.text())

        chip_name = QLabel(f"<b>Name: </b>{chip_info['name']}")
        chip_owner = QLabel(f"<b>Owner: </b>{chip_info['owner']}")
        chip_description = QLabel(f"<b>Description: </b>{chip_info['description']}")
        chip_version = QLabel(f"<b>Installed version: </b>{chip_info['version']}")
        chip_url = QLabel(f"<b>URL: </b>{chip_info['html_url']}")

        details_layout.addWidget(chip_name)
        details_layout.addWidget(chip_owner)
        details_layout.addWidget(chip_description)
        details_layout.addWidget(chip_url)
        details_layout.addWidget(chip_version)
        if chip_info['latest_version'] != chip_info['version']:
            chip_update_label = QLabel(f"<center><font color='green'>A later version is available: {chip_info['latest_version']}.</font></center>")
            details_layout.addWidget(chip_update_label)
            button_chip_update = QPushButton("Update chip")
            details_layout.addWidget(button_chip_update)

        button_chip_uninstall = QPushButton("Uninstall chip")
        details_layout.addWidget(button_chip_uninstall)

        details_dialog.setLayout(details_layout)
        details_dialog.exec_()


class SearchWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.contents_display = None
        self.results_display = None
        self.splitter = None
        self.install_button = None
        self.search_button = None
        self.page_size_input = None
        self.name_input = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Search Navi Chips')
        self.setGeometry(150, 150, 800, 600)

        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('Enter name')

        self.page_size_input = QLineEdit(self)
        self.page_size_input.setPlaceholderText('Enter page size')
        self.page_size_input.setValidator(QIntValidator(1, 100, self))

        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.on_search_click)

        self.install_button = QPushButton("Install", self)
        self.install_button.setEnabled(False)

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel('Name:'))
        input_layout.addWidget(self.name_input)
        input_layout.addWidget(QLabel('Page Size:'))
        input_layout.addWidget(self.page_size_input)
        input_layout.addWidget(self.search_button)

        layout.addLayout(input_layout)

        self.splitter = QSplitter(Qt.Horizontal, self)

        self.results_display = QListWidget()

        self.contents_display = QTextEdit(self)
        self.contents_display.setReadOnly(True)
        self.splitter.addWidget(self.results_display)
        self.splitter.addWidget(self.contents_display)

        layout.addWidget(self.splitter)
        layout.addWidget(self.install_button)
        self.setLayout(layout)
        center(self)

    @pyqtSlot()
    def on_search_click(self):
        name = self.name_input.text()
        page_size = int(f"{self.page_size_input.text()}" if self.page_size_input.text() else "10")
        page_num = 1

        repos = search_for_chips(name, page_size, page_num)

        if not repos:
            self.results_display.addItem("No Navi Chips found")
        else:
            available_repos = 0
            for repo in repos:
                owner, repo_name, rep_description, repo_url = repo['owner']['login'], repo['name'], repo['description'], repo['html_url']
                latest_release = get_latest_release(owner, repo_name).get('tag_name')
                if latest_release and latest_release != "No release found":
                    available_repos += 1
                    item = QListWidgetItem(f"Name: {repo_name}, Owner: {owner}, Latest Release: {latest_release}")
                    data = (owner, repo_name, rep_description, repo_url, latest_release)
                    item.setData(Qt.UserRole, data)
                    self.results_display.addItem(item)

            if available_repos == 0:
                self.results_display.addItem("No Navi Chips found with releases")
            else:
                self.results_display.itemClicked.connect(self.chip_search_details)

    def chip_search_details(self, item):
        self.contents_display.setText(f"""<center style="text-align: left"><b>Name: </b>{item.data(Qt.UserRole)[1]}<br />
<b>Owner: </b>{item.data(Qt.UserRole)[0]}<br />
<b>Description: </b>{item.data(Qt.UserRole)[2]}<br />
<b>Installed version: </b>{item.data(Qt.UserRole)[4]}<br />
<b>URL: </b>{item.data(Qt.UserRole)[3]}</center>
"""
        )
        self.install_button.setEnabled(True)


def center(self):
    qr = self.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())