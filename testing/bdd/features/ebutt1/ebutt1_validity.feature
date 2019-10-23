Feature: Parsing EBU-TT Part 1 files
  Examples:
    | xml_file            |
    | ebutt1_template.xml |

  Scenario: Pass validity check
    Given an xml file <xml_file>
    When the document contains a "styling" element
    And the document contains a "style" element
    And the document contains a "layout" element
    And the document contains a "region" element
    When the XML is parsed as an EBU-TT-1 document
    Then the EBU-TT-1 document is valid

  Scenario: EBU-TT-1 must contain "styling"
    Given an xml file <xml_file>
    When the document contains a "layout" element
    And the document contains a "region" element
    Then the document fails to parse as an EBU-TT-1 document because of an IncompleteElementContentError

  Scenario: Styling without a style element are invalid
    Given an xml file <xml_file>
    When the document contains a "styling" element
    And the document contains a "layout" element
    And the document contains a "region" element
    Then the document fails to parse as an EBU-TT-1 document because of an IncompleteElementContentError

  Scenario: EBU-TT-1 must contain "layout"
    Given an xml file <xml_file>
    When the document contains a "styling" element
    And the document contains a "style" element
    Then the document fails to parse as an EBU-TT-1 document because of an IncompleteElementContentError

  Scenario: Layouts without a region element are invalid
    Given an xml file <xml_file>
    When the document contains a "styling" element
    And the document contains a "style" element
    And the document contains a "layout" element
    Then the document fails to parse as an EBU-TT-1 document because of an IncompleteElementContentError

  Scenario: Body elements with a "dur" attribute are not allowed
    Given an xml file <xml_file>
    When the document contains a "styling" element
    And the document contains a "style" element
    And the document contains a "layout" element
    And the document contains a "region" element
    And the document body contains a "dur" attribute
    Then the document fails to parse as an EBU-TT-1 document because of an UnrecognizedAttributeError
