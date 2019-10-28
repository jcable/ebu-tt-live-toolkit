import copy
import logging

from ebu_tt_live.bindings import load_types_for_document, tt1_tt_type, tt
from pyxb.binding.basis import ElementContent, NonElementContent

log = logging.getLogger(__name__)


class EBUTT1EBUTT3Converter(object):

    def __init__(self):
        pass

    def map_type(self, in_element):
        if isinstance(in_element, tt1_tt_type):
            return self.convert_tt
        else:
            return self.convert_unknown

    def convert_tt(self, tt_in, dataset):
        document_identifier = 'sequence'
        if hasattr(tt_in, 'head') and hasattr(tt_in.head, 'metadata'):
            if hasattr(tt_in.head.metadata, 'documentMetadata') and \
                hasattr(tt_in.head.metadata.documentMetadata, 'documentIdentifier') and \
                    tt_in.head.metadata.documentMetadata.documentIdentifier:
                document_identifier = tt_in.head.metadata.documentMetadata.documentIdentifier
            elif hasattr(tt_in.head.metadata, 'documentIdentifier') and \
                    tt_in.head.metadata.documentIdentifier:
                document_identifier = tt_in.head.metadata.documentIdentifier

        new_elem = tt(
            sequenceIdentifier=document_identifier,
            sequenceNumber=1,
        )
        return new_elem


    def convert_unknown(self, element, dataset):
        return None

    def convert_children(self, element, dataset):
        output = []
        children = element.orderedContent()
        for item in children:
            if isinstance(item, NonElementContent):
                output.append(copy.deepcopy(item.value))
            elif isinstance(item, ElementContent):
                conv_elem = self.convert_element(item.value, dataset)
                if conv_elem is not None:
                    output.append(conv_elem)
            else:
                raise Exception('Can this even happen!??!?!?!')
        return output

    def convert_element(self, element, dataset):
        converter = self.map_type(element)
        return converter(element, dataset)

    def convert_document(self, root_element, dataset=None):
        if dataset is None:
            self._semantic_dataset = {}
        else:
            self._semantic_dataset = dataset

        load_types_for_document('ebutt3')

        converted_bindings = self.convert_element(
            root_element,
            self._semantic_dataset
        )

        return converted_bindings
