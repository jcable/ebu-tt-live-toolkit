Feature: EBU-TT-D lineHeight conversion

    On converting to EBU-TT-D, lineHeight values must be translated into percentages.

    Examples:
        | xml_file                     |
        | style_element_references.xml |

    Scenario: The value of tts:lineHeight shall be recalculated and expressed in percentage
        Given an xml file <xml_file>
        When it contains style "s1"
        And style "s1" has attribute "lineHeight" set to <lineHeight>
        And style "s1" has attribute "fontSize" set to <fontSize>
        And it contains some text with style "s1"
        When the document is generated
        And the EBU-TT-Live document is converted to EBU-TT-D
        Then the ebu_tt_d document contains style "autogenFontStyle_None_200.0" with attribute "lineHeight" set to <ebu_tt_d_value>

        Examples:
            | lineHeight | fontSize | ebu_tt_d_value |
            | 2c         | 2c       | 100.0%         |