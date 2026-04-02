import re
import ast
import operator
from typing import Union

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

_EXPRESSION_RE = re.compile(r"[\d\s\.\+\-\*/\(\)\^%]+")


def _eval_node(node: ast.AST) -> Union[int, float]:
    """Recursively evaluate an AST node with only safe numeric operations."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if op_type is ast.Div and right == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](_eval_node(node.operand))
    raise ValueError(f"Unsupported node type: {type(node).__name__}")


def _safe_eval(expression: str) -> Union[int, float]:
    """Parse and evaluate a mathematical expression safely."""
    # Replace ^ with ** for power operator
    expression = expression.replace("^", "**")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {expression}") from exc
    return _eval_node(tree.body)


def _extract_expression(query: str) -> str:
    """Extract a numeric expression from a natural-language query."""
    # Remove common words
    cleaned = re.sub(
        r"\b(calculate|compute|what(?:\s+is)?|equals?|please|the|result|of)\b",
        " ",
        query,
        flags=re.IGNORECASE,
    )
    # Collapse whitespace
    cleaned = " ".join(cleaned.split())
    return cleaned.strip()


def handle_calculator(query: str) -> str:
    """Evaluate a mathematical expression found in the query string."""
    expression = _extract_expression(query)
    if not expression:
        return "Please provide a mathematical expression to calculate."
    try:
        result = _safe_eval(expression)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"The result of {expression} is {result}."
    except ZeroDivisionError as exc:
        return str(exc)
    except ValueError:
        return (
            f"Sorry, I couldn't evaluate the expression '{expression}'. "
            "Please use only numbers and the operators +, -, *, /, %, ^ (or **)."
        )
