from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from views.styles import MODERN_QSS
from views.tab_editor import EditorTab
from views.tab_dfa import DFATab
from views.tab_itertools import ItertoolsTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Editor Studio - Trình Soạn Thảo Văn Bản & Regex/DFA")
        self.setGeometry(100, 100, 950, 680)

        # Áp dụng CSS giao diện
        self.setStyleSheet(MODERN_QSS)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        self.tabs = QTabWidget()

        # 1. Tạo Tab DFA trước để lấy dữ liệu
        self.tab_dfa = DFATab()

        # 2. Tạo Tab Editor (Truyền callback lấy DFA)
        self.tab_editor = EditorTab(get_dfa_callback=lambda: self.tab_dfa.current_dfa)

        # 3. Tạo Tab Itertools (Truyền callback lấy DFA + Callback nạp chữ sang Editor)
        self.tab_itertools = ItertoolsTab(
            get_dfa_callback=lambda: self.tab_dfa.current_dfa,
            on_send_to_editor_callback=self.tab_editor.set_text
        )

        # Lắp ghép các Tab vào Window
        self.tabs.addTab(self.tab_editor, "📝  1. Trình Soạn Thảo & Regex")
        self.tabs.addTab(self.tab_dfa, "⚙️  2. Cấu Hình DFA")
        self.tabs.addTab(self.tab_itertools, "🔄  3. Sinh Test Case")

        main_layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)