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
    When the document has metadata "ebuttm:documentIdentifier" set to "ABC1234"
    And the XML is parsed as an EBU-TT-1 document
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the tt element contains the attribute "ebuttp:sequenceIdentifier" set to "ABC1234"

  Scenario: Replace ebuttm namespace for copyright to ttm
    Given an xml file <xml_file>
    When the document has metadata "ebuttm:documentCopyright" set to "EBU"
    And the XML is parsed as an EBU-TT-1 document
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the head element contains the element "ttm:copyright" set to "EBU"
    And documentMetadata element "ebuttm:documentCopyright" has been removed

  Scenario: ttm:copyright takes precedence over ebuttm:documentCopyright
    Given an xml file <xml_file>
    When the document has metadata "ebuttm:documentCopyright" set to "EBU"
    And the document head has element "ttm:copyright" set to "Joe Bloggs"
    And the XML is parsed as an EBU-TT-1 document
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the head element contains the element "ttm:copyright" set to "Joe Bloggs"
# And documentMetadata element "ebuttm:documentCopyright" has been removed
