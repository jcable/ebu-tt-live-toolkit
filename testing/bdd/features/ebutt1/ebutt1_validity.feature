Feature: Parsing EBU-TT Part 1 files
  Examples:
    | xml_file            |
    | ebutt1_template.xml |

  Scenario: Pass validity check
    Given an xml file <xml_file>
    When the document contains a "styling" element
    And the document contains a "layout" element
    When the XML is parsed as an EBU-TT-1 document
    Then the EBU-TT-1 document is valid

  Scenario: EBU-TT-1 must contain "styling"
    Given an xml file <xml_file>
    When the document contains a "layout" element
    Then the document fails to parse as an EBU-TT-1 document because of an IncompleteElementContentError

  # TODO what about a layout with no regions?

  Scenario: EBU-TT-1 must contain "layout"
    Given an xml file <xml_file>
    When the document contains a "styling" element
    Then the document fails to parse as an EBU-TT-1 document because of an IncompleteElementContentError
