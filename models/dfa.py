class DFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transitions = transitions  # Dict: {(state, char): next_state}
        self.start_state = start_state
        self.accept_states = set(accept_states)

    def validate_structure(self):
        if self.start_state not in self.states:
            return False, f"Trạng thái bắt đầu '{self.start_state}' không thuộc tập Q!"
        if not self.accept_states.issubset(self.states):
            invalid = self.accept_states - self.states
            return False, f"Trạng thái kết thúc {invalid} không thuộc tập Q!"
        return True, "Cấu hình DFA hợp lệ."

    def process_string(self, input_string):
        """
        Trả về: 
        - is_accept: True/False
        - transitions_taken: Danh sách tuple [(q_from, char, q_to), ...]
        - id_configs: Danh sách cấu hình hình thế [(q_current, remaining_str), ...]
        - msg: Thông báo kết quả
        """
        current_state = self.start_state
        transitions_taken = []
        id_configs = [(current_state, input_string if input_string else "ε")]

        if not input_string:
            is_accept = current_state in self.accept_states
            msg = "CHẤP NHẬN (ACCEPT)" if is_accept else "TỪ CHỐI (REJECT)"
            return is_accept, transitions_taken, id_configs, msg

        for i, char in enumerate(input_string):
            if char not in self.alphabet:
                return False, transitions_taken, id_configs, f"Ký tự '{char}' không thuộc bảng chữ cái Σ!"
            
            next_state = self.transitions.get((current_state, char))
            if next_state is None:
                return False, transitions_taken, id_configs, f"Không có hàm chuyển δ({current_state}, '{char}')"

            transitions_taken.append((current_state, char, next_state))
            current_state = next_state
            
            remaining = input_string[i+1:] if i+1 < len(input_string) else "ε"
            id_configs.append((current_state, remaining))

        is_accept = current_state in self.accept_states
        msg = "CHẤP NHẬN (ACCEPT)" if is_accept else "TỪ CHỐI (REJECT)"
        return is_accept, transitions_taken, id_configs, msg