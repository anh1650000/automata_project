import re
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QSpinBox, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QSyntaxHighlighter
from models.dfa import DFA
from utils.tools import AutomataTools

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automata Studio - DFA & Regex Processing Tool")
        self.setGeometry(100, 100, 850, 600)
        self.current_dfa = None

        self.init_ui()
        self.load_default_dfa()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Thêm 3 tab chức năng
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "1. Cấu hình & Mô phỏng DFA")
        self.tabs.addTab(self.tab2, "2. Sinh Test Case (Itertools)")
        self.tabs.addTab(self.tab3, "3. Xử lý File & Regex")

        self.setup_tab1()
        self.setup_tab2()
        self.setup_tab3()

        main_layout.addWidget(self.tabs)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # ---------------- TAB 1: CẤU HÌNH & TẬP HỢP ----------------
    def setup_tab1(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.txt_states = QLineEdit("q0, q1, q2")
        self.txt_alphabet = QLineEdit("a, b")
        self.txt_start = QLineEdit("q0")
        self.txt_accept = QLineEdit("q2")
        self.txt_transitions = QTextEdit("q0,a->q1; q0,b->q0\nq1,a->q1; q1,b->q2\nq2,a->q1; q2,b->q0")
        self.txt_transitions.setMaximumHeight(80)

        form_layout.addRow("Tập trạng thái Q:", self.txt_states)
        form_layout.addRow("Bảng chữ cái Σ:", self.txt_alphabet)
        form_layout.addRow("Trạng thái bắt đầu q0:", self.txt_start)
        form_layout.addRow("Tập trạng thái đích F:", self.txt_accept)
        form_layout.addRow("Hàm chuyển δ (s,c->next):", self.txt_transitions)

        btn_build = QPushButton("⚡ Cập nhật & Kiểm tra cấu hình DFA")
        btn_build.clicked.connect(self.build_dfa_from_ui)

        # Khung test 1 chuỗi
        test_layout = QHBoxLayout()
        self.txt_single_input = QLineEdit()
        self.txt_single_input.setPlaceholderText("Nhập chuỗi cần test (vd: aab)")
        btn_run_single = QPushButton("Chạy thử")
        btn_run_single.clicked.connect(self.test_single_string)
        test_layout.addWidget(self.txt_single_input)
        test_layout.addWidget(btn_run_single)

        self.lbl_trace = QLabel("Vết di chuyển: ")
        self.lbl_trace.setWordWrap(True)

        layout.addLayout(form_layout)
        layout.addWidget(btn_build)
        layout.addSpacing(10)
        layout.addWidget(QLabel("<b>Mô phỏng từng bước (Trace):</b>"))
        layout.addLayout(test_layout)
        layout.addWidget(self.lbl_trace)
        layout.addStretch()
        self.tab1.setLayout(layout)

    # ---------------- TAB 2: SINH TEST CASE (ITERTOOLS) ----------------
    def setup_tab2(self):
        layout = QVBoxLayout()
        
        ctrl_layout = QHBoxLayout()
        ctrl_layout.addWidget(QLabel("Độ dài chuỗi tối đa (N):"))
        self.spin_max_len = QSpinBox()
        self.spin_max_len.setRange(1, 6)
        self.spin_max_len.setValue(3)
        ctrl_layout.addWidget(self.spin_max_len)

        btn_gen = QPushButton("🔄 Sinh & Test Hàng Loạt")
        btn_gen.clicked.connect(self.generate_and_run_tests)
        ctrl_layout.addWidget(btn_gen)
        ctrl_layout.addStretch()

        self.tbl_results = QTableWidget()
        self.tbl_results.setColumnCount(4)
        self.tbl_results.setHorizontalHeaderLabels(["STT", "Chuỗi Đầu Vào", "Kết Quả", "Vết Trạng Thái"])
        self.tbl_results.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(ctrl_layout)
        layout.addWidget(self.tbl_results)
        self.tab2.setLayout(layout)

    # ---------------- TAB 3: REGEX & FILE I/O ----------------
    def setup_tab3(self):
        layout = QVBoxLayout()

        file_ctrl = QHBoxLayout()
        btn_load_file = QPushButton("📁 Mở File .txt")
        btn_load_file.clicked.connect(self.load_file)
        self.lbl_file_path = QLabel("Chưa chọn file")
        file_ctrl.addWidget(btn_load_file)
        file_ctrl.addWidget(self.lbl_file_path)
        file_ctrl.addStretch()

        regex_ctrl = QHBoxLayout()
        regex_ctrl.addWidget(QLabel("Lọc bằng Regex:"))
        self.txt_regex = QLineEdit("^[ab]+$")
        regex_ctrl.addWidget(self.txt_regex)

        btn_process_file = QPushButton("🚀 Lọc Regex & Chạy DFA")
        btn_process_file.clicked.connect(self.process_file_data)
        regex_ctrl.addWidget(btn_process_file)

        self.txt_file_output = QTextEdit()
        self.txt_file_output.setReadOnly(True)

        btn_save = QPushButton("💾 Lưu Kết Quả Ra File")
        btn_save.clicked.connect(self.save_output_file)

        layout.addLayout(file_ctrl)
        layout.addLayout(regex_ctrl)
        layout.addWidget(self.txt_file_output)
        layout.addWidget(btn_save)
        self.tab3.setLayout(layout)
        
    def highlight_search_results(self):
        # Lấy regex từ ô nhập
        pattern = self.txt_regex.text()
        if not pattern: return
        
        # Thiết lập định dạng tô màu (ví dụ màu vàng)
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("yellow"))
        
        # Xóa các highlight cũ (đây là logic cơ bản)
        self.txt_file_output.setPlainText(self.txt_file_output.toPlainText()) 
        
        # Dùng cursor để tìm và highlight
        cursor = self.txt_file_output.textCursor()
        regex = re.compile(pattern)
        text = self.txt_file_output.toPlainText()
        
        for match in regex.finditer(text):
            start = match.start()
            end = match.end()
            cursor.setPosition(start)
            cursor.setPosition(end, cursor.KeepAnchor)
            cursor.setCharFormat(fmt)

    # ================= LOGIC XỬ LÝ SỰ KIỆN =================
    def build_dfa_from_ui(self):
        try:
            states = [s.strip() for s in self.txt_states.text().split(",") if s.strip()]
            alphabet = [a.strip() for a in self.txt_alphabet.text().split(",") if a.strip()]
            start = self.txt_start.text().strip()
            accept = [a.strip() for a in self.txt_accept.text().split(",") if a.strip()]

            # Dùng Regex để tự động trích xuất các luật chuyển trạng thái dạng: (State, Char) -> NextState
            raw_text = self.txt_transitions.toPlainText()
            pattern = r'(\w+)\s*,\s*(\w+)\s*->\s*(\w+)'
            matches = re.findall(pattern, raw_text)

            if not matches:
                QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy hàm chuyển δ hợp lệ nào!")
                return False

            transitions = {}
            for current_state, char, next_state in matches:
                transitions[(current_state, char)] = next_state

            dfa = DFA(states, alphabet, transitions, start, accept)
            is_valid, msg = dfa.validate_structure()
            
            if not is_valid:
                QMessageBox.critical(self, "Lỗi Cấu Hình DFA", msg)
                return False

            self.current_dfa = dfa
            QMessageBox.information(self, "Thành công", "Cấu hình DFA đã được cập nhật thành công!")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Định Dạng", f"Cú pháp nhập vào không hợp lệ: {e}")
            return False

    def load_default_dfa(self):
        self.build_dfa_from_ui()

    def test_single_string(self):
        if not self.current_dfa: return
        inp = self.txt_single_input.text().strip()
        is_accept, path, msg = self.current_dfa.process_string(inp)
        
        path_str = " ➔ ".join(path)
        color = "green" if is_accept else "red"
        self.lbl_trace.setText(f"<b>Kết quả:</b> <font color='{color}'>{msg}</font><br><b>Luồng dịch chuyển:</b> {path_str}")

    def generate_and_run_tests(self):
        if not self.current_dfa: return
        max_len = self.spin_max_len.value()
        test_cases = AutomataTools.generate_all_strings(list(self.current_dfa.alphabet), max_len)

        self.tbl_results.setRowCount(0)
        for idx, tc in enumerate(test_cases):
            is_accept, path, msg = self.current_dfa.process_string(tc)
            self.tbl_results.insertRow(idx)
            self.tbl_results.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))
            self.tbl_results.setItem(idx, 1, QTableWidgetItem(tc))
            
            res_item = QTableWidgetItem("ACCEPT" if is_accept else "REJECT")
            res_item.setForeground(Qt.green if is_accept else Qt.red)
            self.tbl_results.setItem(idx, 2, res_item)
            self.tbl_results.setItem(idx, 3, QTableWidgetItem(" ➔ ".join(path)))

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Chọn file text", "", "Text Files (*.txt)")
        if path:
            self.lbl_file_path.setText(path)

    def process_file_data(self):
        file_path = self.lbl_file_path.text()
        if file_path == "Chưa chọn file":
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn file trước!")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Lọc dữ liệu bằng Regex
            valid_lines, err = AutomataTools.filter_with_regex(lines, self.txt_regex.text().strip())
            if err:
                QMessageBox.critical(self, "Lỗi Regex", err)
                return

            self.txt_file_output.clear()
            self.txt_file_output.append(f"--- ĐÃ LỌC {len(valid_lines)} CHUỖI HỢP LỆ BẰNG REGEX ---\n")
            
            for line in valid_lines:
                is_accept, path, msg = self.current_dfa.process_string(line)
                status = "[ĐƯỢC CHẤP NHẬN]" if is_accept else "[BỊ TỪ CHỐI]"
                self.txt_file_output.append(f"Chuỗi: '{line}' | {status}\n  └─ Vết: {' ➔ '.join(path)}\n")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi Đọc File", str(e))

    def save_output_file(self):
        content = self.txt_file_output.toPlainText()
        if not content:
            QMessageBox.warning(self, "Cảnh báo", "Không có nội dung để lưu!")
            return
            
        path, _ = QFileDialog.getSaveFileName(self, "Lưu file kết quả", "output.txt", "Text Files (*.txt)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, "Thành công", f"Đã lưu kết quả tại: {path}")