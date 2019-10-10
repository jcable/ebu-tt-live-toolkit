from .base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3Document


class EBUTT1EBUTT3ProducerNode(AbstractCombinedNode):

    _ebutt3_converter = None
    _expects = EBUTT3Document  # TODO change to EBUTT1 when we create that class
    _provides = EBUTT3Document

    def __init__(self, node_id, consumer_carriage=None, producer_carriage=None, **kwargs):
        super(EBUTT1EBUTT3ProducerNode, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage,
            producer_carriage=producer_carriage,
            **kwargs
        )

    def process_document(self, document, **kwargs):
        self.producer_carriage.emit_data(document, **kwargs)
