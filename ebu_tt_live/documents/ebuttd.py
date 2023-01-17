import logging
from xml.dom import minidom
from .base import SubtitleDocument, TimeBase
from ebu_tt_live import bindings
from ebu_tt_live.bindings.converters.ebutt3_ebuttd import EBUTT3EBUTTDConverter
from ebu_tt_live.documents.time_utils import TimelineUtilMixin
from datetime import timedelta
log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class EBUTTDDocument(SubtitleDocument, TimelineUtilMixin):

    _ebuttd_content = None
    _implicit_ns = None

    # Encoding to use when creating XML representations
    _encoding = 'UTF-8'

    def __init__(self, lang):
        self.load_types_for_document()
        self._ebuttd_content = bindings.ttd(
            timeBase='media',
            head=bindings.d_head_type(
                styling=bindings.d_styling_type.create_default_value(),
                layout=bindings.d_layout_type.create_default_value()
            ),
            lang=lang
        )

    @property
    def binding(self):
        return self._ebuttd_content

    @property
    def implicit_ns(self):
        return self._implicit_ns

    @implicit_ns.setter
    def implicit_ns(self, value):
        if not isinstance(value, bool):
            raise ValueError()
        self._implicit_ns = value

    def validate(self):
        self._ebuttd_content.validateBinding(
            document=self
        )

    @classmethod
    def load_types_for_document(cls):
        bindings.load_types_for_document('ebuttd')

    @classmethod
    def create_from_xml(cls, xml):
        # NOTE: This is a workaround to make the bindings accept separate root element identities
        # for the same name. tt comes in but we rename it to ttd to make the xsd validate.
        cls.load_types_for_document()
        xml_dom = minidom.parseString(xml)
        if xml_dom.documentElement.tagName == xml_dom.documentElement.prefix + ':tt':
            xml_dom.documentElement.tagName = xml_dom.documentElement.prefix +  ':ttd'
        instance = cls.create_from_raw_binding(
            binding=bindings.CreateFromDOM(
                xml_dom
            )
        )
        return instance

    @classmethod
    def create_from_raw_binding(cls, binding):
        cls.load_types_for_document()
        instance = cls.__new__(cls)
        instance._ebuttd_content = binding
        return instance

    def _get_bds(self):
        if self._implicit_ns:
            return bindings.BindingDOMSupport(
                namespace_prefix_map=bindings.namespace_prefix_map,
                default_namespace=bindings.Namespace
            )
        else:
            return bindings.BindingDOMSupport(
                namespace_prefix_map=bindings.namespace_prefix_map
            )

    def get_xml(self, indent=None, newl=None):
        return str(self._ebuttd_content.toxml(
            encoding=self._encoding,
            bds=self._get_bds(),
            indent=indent,
            newl=newl
        ), encoding=self._encoding)

    def get_dom(self):
        return self._ebuttd_content.toDOM(
            bds=self._get_bds()
        )

    def get_element_by_id(self, elem_id, elem_type=None):
        return self.binding.get_element_by_id(elem_id=elem_id, elem_type=elem_type)
