import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from models.dfa import DFA

# Dữ liệu mặc định
DEFAULT_STATES = "q0, q1, q2"
DEFAULT_ALPHABET = "a, b"
DEFAULT_START = "q0"
DEFAULT_ACCEPT = "q2"
DEFAULT_TRANSITIONS = "q0,a->q1; q0,b->q0\nq1,a->q1; q1,b->q2\nq2,a->q1; q2,b->q0"

class DFATab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_dfa = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        form_layout = QFormLayout()

        # Tạo các trường nhập liệu
        self.txt_states = QLineEdit()
        self.txt_alphabet = QLineEdit()
        self.txt_start = QLineEdit()
        self.txt_accept = QLineEdit()
        self.txt_transitions = QTextEdit()
        self.txt_transitions.setMaximumHeight(90)

        form_layout.addRow("Tập trạng thái Q:", self.txt_states)
        form_layout.addRow("Bảng chữ cái Σ:", self.txt_alphabet)
        form_layout.addRow("Trạng thái bắt đầu q0:", self.txt_start)
        form_layout.addRow("Tập trạng thái đích F:", self.txt_accept)
        form_layout.addRow("Hàm chuyển δ (s,c->next):", self.txt_transitions)

        # Hàng chứa 2 nút hành động: Cập nhật & Reset
        action_bar = QHBoxLayout()
        
        btn_build = QPushButton("⚡ Cập Nhật Cấu Hình DFA")
        btn_build.setProperty("primary", "true")
        btn_build.clicked.connect(self.build_dfa_from_ui)

        btn_reset = QPushButton("🔄 Reset Mặc Định")
        btn_reset.clicked.connect(self.reset_to_default)

        action_bar.addWidget(btn_build, stretch=2)
        action_bar.addWidget(btn_reset, stretch=1)

        # Khu vực mô phỏng chạy thử
        test_layout = QHBoxLayout()
        self.txt_single_input = QLineEdit()
        self.txt_single_input.setPlaceholderText("Nhập chuỗi để xem vết di chuyển (vd: aab)")
        btn_run_single = QPushButton("Chạy Thử Vết")
        btn_run_single.clicked.connect(self.test_single_string)
        test_layout.addWidget(self.txt_single_input)
        test_layout.addWidget(btn_run_single)

        self.lbl_trace = QLabel("Vết di chuyển: ")
        self.lbl_trace.setWordWrap(True)

        layout.addLayout(form_layout)
        layout.addLayout(action_bar)
        layout.addSpacing(10)
        layout.addWidget(QLabel("<b>Mô phỏng luồng vết di chuyển trạng thái (Trace):</b>"))
        layout.addLayout(test_layout)
        layout.addWidget(self.lbl_trace)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Nạp dữ liệu mặc định ban đầu
        self.reset_to_default(show_message=False)

    def reset_to_default(self, show_message=True):
        """Khôi phục cấu hình DFA về mặc định"""
        self.txt_states.setText(DEFAULT_STATES)
        self.txt_alphabet.setText(DEFAULT_ALPHABET)
        self.txt_start.setText(DEFAULT_START)
        self.txt_accept.setText(DEFAULT_ACCEPT)
        self.txt_transitions.setText(DEFAULT_TRANSITIONS)
        self.lbl_trace.setText("Vết di chuyển: ")
        self.txt_single_input.clear()
        
        self.build_dfa_from_ui()
        
        if show_message:
            QMessageBox.information(self, "Thông báo", "Đã khôi phục cấu hình DFA về mặc định!")

    def build_dfa_from_ui(self):
        try:
            states = [s.strip() for s in self.txt_states.text().split(",") if s.strip()]
            alphabet = [a.strip() for a in self.txt_alphabet.text().split(",") if a.strip()]
            start = self.txt_start.text().strip()
            accept = [a.strip() for a in self.txt_accept.text().split(",") if a.strip()]

            raw_text = self.txt_transitions.toPlainText()
            pattern = r'(\w+)\s*,\s*(\w+)\s*->\s*(\w+)'
            matches = re.findall(pattern, raw_text)

            if not matches:
                QMessageBox.warning(self, "Cảnh báo", "Không tìm thấy hàm chuyển δ hợp lệ nào!")
                return False

            transitions = {(curr, char): next_st for curr, char, next_st in matches}
            dfa = DFA(states, alphabet, transitions, start, accept)
            is_valid, msg = dfa.validate_structure()
            
            if not is_valid:
                QMessageBox.critical(self, "Lỗi Cấu Hình DFA", msg)
                return False

            self.current_dfa = dfa
            return True
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Định Dạng", f"Cú pháp không hợp lệ: {e}")
            return False

    def test_single_string(self):
        if not self.current_dfa: return
        inp = self.txt_single_input.text().strip()
        is_accept, path, msg = self.current_dfa.process_string(inp)
        
        path_str = " ➔ ".join(path)
        color = "#2b9348" if is_accept else "#d90429"
        self.lbl_trace.setText(f"<b>Kết quả:</b> <font color='{color}'>{msg}</font><br><b>Luồng dịch chuyển:</b> {path_str}")