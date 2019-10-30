import copy
import logging

from pyxb.binding import datatypes
from pyxb.binding.basis import ElementContent, NonElementContent

from ebu_tt_live.bindings import (body_type, head_type, layout,
                                  load_types_for_document, tt, tt1_body_type,
                                  tt1_head_type, tt1_layout_type, tt1_tt_type, styling)
from ebu_tt_live.bindings._ebuttm import headMetadata_type

log = logging.getLogger(__name__)


class EBUTT1EBUTT3Converter(object):

    def __init__(self):
        pass

    def map_type(self, in_element):
        if isinstance(in_element, tt1_tt_type):
            return self.convert_tt
        elif isinstance(in_element, tt1_head_type):
            return self.convert_head
        elif isinstance(in_element, tt1_body_type):
            return self.convert_body
        elif isinstance(in_element, headMetadata_type):
            return self.convert_metadata
        elif isinstance(in_element, styling):
            return self.convert_unchanged
        elif isinstance(in_element, tt1_layout_type):
            return self.convert_layout
        elif isinstance(in_element, datatypes.string):
            return self.convert_unchanged
        else:
            log.warn('Type %s being ignored' % type(in_element))
            return self.convert_unknown

    def convert_tt(self, tt_in, dataset):
        dataset['timeBase'] = tt_in.timeBase

        # Add sequence identifier which can be taken from document metadata
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
            head=self.convert_element(tt_in.head, dataset),
            body=self.convert_element(tt_in.body, dataset),
            lang=tt_in.lang,
            space=tt_in.space,
            sequenceIdentifier=document_identifier,
            sequenceNumber=1,
            timeBase=tt_in.timeBase,
            frameRate=tt_in.frameRate,
            frameRateMultiplier=tt_in.frameRateMultiplier,
            dropMode=tt_in.dropMode,
            markerMode=tt_in.markerMode,
        )
        return new_elem

    def convert_head(self, head_in, dataset):
        new_elem = head_type()

        # Set ttm:copyright if ebuttm:documentCopyright exists
        if not(head_in.copyright) and head_in.metadata:
            if hasattr(head_in.metadata, 'documentMetadata') and \
                    hasattr(head_in.metadata.documentMetadata, 'documentCopyright'):
                new_elem.copyright = head_in.metadata.documentMetadata.documentCopyright
                head_in.metadata.documentMetadata.documentCopyright = None
            elif hasattr(head_in.metadata, 'documentCopyright'):
                new_elem.copyright = head_in.metadata.documentCopyright
                head_in.metadata.documentCopyright = None

        head_children = self.convert_children(head_in, dataset)
        for item in head_children:
            if isinstance(item, styling):
                new_elem.styling = item
            elif isinstance(item, layout):
                new_elem.layout = item
            elif isinstance(item, headMetadata_type):
                new_elem.metadata = item
            else:
                new_elem.append(item)
        return new_elem

    def remove_metadata(self, metadata_in, element_name):
        if hasattr(metadata_in, 'documentMetadata') and hasattr(metadata_in.documentMetadata, element_name):
            setattr(metadata_in.documentMetadata, element_name, None)
        if hasattr(metadata_in, element_name):
            setattr(metadata_in, element_name, None)

    def convert_metadata(self, metadata_in, dataset):
        unnecessary_elements = [
            'documentReadingSpeed',
            'binaryData',
            'documentOriginalProgrammeTitle',
            'documentOriginalEpisodeTitle',
            'documentTranslatedProgrammeTitle',
            'documentTranslatedEpisodeTitle',
            'documentTotalNumberOfSubtitles',
            'documentMaximumNumberOfDisplayableCharacterInAnyRow',
            'documentSubtitleListReferenceCode',
            'documentStartOfProgramme',
        ]
        for e in unnecessary_elements:
            self.remove_metadata(metadata_in, e)
        return metadata_in

    def convert_layout(self, layout_in, dataset):
        new_elem = layout()
        dataset['ids'] = set()
        new_elem.merge(layout_in, dataset)
        return new_elem

    def convert_body(self, body_in, dataset):
        return body_in

    def convert_unchanged(self, element, dataset):
        return element

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
