# 📝 Regex Text Editor Studio & DFA Visualizer

> **Đồ án môn học:** Tin học Lý thuyết (Mã học phần: CT121/01)
> **Trường:** Công nghệ Thông tin & Truyền thông - Đại học Cần Thơ
> **Giảng viên hướng dẫn:** ThS. Phạm Xuân Hiền
> **Sinh viên thực hiện:** Phạm Duy Anh - MSSV: B2308346 (Khoa học Máy tính - K49)

---

## 📌 Giới thiệu dự án

**Regex Text Editor Studio** là ứng dụng soạn thảo văn bản tích hợp bộ mô phỏng Automata hữu hạn đơn định (DFA) và công cụ tìm kiếm theo Biểu thức chính quy (Regex)[cite: 3]. Dự án kết hợp giữa ứng dụng thực tiễn của xử lý văn bản và cơ sở lý thuyết ngôn ngữ chính quy trong Tin học Lý thuyết[cite: 3].

Phần mềm được xây dựng bằng ngôn ngữ **Python** kết hợp thư viện đồ họa **PyQt5**, **NetworkX** và **Matplotlib**[cite: 3].

---

## 🔥 Các tính năng chính

### 1. 🖊️ Trình soạn thảo văn bản & Tìm kiếm Regex (Tab 1)
* Quản lý file văn bản cơ bản: Tạo mới, Mở (`.txt`), Lưu file
* Tô sáng mẫu tìm kiếm (Real-time Regex Highlighting) bằng màu vàng nổi bật với tốc độ xử lý tức thì
* Bắt lỗi cú pháp Regex và hiển thị cảnh báo chi tiết
* Kiểm tra từng dòng văn bản trực tiếp bằng cấu hình máy DFA

### 2. ⚙️ Cấu hình & Trực quan hóa sơ đồ DFA (Tab 2)
* Khởi tạo máy trạng thái $M = (Q, \Sigma, \delta, q_0, F)$ từ
  * **Văn phạm chính quy tuyến tính phải** $G = (V, \Sigma, P, S)$
  * **Bảng chuyển trạng thái** $\delta$ trực tiếp[cite: 3].
* Tự động tách các trạng thái trung gian cho luật sinh có vế phải dài hơn 1 ký tự
* Vẽ trực quan đồ thị chuyển trạng thái có hướng: đỉnh bắt đầu có mũi tên `START`, các trạng thái kết thúc (Accept States) được tô viền xanh bằng vòng tròn đôi
* Mô phỏng chi tiết vết chuyển trạng thái (ID - Instantaneous Description) cho từng chuỗi đầu vào

### 3. 🧪 Sinh dữ liệu kiểm thử tự động (Tab 3)
* Sinh tất cả các chuỗi kiểm thử từ bảng chữ cái $\Sigma$ theo tích Cartesian với độ dài $N$ tùy chọn ($1 \le N \le 15$)
* Hiển thị bảng đánh giá 3 cột: Chuỗi đầu vào, Kết quả DFA (ACCEPT/REJECT), Vết trạng thái ID
* Lọc dữ liệu hiển thị theo thời gian thực (Tất cả, Chỉ ACCEPT, Chỉ REJECT)
* Chuyển danh sách chuỗi kiểm thử sang trình soạn thảo ở Tab 1 chỉ với 1 cú nhấp

---

## 🛠️ Cấu trúc thư mục dự án

```text
automata_project/
├── main.py                     # File khởi chạy ứng dụng chính
├── data/
│   └── input.txt               # File dữ liệu mẫu thử nghiệm
├── docs/
│   └── B2308346_PhamDuyAnh_Nhom6_THLT.docx # Báo cáo chi tiết
├── models/
│   └── dfa.py                  # Class biểu diễn và xử lý máy trạng thái DFA
├── utils/
│   └── tools.py                # Hàm hỗ trợ sinh chuỗi & chuyển đổi Văn phạm sang DFA
└── views/
    ├── main_window.py          # Bộ điều phối giao diện chính (Window Manager)
    ├── styles.py               # Bộ CSS/QSS giao diện người dùng
    ├── tab_dfa.py              # Giao diện cấu hình & mô phỏng sơ đồ DFA
    ├── tab_editor.py           # Giao diện soạn thảo văn bản & highlight Regex
    └── tab_itertools.py        # Giao diện sinh testcase tự động & bộ lọc
```

---

## 💻 Yêu cầu hệ thống & Cài đặt

### Yêu cầu
* Python **3.8+**
* Các thư viện phụ thuộc: `PyQt5`, `networkx`, `matplotlib`

### Hướng dẫn cài đặt

1. **Clone repository về máy local:**
   ```bash
   git clone [https://github.com/anh1650000/automata_project.git](https://github.com/anh1650000/automata_project.git)
   cd automata_project
   ```

2. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install PyQt5 networkx matplotlib
   ```

## Chạy ứng dụng:
 ```bash
  python main.py
```
## 📖 Hướng dẫn sử dụng chi tiết
* Tạo DFA từ Văn phạm chính quy (Tab 2)
* Nhập quy tắc chuyển đổi vào ô Luật sinh:
  
 ``` text
  S -> 0A
  A -> 10A | ε
 ```
* Nhấn **Dựng DFA / Vẽ đồ thị** để xuất sơ đồ máy trạng thái
* Nhập chuỗi vào ô kiểm thử để theo dõi các bước chuyển trạng thái $\delta(q_0, w) \vdash^* q_f$

### Tìm kiếm bằng Regex (Tab 1)
1. Dán hoặc mở đoạn văn bản trong vùng soạn thảo
2. Nhập biểu thức chính quy (ví dụ tìm email: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`)
3. Nhấn **Highlight** để làm nổi bật tất cả đoạn khớp văn bản

---

## 📜 Tài liệu tham khảo
1. V. H. Trâm, *Giáo trình Tin học Lý thuyết*, ĐH Cần Thơ, 2009
2. J. E. Hopcroft and J. D. Ullman, *Introduction to Automata Theory, Languages, and Computation*, Addison-Wesley, 1979
3. Python Software Foundation, *re — Regular expression operations*
4. Riverbank Computing, *PyQt5 Reference Guide*
