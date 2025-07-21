from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)

        self.control_layout = QHBoxLayout()
        
        self.url_bar = QLineEdit()
        self.url_bar.setMaximumHeight(30)
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.go_btn = QPushButton("Go")
        self.go_btn.setMinimumHeight(30)
        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(30)
        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(30)

        self.control_layout.addWidget(self.back_btn)
        self.control_layout.addWidget(self.forward_btn)
        self.control_layout.addWidget(self.url_bar)
        self.control_layout.addWidget(self.go_btn)

        self.layout.addLayout(self.control_layout)

        self.browser = QWebEngineView()
        self.go_btn.clicked.connect(self.navigate_to_url)
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)

        self.browser.setUrl(QUrl("https://google.com"))
        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url

        if not url.endswith(".com"):
            search_query = self.url_bar.text().strip().replace(" ", "+")
            url = f"https://www.google.com/search?q={search_query}"

        self.url_bar.setText(url)
        self.browser.setUrl(QUrl(url))

class MyWebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sabse bada")
        self.setWindowIcon(QIcon("resources/logo.png"))

        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.main_layout = QVBoxLayout(self.container)

        # Controls bar
        self.controls_layout = QHBoxLayout()
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        tab_bar = self.tab_widget.tabBar()

        # '+' Button tab
        self.add_tab_button = QPushButton("Add tab")
        self.add_tab_button.setFixedSize(25, 25)
        self.add_tab_button.setStyleSheet("margin-left: 5px;")
        self.add_tab_button.clicked.connect(lambda: self.add_new_tab())
        
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addLayout(self.controls_layout)

        self.add_new_tab()  # Open one tab by default
        self.tab_widget.addTab(QWidget(), "Add tab")

        self.show()

    def add_new_tab(self, url=QUrl("https://google.com")):
        new_tab = BrowserTab()
        index = self.tab_widget.addTab(new_tab, "New Tab")
        self.tab_widget.setCurrentIndex(index)
        new_tab.browser.setUrl(url)
        new_tab.browser.urlChanged.connect(self.update_url_bar)
        new_tab.browser.loadFinished.connect(lambda: self.update_tab_title(index))

    def close_tab(self, index):
        if self.tab_widget.tabText(index) == "Add tab":
            return  # Don't close the "+" tab
        if self.tab_widget.count() > 2:  # At least one actual tab + "+"
            self.tab_widget.removeTab(index)
 
    def update_url_bar(self, index=None):
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, "browser") and hasattr(current_widget, "url_bar"):
            current_widget.url_bar.setText(current_widget.browser.url().toString())

    def update_tab_title(self, index):
        browser = self.current_browser()
        if browser:
            title = browser.title() or "New Tab"
            self.tab_widget.setTabText(index, title)

    def current_browser(self):
        current_widget = self.tab_widget.currentWidget()
        if current_widget and hasattr(current_widget, "browser"):
            return current_widget.browser
        return None

    def on_tab_changed(self, index):
        if self.tab_widget.tabText(index) == "Add tab":
            # Remove the "+" tab temporarily
            self.tab_widget.removeTab(index)

            # Add a new tab
            self.add_new_tab()

            # Re-add the "+" tab at the end
            self.tab_widget.addTab(QWidget(), "Add tab")
            self.tab_widget.setCurrentIndex(self.tab_widget.count() - 2)  # Go to new tab

        else:
            self.update_url_bar()


app = QApplication([])
app.setStyleSheet("""
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QPushButton {
        background-color: #3c3f41;
        color: white;
        border: 1px solid #555;
        padding: 5px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #484a4c;
    }
    QLineEdit {
        background-color: #3c3f41;
        color: white;
        border: 1px solid #555;
        padding: 5px;
        border-radius: 5px;
    }
    QTabWidget::pane {
        border: 1px solid #444;
    }
    QTabBar::tab {
        background: #3c3f41;
        color: white;
        padding: 5px;
        border: 1px solid #555;
        border-bottom: none;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        min-width: 100px;
    }
    QTabBar::tab:selected {
        background: #484a4c;
    }
    QWebEngineView {
        background-color: #2b2b2b;
    }
""")
window = MyWebBrowser()
app.exec_()
