
from ebu_tt_live.bindings.converters.ebutt3_ebuttd import EBUTT3EBUTTDConverter
from ebu_tt_live.bindings.converters.ebutt1_ebutt3 import EBUTT1EBUTT3Converter

from ebu_tt_live.documents.ebuttd import EBUTTDDocument
from ebu_tt_live.documents.ebutt1 import EBUTT1Document
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from subprocess import Popen, PIPE
import tempfile
import os
import logging


log = logging.getLogger(__name__)


def ebutt3_to_ebuttd(ebutt3_in, media_clock):
    """
    This function takes an EBUTT3Document instance and returns the same document as an EBUTTDDocument instance.
    :param ebutt3_in:
    :return:
    """

    converter = EBUTT3EBUTTDConverter(media_clock=media_clock)
    # Here we need a thing that makes sure that the times in the input 
    # document do not depend on a body@dur attribute, and that they are
    # absolutised, so a body with no begin or end time but with a dur
    # gets fixed into a body with an end time, which gives the
    # denester an easier job.
    doc_xml = ebutt3_in.get_xml()
    ebutt3_doc = EBUTT3Document.create_from_xml(doc_xml)
    ebuttd_bindings = converter.convert_document(ebutt3_doc.binding)
    ebuttd_document = EBUTTDDocument.create_from_raw_binding(ebuttd_bindings)
    ebuttd_document.validate()
    return ebuttd_document


def ebutt1_to_ebutt3(ebutt1_in):
    """
    This function takes an EBUTT1Document instance and returns the same document as an EBUTT3Document instance.
    :param ebutt1_in:
    :return:
    """
    converter = EBUTT1EBUTT3Converter()
    doc_xml = ebutt1_in.get_xml()
    ebutt1_doc = EBUTT1Document.create_from_xml(doc_xml)
    ebutt3_bindings = converter.convert_document(ebutt1_doc.binding)
    ebutt3_document = EBUTT3Document.create_from_raw_binding(ebutt3_bindings)
    ebutt3_document.validate()
    return ebutt3_document
