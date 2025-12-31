import ast
import math
import operator
from typing import Union

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv
}

def safe_eval_math(expression_str):
    try:
        node = ast.parse(expression_str, mode='eval').body
    except SyntaxError:
        raise ValueError("Invalid mathematical expression syntax.")

    def _evaluate(node):
        if isinstance(node, (ast.Num, ast.Constant)):
            return node.value
        
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise TypeError(f"Operation {op_type.__name__} is not allowed.")
                
            left = _evaluate(node.left)
            right = _evaluate(node.right)
            
            return ALLOWED_OPERATORS[op_type](left, right)
            
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return operator.neg(_evaluate(node.operand))
            elif isinstance(node.op, ast.UAdd):
                return _evaluate(node.operand)
            else:
                raise TypeError(f"Unary Operation {type(node.op).__name__} is not allowed.")
        else:
            raise TypeError(f"Expression type {type(node).__name__} is not allowed.")

    return _evaluate(node)

class IncrementNumberRounder:
    def __init__(self, increment: float = 0.25, rounding_algorithm: str = "RoundHalfUp"):
        self.Increment = increment
        self.RoundingAlgorithm = rounding_algorithm

    def round(self, value: float) -> float:
        if self.Increment <= 0:
            return value
        ratio = value / self.Increment

        if ratio >= 0:
            rounded_ratio = math.floor(ratio + 0.5)
        else:
            rounded_ratio = round(ratio) 
        
        return rounded_ratio * self.Increment
    
class DecimalFormatter:
    def __init__(self, integer_digits: int = 1, fraction_digits: int = 2, number_rounder: IncrementNumberRounder = None):
        self.IntegerDigits = integer_digits
        self.FractionDigits = fraction_digits
        self.NumberRounder = number_rounder
        
    def format(self, value: Union[float, str]) -> str:
        try:
            float_value = float(value)
        except ValueError:
            return str(value)

        if self.NumberRounder:
            float_value = self.NumberRounder.round(float_value)

        format_spec = f":.{self.FractionDigits}f"

        return "{0{1}}".format(float_value, format_spec)