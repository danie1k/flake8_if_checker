import ast
import collections
import enum

DEFAULT_MAX_IF_CONDITIONS = 2

Result = collections.namedtuple("Result", "type kind line col condition_count")


class IfCheckerErrors(enum.Enum):
    IF01 = "IF01 Too many conditions ({condition_count}) in {type} {kind}"


class IfKind(enum.Enum):
    IfExp = "Expression"
    If = "Statement"


class IfType(enum.Enum):
    IF = "IF"
    ELIF = "ELIF"


class AstVisitor(object):
    def __init__(self):
        self._result_store = {}

    @property
    def results(self):
        return tuple(
            sorted(
                self._result_store.values(),
                key=lambda result: (result.line, result.col, result.kind),
            )
        )

    def lookup(self, tree):
        assert hasattr(tree, "body"), "tree must have `body` property"
        self._visit_node(tree)

    def _get_type(self, node):
        return type(node).__name__

    def _visit_node(self, node):
        self.__visit_subtree(node, "body")
        self.__visit_subtree(node, "orelse")
        self.__visit_subtree(node, "test")
        self.__visit_subtree(node, "value")
        self.__visit_subtree(node, "values")

        # Visiting: If statements & expression
        if self._get_type(node) in ["If", "IfExp"]:
            self.__visit_if(node)

    def __count_if(self, node):
        counter = 0
        values = getattr(node, "values", [])

        if isinstance(values, collections.Iterable):
            for node_value in values:
                node_type = self._get_type(node_value)
                if node_type == "BoolOp":
                    counter += self.__count_if(node_value)
                else:
                    counter += 1

        return counter

    def __visit_if(self, node):
        node_type = self._get_type(node)
        if node_type not in ["If", "IfExp"]:
            return

        node_line = node.lineno
        node_col = node.col_offset
        node_kind = IfKind[node_type].value
        result_key = (node_kind, node_line, node_col)

        test_values = getattr(node.test, "values", [])
        if not test_values:
            counter = 1
        else:
            counter = self.__count_if(node.test)

        self._result_store[result_key] = Result(
            type=None,
            kind=node_kind,
            line=node_line,
            col=node_col,
            condition_count=counter,
        )

    def __visit_subtree(self, node, subtree_name):
        subtree = getattr(node, subtree_name, [])
        if isinstance(subtree, collections.Iterable):
            [self._visit_node(subtree_item) for subtree_item in subtree]
        elif isinstance(subtree, ast.AST):
            self._visit_node(subtree)


class IfChecker(object):
    name = "flake8_if_checker"
    version = "0.3.0"

    ELIF_LEN = len("elif ")

    def __init__(self, tree, lines, options):
        self.tree = tree
        self.lines = lines
        self.options = options

    @staticmethod
    def add_options(optmanager):
        optmanager.add_option(
            "--max-if-conditions",
            type="int",
            metavar="n",
            default=DEFAULT_MAX_IF_CONDITIONS,
            parse_from_config=True,
        )

    def run(self):
        tree = ast.fix_missing_locations(self.tree)

        visitor = AstVisitor()
        visitor.lookup(tree)

        for result in visitor.results:
            fixed_result = self._fix_result_item(result)
            if self._has_if01_error(fixed_result):
                yield self._format_report(IfCheckerErrors.IF01, fixed_result)

    def _fix_result_item(self, result):
        # Add default IF type
        kwargs = result._asdict()
        kwargs["type"] = IfType.IF.value
        result = Result(**kwargs)

        if result.col < self.ELIF_LEN:
            return result

        # Fix ELIF detection, impossible in AST
        code_line = self.lines[result.line - 1]
        substr_from, substr_to = result.col - self.ELIF_LEN, result.col

        if code_line[substr_from:substr_to].startswith("elif"):
            kwargs = result._asdict()
            kwargs["col"] = substr_from
            kwargs["type"] = IfType.ELIF.value
            return Result(**kwargs)

        return result

    def _has_if01_error(self, result):
        return result.condition_count > self.options.max_if_conditions

    def _format_report(self, error, result):
        return (
            result.line,
            result.col,
            error.value.format(**result._asdict()),
            type(self),
        )
