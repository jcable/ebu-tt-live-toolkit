from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttlm as ebuttlm
from ebu_tt_live.documents import SubtitleDocument


class EBUTT1ObjectBase(object):
    message_type_mapping = {}

    def get_xml(self):
        raise NotImplementedError()

    def get_dom(self):
        raise NotImplementedError()

    @classmethod
    def create_from_xml(cls, xml):
        instance = bindings.CreateFromDocument(
            xml_text=xml
        )
        if isinstance(instance, ebuttlm.message_type):
            return cls.message_type_mapping[instance.header.type].create_from_raw_binding(instance)

    @classmethod
    def create_from_raw_binding(cls, **kwargs):
        raise NotImplementedError()


class TimelineUtilMixin(object):

    def add_to_timeline(self, element):
        pass


class EBUTT1Document(TimelineUtilMixin, SubtitleDocument, EBUTT1ObjectBase):
    """
    This class wraps the binding object representation of the XML and provides the features the applications in the
    specification require.
    """

    # The XML binding holding the content of the document
    _ebutt1_content = None

    def _cmp_key(self):
        raise NotImplementedError()

    def __init__(self):
        self.load_types_for_document()
        self._ebutt1_content = bindings.tt()
        self.validate()

    def validate(self):
        # Run validation

        result = self._ebutt1_content.validateBinding(
            availability_time=None,
            document=self
        )

    @classmethod
    def create_from_raw_binding(cls, binding):
        cls.load_types_for_document()
        instance = cls.__new__(cls)
        instance._ebutt1_content = binding
        instance.validate()
        return instance

    @classmethod
    def create_from_xml(cls, xml):
        cls.load_types_for_document()
        instance = cls.create_from_raw_binding(binding=bindings.CreateFromDocument(xml_text=xml))
        return instance

    @classmethod
    def load_types_for_document(cls):
        bindings.load_types_for_document('ebutt1')

    @property
    def lang(self):
        return self._ebutt1_content.lang

    @property
    def clock_mode(self):
        return self._ebutt1_content.clockMode

    def add_div(self, div):
        body = self._ebutt1_content.body
        body.append(div)

    def set_begin(self, begin):
        self._ebutt1_content.body.begin = begin

    def set_end(self, end):
        self._ebutt1_content.body.end = end

    def set_dur(self, dur):
        self._ebutt1_content.body.dur = dur

    @property
    def binding(self):
        return self._ebutt1_content

    def get_xml(self):
        return self._ebutt1_content.toxml()

    def get_dom(self):
        return self._ebutt1_content.toDOM()

    def get_element_by_id(self, elem_id, elem_type=None):
        return self.binding.get_element_by_id(elem_id=elem_id, elem_type=elem_type)
