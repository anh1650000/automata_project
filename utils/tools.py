import itertools
import re

class AutomataTools:
    @staticmethod
    def generate_all_strings(alphabet, max_length):
        """Dùng itertools.product để sinh tất cả chuỗi có độ dài từ 1 đến max_length"""
        results = []
        for length in range(1, max_length + 1):
            combos = itertools.product(alphabet, repeat=length)
            results.extend(["".join(c) for c in combos])
        return results

    @staticmethod
    def filter_with_regex(lines, pattern_str):
        """Dùng thư viện re để lọc danh sách chuỗi theo Pattern"""
        try:
            pattern = re.compile(pattern_str)
            valid_lines = [line.strip() for line in lines if line.strip() and pattern.match(line.strip())]
            return valid_lines, None
        except re.error as e:
            return [], f"Lỗi cú pháp Regex: {e}"