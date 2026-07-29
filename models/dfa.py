class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions  # Dict: {(state, char): next_state}
        self.start_state = start_state
        self.accept_states = set(accept_states)

    def validate_structure(self):
        """Kiểm tra tính hợp lệ của DFA bằng các thao tác trên tập hợp (Set)"""
        if self.start_state not in self.states:
            return False, f"Trạng thái bắt đầu '{self.start_state}' không thuộc tập trạng thái Q!"
        
        # Thao tác tập con: accept_states phải là tập con của states
        if not self.accept_states.issubset(self.states):
            invalid = self.accept_states - self.states
            return False, f"Trạng thái kết thúc {invalid} không nằm trong tập trạng thái Q!"
            
        return True, "Cấu hình DFA hợp lệ."

    def process_string(self, input_string):
        """Chạy chuỗi và trả về: (Kết quả, Vết trạng thái, Thông báo)"""
        current_state = self.start_state
        path = [current_state]

        for char in input_string:
            if char not in self.alphabet:
                return False, path, f"Ký tự '{char}' không thuộc bảng chữ cái Σ!"
            
            next_state = self.transitions.get((current_state, char))
            if next_state is None:
                return False, path, f"Không có hàm chuyển cho ({current_state}, {char})"
            
            current_state = next_state
            path.append(current_state)

        is_accept = current_state in self.accept_states
        msg = "Chấp nhận (ACCEPT)" if is_accept else "Từ chối (REJECT)"
        return is_accept, path, msg