import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from models.dfa import DFA

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

        action_bar = QHBoxLayout()
        btn_build = QPushButton("⚡ Cập Nhật Cấu Hình DFA")
        btn_build.setProperty("primary", "true")
        btn_build.clicked.connect(self.build_dfa_from_ui)

        btn_reset = QPushButton("🔄 Reset Mặc Định")
        btn_reset.clicked.connect(self.reset_to_default)

        action_bar.addWidget(btn_build, stretch=2)
        action_bar.addWidget(btn_reset, stretch=1)

        test_layout = QHBoxLayout()
        self.txt_single_input = QLineEdit()
        self.txt_single_input.setPlaceholderText("Nhập chuỗi để mô phỏng (vd: aab)")
        btn_run_single = QPushButton("Chạy Thử Vết")
        btn_run_single.clicked.connect(self.test_single_string)
        test_layout.addWidget(self.txt_single_input)
        test_layout.addWidget(btn_run_single)

        self.lbl_trace = QLabel("Vết di chuyển sẽ hiển thị ở đây...")
        self.lbl_trace.setWordWrap(True)
        self.lbl_trace.setStyleSheet("background-color: #f1f3f5; padding: 12px; border-radius: 6px; line-height: 1.5;")

        layout.addLayout(form_layout)
        layout.addLayout(action_bar)
        layout.addSpacing(10)
        layout.addWidget(QLabel("<b>Mô phỏng luồng chuyển trạng thái (Chuẩn Giáo Trình):</b>"))
        layout.addLayout(test_layout)
        layout.addWidget(self.lbl_trace)
        layout.addStretch()
        
        self.setLayout(layout)
        self.reset_to_default(show_message=False)

    def reset_to_default(self, show_message=True):
        self.txt_states.setText(DEFAULT_STATES)
        self.txt_alphabet.setText(DEFAULT_ALPHABET)
        self.txt_start.setText(DEFAULT_START)
        self.txt_accept.setText(DEFAULT_ACCEPT)
        self.txt_transitions.setText(DEFAULT_TRANSITIONS)
        self.lbl_trace.setText("Vết di chuyển sẽ hiển thị ở đây...")
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
        is_accept, transitions, id_configs, msg = self.current_dfa.process_string(inp)
        
        color = "#2b9348" if is_accept else "#d90429"

        # 1. Biểu diễn dạng Sơ đồ mũi tên có Ký tự: q0 --'a'--> q1 --'a'--> q1 --'b'--> q2
        arrow_path = ""
        if transitions:
            steps = [f"<b>{st}</b>" for st, _, _ in transitions] + [f"<b>{transitions[-1][2]}</b>"]
            arrow_steps = []
            for idx, (st, c, nst) in enumerate(transitions):
                arrow_steps.append(f"<b>{st}</b> ──<font color='#4361ee'><b>'{c}'</b></font>──➔ ")
            arrow_steps.append(f"<b>{transitions[-1][2]}</b>")
            arrow_path = "".join(arrow_steps)
        else:
            arrow_path = f"<b>{self.current_dfa.start_state}</b>"

        # 2. Biểu diễn dạng Hình thế / Cấu hình (ID) toán học trong Slide: (q0, aab) ⊢ (q1, ab) ⊢ (q1, b) ⊢ (q2, ε)
        id_path = " <b>⊢</b> ".join([f"({st}, <i>{rem}</i>)" for st, rem in id_configs])

        # 3. Biểu diễn chi tiết từng bước hàm chuyển δ
        delta_steps = "<br>".join([f"• δ({st}, '<font color='#4361ee'><b>{c}</b></font>') = <b>{nst}</b>" for st, c, nst in transitions])

        html_result = f"""
        <b>Kết quả:</b> <font color='{color}'><b>{msg}</b></font><br><br>
        <b>1. Sơ đồ dịch chuyển:</b> {arrow_path}<br><br>
        <b>2. Ký hiệu Hình thế toán học (Slide ID):</b><br>&nbsp;&nbsp;&nbsp;&nbsp;{id_path}<br><br>
        <b>3. Chi tiết hàm chuyển δ:</b><br>{delta_steps if delta_steps else "• Không có bước chuyển nào"}
        """
        
        self.lbl_trace.setText(html_result)