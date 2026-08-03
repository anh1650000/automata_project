from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, 
    QComboBox, QHeaderView, QMessageBox
)
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
        
        # 1. Ô chọn độ dài chuỗi (N)
        ctrl_layout.addWidget(QLabel("Độ dài chuỗi tối đa (N):"))
        self.spin_max_len = QSpinBox()
        self.spin_max_len.setRange(1, 15)
        self.spin_max_len.setValue(3)
        ctrl_layout.addWidget(self.spin_max_len)

        # 2. Nút sinh chuỗi tự động
        btn_gen = QPushButton("🔄 Sinh Chuỗi Tự Động & Đưa Vào Editor")
        btn_gen.setProperty("primary", "true")
        btn_gen.clicked.connect(self.generate_and_send)
        ctrl_layout.addWidget(btn_gen)

        ctrl_layout.addSpacing(20)

        # 3. Menu lọc kết quả ACCEPT / REJECT
        ctrl_layout.addWidget(QLabel("🔍 Lọc kết quả:"))
        self.cbo_filter = QComboBox()
        self.cbo_filter.addItems(["Tất cả", "Chỉ ACCEPT", "Chỉ REJECT"])
        self.cbo_filter.currentIndexChanged.connect(self.filter_results)
        ctrl_layout.addWidget(self.cbo_filter)

        ctrl_layout.addStretch()

        # Bảng hiển thị (ĐÃ BỎ CỘT STT -> Còn 3 cột)
        self.tbl_results = QTableWidget()
        self.tbl_results.setColumnCount(3)
        self.tbl_results.setHorizontalHeaderLabels(["Chuỗi Đầu Vào", "Kết Quả DFA", "Vết Trạng Thái (ID)"])
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
            is_accept, transitions, id_configs, msg = dfa.process_string(tc)
            self.tbl_results.insertRow(idx)
            
            status_str = "ACCEPT" if is_accept else "REJECT"
            bg_color = QColor("#e8f5e9") if is_accept else QColor("#ffffff")  # Xanh lá pastel nhẹ nếu ACCEPT
            
            id_trace_str = " ⊢ ".join([f"({st},{rem})" for st, rem in id_configs])
            
            # Chỉ tạo 3 item đại diện cho 3 cột (Đã bỏ STT)
            items = [
                QTableWidgetItem(tc if tc else "ε (Chuỗi rỗng)"), # Cột 0
                QTableWidgetItem(status_str),                     # Cột 1
                QTableWidgetItem(id_trace_str)                    # Cột 2
            ]
            
            for col_idx, item in enumerate(items):
                item.setBackground(bg_color)
                
                if col_idx == 1:  # Cột "Kết Quả DFA" giờ nằm ở vị trí 1
                    if is_accept:
                        item.setForeground(QColor("#2e7d32"))  # Xanh lá đậm
                    else:
                        item.setForeground(QColor("#c62828"))  # Đỏ
                
                self.tbl_results.setItem(idx, col_idx, item)

        # Áp dụng bộ lọc
        self.filter_results()

        display_cases = [tc if tc else "ε" for tc in test_cases]
        self.on_send_to_editor("\n".join(display_cases))
        QMessageBox.information(self, "Thông báo", f"Đã sinh {len(test_cases)} chuỗi và nạp vào Trình Soạn Thảo (Tab 1)!")

    def filter_results(self):
        """Hàm xử lý ẩn/hiện các hàng dựa theo tùy chọn lọc"""
        filter_option = self.cbo_filter.currentText()
        
        for row in range(self.tbl_results.rowCount()):
            item = self.tbl_results.item(row, 1)  # Cột 1 là cột "Kết Quả DFA" (đã điều chỉnh)
            if not item:
                continue
            
            status = item.text()
            
            if filter_option == "Tất cả":
                self.tbl_results.setRowHidden(row, False)
            elif filter_option == "Chỉ ACCEPT":
                self.tbl_results.setRowHidden(row, status != "ACCEPT")
            elif filter_option == "Chỉ REJECT":
                self.tbl_results.setRowHidden(row, status != "REJECT")