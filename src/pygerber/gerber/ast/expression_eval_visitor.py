"""The `expression_eval_visitor` module contains definition of
`ExpressionEvalVisitor` class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pygerber.gerber.ast.ast_visitor import AstVisitor
from pygerber.gerber.ast.nodes import Double

if TYPE_CHECKING:
    from pygerber.gerber.ast.nodes import (
        Add,
        Constant,
        Div,
        Expression,
        Mul,
        Neg,
        Pos,
        Sub,
        Variable,
    )


class ExpressionEvalVisitor(AstVisitor):
    """`ExpressionEvalVisitor` class implements a visitor pattern for evaluating
    value of an mathematical expression.
    """

    def __init__(self, scope: Optional[dict[str, Double]] = None) -> None:
        super().__init__()
        self.scope = {} if scope is None else scope
        self.return_value = Double(0.0)

    def evaluate(self, node: Expression) -> float:
        """Evaluate the given expression node."""
        self.return_value = Double(0.0)
        node.visit(self)
        return self.return_value

    def on_add(self, node: Add) -> Add:
        """Handle `Add` node."""
        node.head.visit(self)
        total = self.return_value

        for operand in node.tail:
            operand.visit(self)
            total += self.return_value

        self.return_value = total
        return node

    def on_div(self, node: Div) -> Div:
        """Handle `Div` node."""
        node.head.visit(self)
        total = self.return_value

        for operand in node.tail:
            operand.visit(self)
            total /= self.return_value

        self.return_value = total
        return node

    def on_mul(self, node: Mul) -> Mul:
        """Handle `Mul` node."""
        node.head.visit(self)
        total = self.return_value

        for operand in node.tail:
            operand.visit(self)
            total *= self.return_value

        self.return_value = total
        return node

    def on_sub(self, node: Sub) -> Sub:
        """Handle `Sub` node."""
        node.head.visit(self)
        total = self.return_value

        for operand in node.tail:
            operand.visit(self)
            total -= self.return_value

        self.return_value = total
        return node

    # Math :: Operators :: Unary

    def on_neg(self, node: Neg) -> Neg:
        """Handle `Neg` node."""
        node.operand.visit(self)
        self.return_value = -self.return_value
        return node

    def on_pos(self, node: Pos) -> Pos:
        """Handle `Pos` node."""
        node.operand.visit(self)
        self.return_value = +self.return_value
        return node

    def on_variable(self, node: Variable) -> Variable:
        """Handle `Variable` node."""
        self.return_value = self.scope[node.variable]
        return node

    def on_constant(self, node: Constant) -> Constant:
        """Handle `Constant` node."""
        self.return_value = node.constant
        return node
