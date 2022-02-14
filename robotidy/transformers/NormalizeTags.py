from robot.api.parsing import ModelTransformer, Tags, Token, DefaultTags, ForceTags

from robotidy.exceptions import InvalidParameterValueError


class NormalizeTags(ModelTransformer):
    """
    Normalize tag names by normalizing case and removing duplicates.

    Example usage:

        robotidy --transform NormalizeTags:case=lowercase test.robot

    Other supported cases: uppercase, title case. The default is lowercase.

    You can also run it to remove duplicates but preserve current case by setting ``normalize_case`` parameter to False:

        robotidy --transform NormalizeTags:normalize_case=False test.robot

    See https://robotidy.readthedocs.io/en/latest/transformers/NormalizeTags.html for more examples.
    """

    CASE_FUNCTIONS = {
        "lowercase": str.lower,
        "uppercase": str.upper,
        "titlecase": str.title,
    }

    def __init__(self, case: str = "lowercase", normalize_case: bool = True):
        self.case = case.lower()
        self.normalize_case = normalize_case
        try:
            self.case_function = self.CASE_FUNCTIONS[self.case]
        except KeyError:
            raise InvalidParameterValueError(
                self.__class__.__name__, "case", case, "Supported cases: lowercase, uppercase, titlecase."
            )

    def generate_config(self):
        from robotidy.generate_config import TransformerConfig, ParameterSelectSingle, ParameterBool

        config = TransformerConfig(
            name=self.__class__.__name__,
            enabled=self.__dict__.get("ENABLED", True),
            msg="""
            Do you want to normalize tag names? 
            Case will be normalized and duplicates will be removed (tags in Robot Framework are case insensitive).
            Following code:
            
                *** Settings ***
                Default Tags    tag1    Tag2    TAG3    tag3
            
            will be transformed to:
            
                *** Settings ***
                Default Tags    tag1    tag2    tag3
            
            """,
        )
        if not config.enabled:
            return config

        normalize_case = ParameterBool(
            "If you only want to remove duplicates, set `normalize_case` to False:",
            "normalize_case",
            self.normalize_case,
            "Normalize case",
            "Don't normalize case",
        )
        config.parameters.append(normalize_case)
        if normalize_case.value is None and normalize_case.default or normalize_case.value:
            case = ParameterSelectSingle(
                "You can select which case function will be applied to tags (lowercase by default):",
                param="case",
                default="lowercase",
                choices={k: k for k in self.CASE_FUNCTIONS},
            )
            config.parameters.append(case)
        return config

    def visit_Tags(self, node):  # noqa
        return self.normalize_tags(node, Tags, indent=True)

    def visit_DefaultTags(self, node):  # noqa
        return self.normalize_tags(node, DefaultTags)

    def visit_ForceTags(self, node):  # noqa
        return self.normalize_tags(node, ForceTags)

    def normalize_tags(self, node, tag_class, indent=False):
        tags = [tag.value for tag in node.data_tokens[1:]]
        if self.normalize_case:
            tags = self.convert_case(tags)
        tags = self.remove_duplicates(tags)
        comments = node.get_tokens(Token.COMMENT)
        if indent:
            tag_node = tag_class.from_params(
                tags,
                indent=self.formatting_config.separator,
                separator=self.formatting_config.separator,
            )
        else:
            tag_node = tag_class.from_params(tags, separator=self.formatting_config.separator)
        if comments:
            tag_node.tokens = tag_node.tokens[:-1] + tuple(self.join_tokens(comments)) + (tag_node.tokens[-1],)
        return tag_node

    def convert_case(self, tags):
        return [self.case_function(item) for item in tags]

    @staticmethod
    def remove_duplicates(tags):
        return list(dict.fromkeys(tags))

    def join_tokens(self, tokens):
        joined_tokens = []
        for token in tokens:
            joined_tokens.append(Token(Token.SEPARATOR, self.formatting_config.separator))
            joined_tokens.append(token)
        return joined_tokens
