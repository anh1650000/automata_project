import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QTextCharFormat, QColor, QTextCursor

class EditorTab(QWidget):
    def __init__(self, get_dfa_callback):
        super().__init__()
        self.get_dfa = get_dfa_callback  # Callback lấy cỗ máy DFA hiện tại từ Tab 2
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Thanh công cụ File
        file_bar = QHBoxLayout()
        btn_new = QPushButton("📄 Tạo Mới")
        btn_new.clicked.connect(self.new_file)
        btn_open = QPushButton("📁 Mở File")
        btn_open.clicked.connect(self.open_file)
        btn_save = QPushButton("💾 Lưu File")
        btn_save.clicked.connect(self.save_file)
        
        self.lbl_file_status = QLabel("Trạng thái: File mới")
        self.lbl_file_status.setStyleSheet("color: #6c757d; font-style: italic;")

        file_bar.addWidget(btn_new)
        file_bar.addWidget(btn_open)
        file_bar.addWidget(btn_save)
        file_bar.addSpacing(15)
        file_bar.addWidget(self.lbl_file_status)
        file_bar.addStretch()

        # Thanh công cụ Tìm kiếm Regex
        search_bar = QHBoxLayout()
        search_bar.addWidget(QLabel("<b>Regex:</b>"))
        self.txt_regex_search = QLineEdit("^[ab]+$")
        self.txt_regex_search.setPlaceholderText("Nhập mẫu Regex...")
        
        btn_highlight = QPushButton("🔍 Highlight")
        btn_highlight.setProperty("warning", "true")
        btn_highlight.clicked.connect(self.highlight_regex)

        btn_clear_highlight = QPushButton("🧹 Xóa Tô Màu")
        btn_clear_highlight.clicked.connect(self.clear_highlights)

        btn_run_dfa_check = QPushButton("⚡ Kiểm Tra DFA")
        btn_run_dfa_check.setProperty("primary", "true")
        btn_run_dfa_check.clicked.connect(self.verify_lines_with_dfa)

        search_bar.addWidget(self.txt_regex_search)
        search_bar.addWidget(btn_highlight)
        search_bar.addWidget(btn_clear_highlight)
        search_bar.addWidget(btn_run_dfa_check)

        # Editor Soạn thảo
        self.editor_area = QTextEdit()
        self.editor_area.setPlaceholderText("Gõ hoặc dán văn bản của bạn vào đây...")
        self.editor_area.setStyleSheet("font-family: 'Consolas', monospace; font-size: 14px;")

        self.lbl_search_info = QLabel("Sẵn sàng.")
        self.lbl_search_info.setStyleSheet("font-weight: 600; color: #495057;")

        layout.addLayout(file_bar)
        layout.addLayout(search_bar)
        layout.addWidget(self.editor_area)
        layout.addWidget(self.lbl_search_info)
        self.setLayout(layout)

    def set_text(self, text):
        """Hàm gán text từ bên ngoài (dùng khi sinh test case)"""
        self.editor_area.setText(text)

    def highlight_regex(self):
        pattern_str = self.txt_regex_search.text().strip()
        if not pattern_str:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập mẫu Regex!")
            return

        self.clear_highlights()
        text = self.editor_area.toPlainText()
        if not text: return

        try:
            pattern = re.compile(pattern_str, re.MULTILINE)
            cursor = self.editor_area.textCursor()

            highlight_format = QTextCharFormat()
            highlight_format.setBackground(QColor("#ffea00"))
            highlight_format.setForeground(QColor("#000000"))

            match_count = 0
            for match in pattern.finditer(text):
                start, end = match.span()
                if start == end: continue
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.KeepAnchor)
                cursor.setCharFormat(highlight_format)
                match_count += 1

            self.lbl_search_info.setText(f"✨ Đã tô màu {match_count} vị trí khớp với Regex '{pattern_str}'.")
            self.lbl_search_info.setStyleSheet("font-weight: bold; color: #2b9348;")

        except re.error as e:
            QMessageBox.critical(self, "Lỗi Regex", f"Cú pháp Regex không hợp lệ: {e}")

    def clear_highlights(self):
        cursor = self.editor_area.textCursor()
        cursor.select(QTextCursor.Document)
        default_format = QTextCharFormat()
        default_format.setBackground(QColor("white"))
        default_format.setForeground(QColor("black"))
        cursor.setCharFormat(default_format)
        self.lbl_search_info.setText("Đã xóa tô màu.")
        self.lbl_search_info.setStyleSheet("color: #6c757d;")

    def verify_lines_with_dfa(self):
        dfa = self.get_dfa()
        if not dfa:
            QMessageBox.warning(self, "Cảnh báo", "Chưa có cấu hình DFA nào!")
            return

        text = self.editor_area.toPlainText()
        raw_lines = text.split("\n")
        
        if len(raw_lines) == 1 and not raw_lines[0].strip():
            QMessageBox.warning(self, "Cảnh báo", "Trình soạn thảo đang trống!")
            return

        lines = []
        for line in raw_lines:
            stripped = line.strip()
            if not stripped:
                continue
            lines.append("" if stripped == "ε" else stripped)

        accept_count = sum(1 for line in lines if dfa.process_string(line)[0])
        reject_count = len(lines) - accept_count

        QMessageBox.information(
            self, "Kết Quả Kiểm Tra DFA",
            f"Tổng số dòng: {len(lines)}\n"
            f"• Số dòng CHẤP NHẬN (Accept): {accept_count}\n"
            f"• Số dòng TỪ CHỐI (Reject): {reject_count}"
        )

    def new_file(self):
        self.editor_area.clear()
        self.lbl_file_status.setText("Trạng thái: File mới")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Mở file", "", "Text Files (*.txt);;All Files (*)")
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.editor_area.setText(f.read())
                self.lbl_file_status.setText(f"Đã mở: {path}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể đọc file: {e}")

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Lưu file", "document.txt", "Text Files (*.txt)")
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.editor_area.toPlainText())
                self.lbl_file_status.setText(f"Đã lưu: {path}")
                QMessageBox.information(self, "Thành công", "Đã lưu file!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể ghi file: {e}")