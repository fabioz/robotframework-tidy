.. _external-transformers:

External transformers
-------------------------------
It is possible to develop your own transformers. You can use module name (if it is installed in your env) or path to
file with class to run external transformers with *robotidy*::

    robotidy --transform MyTransformers.YourCustomTransformer src
    robotidy --transform C:\transformers\YourCustomTransformer2.py src

External transformers can be configured in the same way internal transformers are configured - see :ref:`configuring-transformers`.

You can use the same syntax ``robotidy`` is using for developing internal transformers. The name of the file should
be the same as name of the class containing your transformer. Your transformer should inherit from ``robot.api.parsing.ModelTransformer``
parent class.

  .. code-block:: python

    from robot.api.parsing import ModelTransformer


    class YourCustomTransformer(ModelTransformer):
        """
        This transformer will remove tests with
        word "deprecated" in the test case name
        """
        def visit_TestCase(self, node):
            if 'deprecated' in node.name:
                return None
            return node

Configurable params should be supplied through ``__init__`` together with the type and default value

  .. code-block:: python

    from robot.api.parsing import EmptyLine, ModelTransformer


    class ExternalTransformer(ModelTransformer):
        """
        This transformer add `param` number of empty lines at the end of
        *** Settings *** section.
        """
        def __init__(self, param: int = 10):
            self.param = param

        def visit_SettingSection(self, node):  # noqa
            empty_line = EmptyLine.from_params()
            node.body += [empty_line] * self.param
            return node
