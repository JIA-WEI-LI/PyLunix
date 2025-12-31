import re
from typing import List

def extract_numbers(input_string: str) -> List[int]:
    number_strings: List[str] = re.findall(r'\d+', input_string)
    numbers: List[int] = [int(num) for num in number_strings]
    return numbers