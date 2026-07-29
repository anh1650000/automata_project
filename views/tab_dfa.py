import re
import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx

from models.dfa import DFA
from utils.tools import AutomataTools

class DFATab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_dfa = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)

        content_layout = QHBoxLayout()
        
        # ==========================================
        # CỘT TRÁI: KHU VỰC NHẬP CẤU HÌNH
        # ==========================================
        left_box = QWidget()
        left_layout = QVBoxLayout(left_box)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Chọn Phương Thức Định Nghĩa
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("<b>Phương thức nhập:</b>"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItems([
            "Luật Sinh Văn Phạm P (Regular Grammar)",
            "Hàm Chuyển Trạng Thái δ (Transition Delta)"
        ])
        self.combo_mode.currentIndexChanged.connect(self.on_mode_changed)
        mode_layout.addWidget(self.combo_mode)
        left_layout.addLayout(mode_layout)

        # ------------------------------------------
        # PHẦN 1: NHẬP LUẬT SINH VĂN PHẠM P
        # ------------------------------------------
        self.box_grammar = QWidget()
        g_layout = QVBoxLayout(self.box_grammar)
        g_layout.setContentsMargins(0, 0, 0, 0)
        
        self.txt_grammar_start = QLineEdit("S")
        self.txt_grammar_rules = QTextEdit()
        self.txt_grammar_rules.setPlaceholderText("Cú pháp ví dụ:\nS -> 0A | b\nA -> 10A | ε")
        self.txt_grammar_rules.setText("S -> 0A\nA -> 10A | ε")
        
        g_form = QFormLayout()
        g_form.addRow("Ký hiệu bắt đầu (S):", self.txt_grammar_start)
        
        g_layout.addLayout(g_form)
        g_layout.addWidget(QLabel("Tập luật sinh P (Dùng '->' hoặc '→', '|' cho lựa chọn, 'ε' cho rỗng):"))
        g_layout.addWidget(self.txt_grammar_rules)

        # ------------------------------------------
        # PHẦN 2: NHẬP HÀM CHUYỂN TRẠNG THÁI δ
        # ------------------------------------------
        self.box_delta = QWidget()
        d_form = QFormLayout(self.box_delta)
        d_form.setContentsMargins(0, 0, 0, 0)
        self.txt_states = QLineEdit("q0, q1, q2")
        self.txt_alphabet = QLineEdit("a, b")
        self.txt_start = QLineEdit("q0")
        self.txt_accept = QLineEdit("q2")
        self.txt_transitions = QTextEdit("q0,a->q1; q0,b->q0\nq1,a->q1; q1,b->q2\nq2,a->q1; q2,b->q0")
        self.txt_transitions.setMaximumHeight(90)

        d_form.addRow("Tập trạng thái Q:", self.txt_states)
        d_form.addRow("Bảng chữ cái Σ:", self.txt_alphabet)
        d_form.addRow("Trạng thái bắt đầu q0:", self.txt_start)
        d_form.addRow("Tập trạng thái đích F:", self.txt_accept)
        d_form.addRow("Hàm chuyển δ (s,c->next):", self.txt_transitions)
        self.box_delta.setVisible(False)

        left_layout.addWidget(self.box_grammar)
        left_layout.addWidget(self.box_delta)

        # Thanh nút bấm hành động
        action_bar = QHBoxLayout()
        btn_build = QPushButton("⚡ Cập Nhật Sơ Đồ DFA")
        btn_build.setProperty("primary", "true")
        btn_build.clicked.connect(self.build_dfa_from_ui)

        btn_reset = QPushButton("🔄 Reset")
        btn_reset.clicked.connect(self.reset_to_default)

        action_bar.addWidget(btn_build, stretch=2)
        action_bar.addWidget(btn_reset, stretch=1)
        left_layout.addLayout(action_bar)

        # ==========================================
        # CỘT PHẢI: KHUNG VẼ SƠ ĐỒ ĐỒ HỌA
        # ==========================================
        right_box = QWidget()
        right_layout = QVBoxLayout(right_box)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        self.figure = Figure(figsize=(5, 3.8), facecolor='#ffffff')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("border: 1px solid #ced4da; border-radius: 8px;")
        
        right_layout.addWidget(QLabel("<b>Sơ Đồ Đồ Họa Trạng Thái DFA:</b>"))
        right_layout.addWidget(self.canvas)

        content_layout.addWidget(left_box, stretch=4)
        content_layout.addWidget(right_box, stretch=5)

        # ==========================================
        # KHU VỰC DƯỚI: CHẠY THỬ VẾT
        # ==========================================
        test_layout = QHBoxLayout()
        self.txt_single_input = QLineEdit()
        self.txt_single_input.setPlaceholderText("Nhập chuỗi kiểm thử...")
        btn_run_single = QPushButton("🚀 Mô Phỏng Vết")
        btn_run_single.setProperty("primary", "true")
        btn_run_single.clicked.connect(self.test_single_string)
        test_layout.addWidget(self.txt_single_input, stretch=3)
        test_layout.addWidget(btn_run_single, stretch=1)

        self.lbl_trace = QLabel("Kết quả mô phỏng vết sẽ hiển thị tại đây...")
        self.lbl_trace.setWordWrap(True)
        self.lbl_trace.setStyleSheet("background-color: #f8f9fa; padding: 12px; border: 1px solid #e9ecef; border-radius: 6px; line-height: 1.6;")

        main_layout.addLayout(content_layout)
        main_layout.addSpacing(5)
        main_layout.addWidget(QLabel("<b>Mô Phỏng Vết Dịch Chuyển Trạng Thái:</b>"))
        main_layout.addLayout(test_layout)
        main_layout.addWidget(self.lbl_trace)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.reset_to_default(show_message=False)

    def on_mode_changed(self, index):
        """Chuyển đổi linh hoạt giữa Luật sinh P và Hàm chuyển delta"""
        self.box_grammar.setVisible(index == 0)
        self.box_delta.setVisible(index == 1)
        self.build_dfa_from_ui()

    def reset_to_default(self, show_message=True):
        self.combo_mode.setCurrentIndex(0)
        self.txt_grammar_start.setText("S")
        self.txt_grammar_rules.setText("S -> 0A\nA -> 10A | ε")
        self.txt_states.setText("q0, q1, q2")
        self.txt_alphabet.setText("a, b")
        self.txt_start.setText("q0")
        self.txt_accept.setText("q2")
        self.txt_transitions.setText("q0,a->q1; q0,b->q0\nq1,a->q1; q1,b->q2\nq2,a->q1; q2,b->q0")
        self.lbl_trace.setText("Kết quả mô phỏng vết sẽ hiển thị tại đây...")
        self.txt_single_input.clear()
        
        self.build_dfa_from_ui()
        if show_message:
            QMessageBox.information(self, "Thông báo", "Đã khôi phục dữ liệu mặc định!")

    def build_dfa_from_ui(self):
        try:
            mode = self.combo_mode.currentIndex()
            if mode == 0:
                # Dựng DFA từ Tập Luật Sinh P
                start_sym = self.txt_grammar_start.text().strip() or "S"
                rules_txt = self.txt_grammar_rules.toPlainText()
                states, alphabet, transitions, start, accept = AutomataTools.parse_grammar_to_dfa(rules_txt, start_sym)
                dfa = DFA(states, alphabet, transitions, start, accept)
            else:
                # Dựng DFA từ Hàm chuyển Delta
                states = [s.strip() for s in self.txt_states.text().split(",") if s.strip()]
                alphabet = [a.strip() for a in self.txt_alphabet.text().split(",") if a.strip()]
                start = self.txt_start.text().strip()
                accept = [a.strip() for a in self.txt_accept.text().split(",") if a.strip()]

                raw_text = self.txt_transitions.toPlainText()
                matches = re.findall(r'(\w+)\s*,\s*(\w+)\s*->\s*(\w+)', raw_text)
                transitions = {(curr, char): next_st for curr, char, next_st in matches}
                dfa = DFA(states, alphabet, transitions, start, accept)

            is_valid, msg = dfa.validate_structure()
            if not is_valid:
                QMessageBox.critical(self, "Lỗi Cấu Hình DFA", msg)
                return False

            self.current_dfa = dfa
            self.draw_graph()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Cú Pháp", f"Không thể xử lý văn phạm/cấu hình: {e}")
            return False

    def draw_graph(self, active_path=None):
        if not self.current_dfa: return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#ffffff')

        states = list(self.current_dfa.states)
        accept_states = set(self.current_dfa.accept_states)
        start_state = self.current_dfa.start_state
        transitions = self.current_dfa.transitions

        G = nx.DiGraph()
        for s in states: G.add_node(s)

        edge_dict = {}
        for (src, char), dst in transitions.items():
            if (src, dst) not in edge_dict: edge_dict[(src, dst)] = []
            edge_dict[(src, dst)].append(char)

        for (src, dst), chars in edge_dict.items():
            G.add_edge(src, dst, label=", ".join(chars))

        pos = nx.circular_layout(G) if len(states) <= 4 else nx.spring_layout(G, seed=42)

        active_nodes, active_edges = set(), set()
        if active_path:
            for st in active_path: active_nodes.add(st)
            for i in range(len(active_path) - 1):
                active_edges.add((active_path[i], active_path[i+1]))

        normal_nodes = [s for s in states if s not in accept_states]
        accept_nodes = [s for s in states if s in accept_states]

        NODE_SIZE = 1200  # Điều chỉnh kích thước chuẩn cho nút

        # Vẽ trạng thái thường
        if normal_nodes:
            colors = ['#ffecb3' if s in active_nodes else '#e3f2fd' for s in normal_nodes]
            borders = ['#ff9800' if s in active_nodes else '#1976d2' for s in normal_nodes]
            nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, node_color=colors,
                                   node_size=NODE_SIZE, edgecolors=borders, linewidths=2.5, ax=ax)

        # Vẽ trạng thái kết thúc (Vòng đôi)
        if accept_nodes:
            colors = ['#ffecb3' if s in active_nodes else '#e8f5e9' for s in accept_nodes]
            borders = ['#ff9800' if s in active_nodes else '#2e7d32' for s in accept_nodes]
            nx.draw_networkx_nodes(G, pos, nodelist=accept_nodes, node_color=colors, node_size=NODE_SIZE, edgecolors=borders, linewidths=3, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=accept_nodes, node_color=colors, node_size=NODE_SIZE * 0.6, edgecolors=borders, linewidths=2, ax=ax)

        # Vẽ nhãn START
        if start_state in pos:
            x, y = pos[start_state]
            ax.annotate('START ➔', xy=(x, y), xytext=(x - 0.22, y + 0.22),
                        arrowprops=dict(facecolor='#d32f2f', shrink=0.08, width=2, headwidth=7),
                        fontsize=9, fontweight='bold', color='#d32f2f', ha='right')

        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_color='#212529', ax=ax)

        # Vẽ các cung có hướng (Edges với mũi tên sắc nét)
        for (u, v, d) in G.edges(data=True):
            lbl = d['label']
            is_active = (u, v) in active_edges
            edge_col = '#ff9800' if is_active else '#4361ee'
            width = 2.5 if is_active else 1.5

            if u == v:
                # Xử lý Vòng tự lặp (Self-loop) có mũi tên
                x, y = pos[u]
                ax.annotate(lbl, xy=(x, y+0.08), xytext=(x, y+0.25),
                            arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.8", color=edge_col, lw=width, mutation_scale=18),
                            fontsize=9, fontweight='bold', color='#d32f2f' if is_active else '#1565c0', ha='center')
            else:
                # Vẽ cung dịch chuyển giữa 2 trạng thái kèm MŨI TÊN CHỈ HƯỚNG
                rad = 0.22 if G.has_edge(v, u) else 0.1
                nx.draw_networkx_edges(
                    G, pos, edgelist=[(u, v)], ax=ax,
                    connectionstyle=f'arc3, rad={rad}',
                    arrowstyle='-|>',
                    arrowsize=20,
                    edge_color=edge_col,
                    width=width,
                    min_source_margin=18,  # Lùi gốc cung ra ngoài viền node
                    min_target_margin=18   # Lùi ngọn mũi tên ra mép node để không bị che
                )
                
                # Hiển thị nhãn ký tự dịch chuyển
                p1, p2 = np.array(pos[u]), np.array(pos[v])
                mid = (p1 + p2) / 2
                diff = p2 - p1
                perp = np.array([-diff[1], diff[0]])
                if np.linalg.norm(perp) > 0: perp = perp / np.linalg.norm(perp) * 0.08 * (1 if rad > 0 else -1)
                lbl_pos = mid + perp
                ax.text(lbl_pos[0], lbl_pos[1], lbl, fontsize=9, fontweight='bold', 
                        color='#d32f2f' if is_active else '#212529', 
                        ha='center', va='center', 
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffffff', edgecolor='#ced4da', alpha=0.9))

        ax.axis('off')
        self.figure.tight_layout()
        self.canvas.draw()

    def test_single_string(self):
        if not self.current_dfa: return
        inp = self.txt_single_input.text().strip()
        is_accept, transitions, id_configs, msg = self.current_dfa.process_string(inp)
        
        active_path = [st for st, _ in id_configs]
        self.draw_graph(active_path=active_path)

        color = "#2b9348" if is_accept else "#d90429"

        if transitions:
            arrow_steps = [f"<b>{st}</b> ──<font color='#4361ee'><b>'{c}'</b></font>──➔ " for st, c, _ in transitions]
            arrow_steps.append(f"<b>{transitions[-1][2]}</b>")
            arrow_path = "".join(arrow_steps)
        else:
            arrow_path = f"<b>{self.current_dfa.start_state}</b>"

        id_path = " <b>⊢</b> ".join([f"({st}, <i>{rem}</i>)" for st, rem in id_configs])
        delta_steps = " &nbsp;&nbsp;|&nbsp;&nbsp; ".join([f"δ({st}, '<font color='#4361ee'><b>{c}</b></font>') = <b>{nst}</b>" for st, c, nst in transitions])

        html_result = f"""
        <b>Kết Quả:</b> <font color='{color}'><b>{msg}</b></font><br>
        <b>1. Sơ Đồ Dịch Chuyển:</b> {arrow_path}<br>
        <b>2. Ký Hiệu Hình Thế Toán Học (Slide ID):</b> {id_path}<br>
        <b>3. Chi Tiết Các Bước Hàm Chuyển δ:</b> {delta_steps if delta_steps else "Không có bước chuyển"}
        """
        self.lbl_trace.setText(html_result)