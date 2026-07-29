MODERN_QSS = """
/* Tổng thể ứng dụng - Font chữ tăng lên 14px */
QMainWindow {
    background-color: #f8f9fa;
}
QWidget {
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    color: #212529;
}

/* Thanh Tab Navbar: Căn giữa & Nới rộng kích thước */
QTabWidget::tab-bar {
    alignment: center; /* Căn giữa 3 tab trên Navbar */
}
QTabWidget::pane {
    border: 1px solid #e9ecef;
    background-color: #ffffff;
    border-radius: 8px;
    padding: 12px;
}
QTabBar::tab {
    background-color: #e9ecef;
    color: #495057;
    padding: 12px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 600;
    margin: 0 4px;
    min-width: 260px; /* Mỗi tab chiếm khoảng ~30% độ rộng giao diện */
    text-align: center;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    color: #4361ee;
    border-bottom: 3px solid #4361ee;
}

/* Khung nhập liệu (Input & TextEdit) */
QLineEdit, QTextEdit, QSpinBox {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 8px 10px;
    font-size: 14px;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {
    border: 1px solid #4361ee;
}

/* Nút bấm */
QPushButton {
    background-color: #ffffff;
    border: 1px solid #ced4da;
    border-radius: 6px;
    padding: 9px 18px;
    font-weight: 600;
    font-size: 14px;
    color: #495057;
}
QPushButton:hover { background-color: #e9ecef; }
QPushButton[primary="true"] {
    background-color: #4361ee;
    color: #ffffff;
    border: none;
}
QPushButton[primary="true"]:hover { background-color: #3f37c9; }
QPushButton[warning="true"] {
    background-color: #ffb703;
    color: #000000;
    border: none;
}
QPushButton[warning="true"]:hover { background-color: #fb8500; color: #ffffff; }

/* Bảng QTableWidget */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 6px;
    font-size: 14px;
}
QHeaderView::section {
    background-color: #f8f9fa;
    font-weight: bold;
    border: none;
    border-bottom: 2px solid #e9ecef;
    padding: 10px;
    font-size: 14px;
}
"""