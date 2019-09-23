Feature: EBU-TT lengthType validation

    If pixel units are used in regions but 'extent' has not been specified on the tt:tt element, the document is invalid.

    Examples:
        | xml_file                     |
        | style_element_references.xml |

    Scenario: throw an error and stop the processing if no pixel value for tts:extent is supplied on the tt:tt element
        Given an xml file <xml_file>
        When the document does not specify an extent
        And it contains region "r1"
        And region "r1" has attribute <attribute> set to "200px 360px"
        And it contains some text with region "r1"
        Then document is invalid

        Examples:
            | attribute |
            | origin    |
            | extent    |
