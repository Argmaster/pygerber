# -*- coding: utf-8 -*-
from unittest import TestCase
from unittest import main
from unittest.mock import Mock

from pygerber.constants import Interpolation
from pygerber.constants import Unit
from pygerber.drawing_state import DrawingState
from pygerber.tokens.gnn import G0N_Token
from pygerber.tokens.gnn import G36_Token
from pygerber.tokens.gnn import G37_Token
from pygerber.tokens.gnn import G70_Token
from pygerber.tokens.gnn import G71_Token
from pygerber.tokens.gnn import G90_Token
from pygerber.tokens.gnn import G91_Token


class G0N_Token_Test(TestCase):
    def parse_token(self, source):
        re_match = G0N_Token.regex.match(source, 0)
        if re_match is not None:
            return G0N_Token(re_match, DrawingState())
        else:
            raise RuntimeError(f"Token not matched for {source}")

    def test_G01(self):
        token = self.parse_token("G01*")
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.interpolation, Interpolation.Linear)

    def test_G02(self):
        token = self.parse_token("G02*")
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.interpolation, Interpolation.ClockwiseCircular)

    def test_G03(self):
        token = self.parse_token("G03*")
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.interpolation, Interpolation.CounterclockwiseCircular)


class GNN_Token_Test(TestCase):
    def parse_token(self, source, token_class):
        re_match = token_class.regex.match(source, 0)
        if re_match is not None:
            return token_class(re_match, DrawingState())
        else:
            raise RuntimeError(f"Token not matched for {source}")

    def test_region_mode_in_out(self):
        token = self.parse_token("G36*", G36_Token)
        state = DrawingState()
        token.alter_state(state)
        self.assertTrue(state.is_regionmode)
        token = self.parse_token("G37*", G37_Token)
        token.post_render(state)
        self.assertFalse(state.is_regionmode)

    def get_renderer_mock(self):
        manager = Mock()
        bounds = Mock()
        return Mock(
            manager=manager,
            bounds=bounds,
            finish_drawing_region=Mock(return_value=(manager, bounds)),
        )

    def test_region_mode_render(self):
        token = self.parse_token("G37*", G37_Token)
        renderer = self.get_renderer_mock()
        token.pre_render(renderer)
        token.render(renderer)
        token.post_render(renderer)
        renderer.finish_drawing_region.assert_called()
        renderer.manager.finish.assert_called_with(renderer.bounds)
        renderer.end_region.assert_called()

    def test_G70(self):
        token = self.parse_token("G70*", G70_Token)
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.unit, Unit.INCHES)

    def test_G71(self):
        token = self.parse_token("G71*", G71_Token)
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.unit, Unit.MILLIMETERS)

    def test_G90(self):
        token = self.parse_token("G90*", G90_Token)
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.coparser.get_mode(), "A")

    def test_G91(self):
        token = self.parse_token("G91*", G91_Token)
        state = DrawingState()
        token.alter_state(state)
        self.assertEqual(state.coparser.get_mode(), "I")


if __name__ == "__main__":
    main()
