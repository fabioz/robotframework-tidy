.. _InlineIf:

InlineIf
================================
Replaces IF blocks with inline IF.

.. |TRANSFORMERNAME| replace:: InlineIf
.. include:: enabled_hint.txt

It will only replace IF block if it can fit in one line shorter than ``line_length`` parameter (default: ``80`` characters).

Simple IF blocks that will be replaced by inline IF:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            IF    $condition1
                Keyword    argument
            ELSE IF    $condition2
                Keyword    argument2
            END
            IF    $condition2
                RETURN
            END

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            IF    $condition1    Keyword    argument    ELSE IF    $condition2    Keyword    argument2
            IF    $condition2    RETURN

Assignments
------------
Assignments are also supported as long all ELSE and ELSE IF branches have matching return variables and there is ELSE
branch. ELSE branch is required because without it assignment variable would be overwritten with ``None`` without
your consent:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
        # assignment variable but missing ELSE
        IF    $condition
            ${var}    Keyword
        END
        # assignment variables and ELSE branch
        IF    $condition
            ${var}    ${var2}    Keyword
        ELSE
            ${var}    ${var2}    Keyword 2
        END
        # assignment variable and ELSE branch but variable name does not match
        IF    $condition
            ${var}    Keyword
        ELSE
            ${other_var}    Keyword 2
        END

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
        # assignment variable but missing ELSE
        IF    $condition
            ${var}    Keyword
        END
        # assignment variables and ELSE branch
        ${var}    ${var2}    IF    $condition    Keyword    ELSE    Keyword 2
        # assignment variable and ELSE branch but variable name does not match
        IF    $condition
            ${var}    Keyword
        ELSE
            ${other_var}    Keyword 2
        END

Line length
------------
Inline IF will be only used if resulting IF will be shorter than ``line_length`` parameter (default value is ``80``).
Multi statements IF blocks are also skipped:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            FOR    ${var}    IN    @{array}
                # Infline IF would not fit under --line-length
                IF    $condition == "some value"
                    Longer Keyword That Will Not Fit In One Line    ${argument}    ${argument2}
                ELIF    $condition == "other value"
                    Longer Keyword That Will Not Fit In One Line    ${argument3}    ${argument4}
                END
            END
            # multi statements inside IF
            IF    $condition
                Keyword
                Other Keyword
            END

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            FOR    ${var}    IN    @{array}
                # Infline IF would not fit under --line-length
                IF    $condition == "some value"
                    Longer Keyword That Will Not Fit In One Line    ${argument}    ${argument2}
                ELIF    $condition == "other value"
                    Longer Keyword That Will Not Fit In One Line    ${argument3}    ${argument4}
                END
            END
            # multi statements inside IF
            IF    $condition
                Keyword
                Other Keyword
            END

``line_length`` parameter is configurable. Note that ``line_length`` is different than global ``--line-length`` (used
in other transformers such as SplitTooLongLine)::

    robotidy --line-length 80 --configure InlineIf:line_length:140 src.robot

With above configuration ``InlineIf`` will be configured to use ``line_length`` of 140 characters limit and
global ``--line-length`` is set to 80 (and is not used by ``InlineIf``).

Too long inline IF
------------------
Too long inline IFs (over ``line_length`` character limit) will be replaced with normal IF block:

.. tabs::

    .. code-tab:: robotframework Before

        *** Keywords ***
        Keyword
            ${var}    ${var2}    IF    $condition != $condition2    Longer Keyword Name    ${argument}    values    ELSE IF    $condition2    Short Keyword    ${arg}  # comment

    .. code-tab:: robotframework After

        *** Keywords ***
        Keyword
            # comment
            IF    $condition != $condition2
                ${var}    ${var2}    Longer Keyword Name    ${argument}    values
            ELSE IF    $condition2
                ${var}    ${var2}    Short Keyword    ${arg}
            ELSE
                ${var}    ${var2}    Set Variable    ${None}    ${None}    # ELSE branch added to replicate missing ELSE in inline if
            END

Since in above example ``${var}`` and ``${var2}`` variables were used in assignment `Robotidy` added missing ``ELSE`` branch
to set variable values to ``None`` if no other condition matches. If there is ``ELSE`` branch or there is no assignments
in transformed inline IF `Robotidy` will not add it.

Supports global formatting params: ``--startline`` and ``--endline``.