import logging

log = logging.getLogger(__name__)


class EBUTT1EBUTT3Converter(object):

    def __init__(self):
        pass

    def map_type(self, in_element):
        return self.convert_unknown

    def convert_unknown(self, element, dataset):
        return None

    def convert_element(self, element, dataset):
        converter = self.map_type(element)
        return converter(element, dataset)

    def convert_document(self, root_element, dataset=None):
        if dataset is None:
            self._semantic_dataset = {}
        else:
            self._semantic_dataset = dataset
        converted_bindings = self.convert_element(
            root_element,
            self._semantic_dataset
        )

        return converted_bindings
