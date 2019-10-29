Feature: Files converted from EBU-TT-1 to EBU-TT-3 are valid
    Examples:
      | xml_file           |
      | ebutt1_example.xml |

  Scenario: Converted TT3 document contains required attributes
    Given an xml file <xml_file>
    When the XML is parsed as an EBU-TT-1 document
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the tt element contains the attribute "ebuttp:sequenceNumber" set to "1"

  Scenario: sequenceIdentifier attribute taken from documentIdentifier in metadata
    Given an xml file <xml_file>
    When the document has metadata "documentIdentifier" set to "ABC1234"
    And the XML is parsed as an EBU-TT-1 document
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the tt element contains the attribute "ebuttp:sequenceIdentifier" set to "ABC1234"
