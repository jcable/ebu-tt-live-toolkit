@styles @document @skip
Feature: Compute fontSize on a single EBU-TT Live element

  Examples:
  | elem_id | style_attribute |  
  | span1   | tts:fontSize    |  

  # Elements referencing styles with different fontSize attribute values
  Scenario: Font size inheritance 
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And it contains style S1 with <style_attribute> value <S1_value>
    And it contains style S2 with <style_attribute> value <S2_value>
    And it contains style S3 with <style_attribute> value <S3_value>
    And it contains style S4 with <style_attribute> value <S4_value>
    And the document is generated
    Then the computed <style_attribute> in <elem_id> is <computed_value>

    Examples:
    | xml_file                      | extent      | cell_resolution | S1_value | S2_value | S3_value | S4_value  | computed_value |  
    | style_attribute_inherited.xml |             | 32 15           | 100%     | 100%     | 100%     | 100%      | 1c             |
    | style_attribute_inherited.xml |             | 32 15           | 50%      | 200%     | 50%      | 200%      | 1c             |  
    | style_attribute_inherited.xml |             | 32 15           | 1c       | 200%     | 100%     | 50%       | 1c             |  
    | style_attribute_inherited.xml |             | 32 15           | 100%     | 2c       | 100%     | 50%       | 1c             |  
    | style_attribute_inherited.xml |             | 10 10           | 100%     |          |          | 50%       | .5c            |
    | style_attribute_inherited.xml | 100px 100px | 10 10           | 1c 2c    | 100% 50% | 5px 20px | 200% 50%  | 1c 1c          |
    | style_attribute_inherited.xml |             | 10 10           |          | 50%      |          | 400%      | 2c             |
    | style_attribute_inherited.xml |             | 10 10           | 1c 2c    | 100% 50% | 50% 100% | 200% 100% | 1c 1c          |
    | style_attribute_inherited.xml | 100px 100px |                 |          | 10px     | 200%     | 50%       | 1.5c           |
