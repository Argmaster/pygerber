"""`pygerber.gerberx3.expression_eval_visitor` contains definition of
`ExpressionEvalVisitor` class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pygerber.gerberx3.ast.ast_visitor import AstVisitor
from pygerber.gerberx3.ast.nodes import Double

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.nodes import (
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

    def on_add(self, node: Add) -> None:
        """Handle `Add` node."""
        node.head.visit(self)
        total = self.return_value

        for operand in node.tail:
            operand.visit(self)
            total += self.return_value

        self.return_value = total

    def on_div(self, node: Div) -> None:
        """Handle `Div` node."""
        node.head.visit(self)
        total = self.return_value

        for operand in node.tail:
            operand.visit(self)
            total /= self.return_value

        self.return_value = total

    def on_mul(self, node: Mul) -> None:
        """Handle `Mul` node."""
        node.head.visit(self)
        total = self.return_value

        for operand in node.tail:
            operand.visit(self)
            total *= self.return_value

        self.return_value = total

    def on_sub(self, node: Sub) -> None:
        """Handle `Sub` node."""
        node.head.visit(self)
        total = self.return_value

        for operand in node.tail:
            operand.visit(self)
            total -= self.return_value

        self.return_value = total

    # Math :: Operators :: Unary

    def on_neg(self, node: Neg) -> None:
        """Handle `Neg` node."""
        node.operand.visit(self)
        self.return_value = -self.return_value

    def on_pos(self, node: Pos) -> None:
        """Handle `Pos` node."""
        node.operand.visit(self)
        self.return_value = +self.return_value

    def on_variable(self, node: Variable) -> None:
        """Handle `Variable` node."""
        self.return_value = self.scope[node.variable]

    def on_constant(self, node: Constant) -> None:
        """Handle `Constant` node."""
        self.return_value = node.constant
