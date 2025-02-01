from pygerber.gerber.linter import lint
from pygerber.gerber.parser import parse
from pygerber.examples import ExamplesEnum, load_example

gerber_source_code = load_example(ExamplesEnum.fc_poly_b_cu)

ast = parse(gerber_source_code)

for rule in lint(ast):
    print(rule.line, rule.rule_id, rule.title)
