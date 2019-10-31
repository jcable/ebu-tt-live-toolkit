Feature: When converting from EBU-TT-1 to EBU-TT-3, timings will be converted to media time

    Examples:
      | xml_file           |
      | ebutt1_timings.xml |

  Scenario: Convert to media timeBase
    Given an xml file <xml_file>
    When the tt element has attribute "ttp:timeBase" set to <timebase>
    And the tt element has attribute "ttp:frameRate" set to "25"
    And the tt element has attribute "ttp:frameRateMultiplier" set to "1 1"
    And the tt element has attribute "ttp:markerMode" set to "discontinuous"
    And the document has metadata "ebuttm:documentStartOfProgramme" set to <startOfProgramme>
    And p element has "begin" time set to <in_begin> and "end" time set to <in_end>
    And the XML is parsed as an EBU-TT-1 document
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the tt element contains the attribute "ttp:timeBase" set to "media"
    And p element has "begin" time set to <out_begin> and "end" time set to <out_end>
    And documentMetadata element "ebuttm:documentStartOfProgramme" has been removed

    Examples:
      | timebase | startOfProgramme | in_begin    | in_end      | out_begin | out_end  |
      | smpte    | 10:00:00:00      | 10:00:01:00 | 10:00:02:00 | 00:00:01  | 00:00:02 |


#Scenario: Reject if timeBase is smpte but wrong marker mode
