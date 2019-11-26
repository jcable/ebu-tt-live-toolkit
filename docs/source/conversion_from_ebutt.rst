Conversion of EBU-TT Part 1 documents to EBU-TT Live documents
==============================================================

The :py:func:`ebu_tt_live.documents.converters.ebutt1_to_ebutt3` function
creates an EBUTT3Document from an EBUTT1Document using the helper class
:py:class:`ebu_tt_live.bindings.converters.ebutt1_ebutt3.EBUTT1EBUTT3Converter`.

This class manages various possible complications, including mapping SMPTE
timecodes into media time, and setting a sequence identifier. 

Here's some documentation from the coding process that captures some of our
internal conversation about how to map font sizes, to give an idea of the
complexity.

The problem
-----------

Convert an EBU-TT part 1 document to an EBU-TT part 3 document

EBU-TT part 1 can have smpte timebase; EBU-TT part 3 cannot.
EBU-TT part 1 must not have a sequence identifier and must not
have a sequence number. EBU-TT part 3 documents must have both.

In order to set the sequence identifier the converter can be
configured with the desired value, or it can be set to extract the
document identifier from the `ebuttm:documentIdentifier` element
and use it, if it exists.

TODO: how to convert smpte timebase time expressions into clock or media
timebase time expressions.