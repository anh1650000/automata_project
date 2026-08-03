import itertools
import re

class AutomataTools:
    @staticmethod
    def generate_all_strings(alphabet, max_len):
        """Sinh tất cả các chuỗi từ bảng chữ cái, có bao gồm chuỗi rỗng ε."""
        results = [""]
        for l in range(1, max_len + 1):
            for p in itertools.product(alphabet, repeat=l):
                results.append("".join(p))
        return results

    @staticmethod
    def parse_grammar_to_dfa(rules_text, start_symbol="S"):
        """
        Phân tích Luật sinh Văn phạm Chính quy (Right-Linear Grammar) chuẩn Slide
        Ví dụ:
            S -> 0A
            A -> 10A | ε
            S -> aS | b
        """
        lines = [line.strip() for line in rules_text.strip().split('\n') if line.strip()]
        transitions = {}
        states = set()
        alphabet = set()
        accept_states = set()
        
        final_state = "q_final"
        has_final_state = False

        states.add(start_symbol)

        for line in lines:
            if "->" not in line and "→" not in line:
                continue
            parts = re.split(r'->|→', line)
            lhs = parts[0].strip()
            states.add(lhs)
            
            prods = [p.strip() for p in parts[1].split('|')]
            for prod in prods:
                # Xử lý ký tự rỗng epsilon
                prod_clean = prod.replace('ε', 'e').replace('eps', 'e').replace('epsilon', 'e')
                if prod_clean in ['e', '']:
                    accept_states.add(lhs)
                else:
                    # Bắt chuỗi ký tự kết thúc (terminals) + Biến phi kết thúc (Non-terminal) ở cuối
                    match = re.match(r'^([a-z0-9]+)([A-Z]\w*)?$', prod)
                    if match:
                        terminals, non_term = match.group(1), match.group(2)
                        curr = lhs
                        for i, char in enumerate(terminals):
                            alphabet.add(char)
                            if i == len(terminals) - 1:
                                nxt = non_term if non_term else final_state
                                if not non_term:
                                    has_final_state = True
                            else:
                                nxt = f"{curr}_{char}_{i}"
                                states.add(nxt)
                            
                            transitions[(curr, char)] = nxt
                            curr = nxt

        if has_final_state:
            states.add(final_state)
            accept_states.add(final_state)

        return (
            sorted(list(states)), 
            sorted(list(alphabet)), 
            transitions, 
            start_symbol, 
            sorted(list(accept_states))
        )