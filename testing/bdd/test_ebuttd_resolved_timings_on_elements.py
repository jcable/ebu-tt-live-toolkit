from pytest_bdd import scenarios, when, then, given, parsers
import xml.etree.ElementTree as ET

scenarios('features/timing/ebuttd_resolved_timings_on_elements.feature')

@then('p resulted begin time is <p_resulted_begin_time>')
def then_it_has_p_resulted_begin_time(test_context, p_resulted_begin_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    p_element = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p')[0]
    document_generated_p_begin_time = p_element.get('begin')
    if (p_resulted_begin_time == 'None'):
        assert document_generated_p_begin_time is None
    else:
        assert p_resulted_begin_time == document_generated_p_begin_time

@then('p resulted end time is <p_resulted_end_time>')
def then_it_has_p_resulted_end_time(test_context, p_resulted_end_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    p_element = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p')[0]
    document_generated_p_end_time = p_element.get('end')
    if (p_resulted_end_time == 'None'):
        assert document_generated_p_end_time is None
    else:
        assert p_resulted_end_time == document_generated_p_end_time

@then('nestedSpan resulted begin time is <nestedSpan_resulted_begin_time>')
def then_it_has_nestedSpan_resulted_begin_time(test_context, nestedSpan_resulted_begin_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    document_generated_span_begin_time = elements[1].get('begin')
    assert nestedSpan_resulted_begin_time == document_generated_span_begin_time

@then('nestedSpan resulted end time is <nestedSpan_resulted_end_time>')
def then_it_has_nestedSpan_resulted_end_time(test_context, nestedSpan_resulted_end_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    document_generated_span_end_time = elements[1].get('end')
    assert nestedSpan_resulted_end_time == document_generated_span_end_time

@then('span1 resulted begin time is <span1_resulted_begin_time>')
def then_it_has_span1_resulted_begin_time(test_context, span1_resulted_begin_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    document_generated_span_begin_time = elements[0].get('begin')
    if span1_resulted_begin_time == 'None':
        assert document_generated_span_begin_time is None
    else:
        assert span1_resulted_begin_time == document_generated_span_begin_time

@then('span2 resulted begin time is <span2_resulted_begin_time>')
def then_it_has_span2_resulted_begin_time(test_context, span2_resulted_begin_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    document_generated_span_begin_time = elements[1].get('begin')
    assert span2_resulted_begin_time == document_generated_span_begin_time

@then('span3 resulted begin time is <span3_resulted_begin_time>')
def then_it_has_span3_resulted_begin_time(test_context, span3_resulted_begin_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    document_generated_span_begin_time = elements[2].get('begin')
    assert span3_resulted_begin_time == document_generated_span_begin_time

@then('span1 resulted end time is <span1_resulted_end_time>')
def then_it_has_span1_resulted_end_time(test_context, span1_resulted_end_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    document_generated_span_end_time = elements[0].get('end')
    assert (span1_resulted_end_time == document_generated_span_end_time
        or span1_resulted_end_time == 'None' and document_generated_span_end_time is None)

@then('span2 resulted end time is <span2_resulted_end_time>')
def then_it_has_span2_resulted_end_time(test_context, span2_resulted_end_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    document_generated_span_end_time = elements[1].get('end')
    assert (span2_resulted_end_time == document_generated_span_end_time
        or span2_resulted_end_time == 'None' and document_generated_span_end_time is None)

@then('span3 resulted end time is <span3_resulted_end_time>')
def then_it_has_span3_resulted_end_time(test_context, span3_resulted_end_time):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    document_generated_span_end_time = elements[2].get('end')
    assert (span3_resulted_end_time == document_generated_span_end_time
        or span3_resulted_end_time == 'None' and document_generated_span_end_time is None)

@then('span2 contains one br')
def then_span2_contains_a_br(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    span_elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p/{http://www.w3.org/ns/ttml}span')
    br = span_elements[1].findall('{http://www.w3.org/ns/ttml}br')
    assert (len(br) == 1)

@then('no timings present on p')
def then_no_timings_present_on_p(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    p_elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p')
    for p_element in p_elements:
        assert 'begin' not in p_element.keys()
        assert 'end' not in p_element.keys()

@then('timings present on p')
def then_timings_present_on_p(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    p_elements = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div/{http://www.w3.org/ns/ttml}p')
    for p_element in p_elements:
        assert 'begin' in p_element.keys()
        assert 'end' in p_element.keys()

@then('no timings present on div')
def then_no_timings_present_on_div(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    divs = tree.findall('{http://www.w3.org/ns/ttml}body/{http://www.w3.org/ns/ttml}div')
    for div in divs:
        assert 'begin' not in div.keys()
        assert 'end' not in div.keys()

@then('no timings present on body')
def then_no_timings_present_on_body(test_context):
    document = test_context['ebuttd_document']
    tree = ET.fromstring(document.get_xml())
    body = tree.findall('{http://www.w3.org/ns/ttml}body')[0]
    assert 'begin' not in body.keys() 
    assert 'end' not in body.keys()