from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from utils.tools import AutomataTools

class ItertoolsTab(QWidget):
    def __init__(self, get_dfa_callback, on_send_to_editor_callback):
        super().__init__()
        self.get_dfa = get_dfa_callback
        self.on_send_to_editor = on_send_to_editor_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        ctrl_layout = QHBoxLayout()
        ctrl_layout.addWidget(QLabel("Độ dài chuỗi tối đa (N):"))
        self.spin_max_len = QSpinBox()
        self.spin_max_len.setRange(1, 6)
        self.spin_max_len.setValue(3)
        ctrl_layout.addWidget(self.spin_max_len)

        btn_gen = QPushButton("🔄 Sinh Chuỗi Tự Động & Đưa Vào Editor")
        btn_gen.setProperty("primary", "true")
        btn_gen.clicked.connect(self.generate_and_send)
        ctrl_layout.addWidget(btn_gen)
        ctrl_layout.addStretch()

        self.tbl_results = QTableWidget()
        self.tbl_results.setColumnCount(4)
        self.tbl_results.setHorizontalHeaderLabels(["STT", "Chuỗi Đầu Vào", "Kết Quả DFA", "Vết Trạng Thái"])
        self.tbl_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(ctrl_layout)
        layout.addWidget(self.tbl_results)
        self.setLayout(layout)

    def generate_and_send(self):
        dfa = self.get_dfa()
        if not dfa:
            QMessageBox.warning(self, "Cảnh báo", "Chưa cấu hình DFA!")
            return

        max_len = self.spin_max_len.value()
        test_cases = AutomataTools.generate_all_strings(list(dfa.alphabet), max_len)

        self.tbl_results.setRowCount(0)
        for idx, tc in enumerate(test_cases):
            is_accept, path, msg = dfa.process_string(tc)
            self.tbl_results.insertRow(idx)
            self.tbl_results.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
            self.tbl_results.setItem(idx, 1, QTableWidgetItem(tc))
            
            res_item = QTableWidgetItem("ACCEPT" if is_accept else "REJECT")
            res_item.setForeground(QColor("#2b9348" if is_accept else "#d90429"))
            self.tbl_results.setItem(idx, 2, res_item)
            self.tbl_results.setItem(idx, 3, QTableWidgetItem(" ➔ ".join(path)))

        # Gửi kết quả sang Tab Editor qua Callback
        self.on_send_to_editor("\n".join(test_cases))
        QMessageBox.information(self, "Thông báo", f"Đã sinh {len(test_cases)} chuỗi và nạp vào Trình Soạn Thảo (Tab 1)!")