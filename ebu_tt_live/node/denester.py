from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings import div_type, p_type, span_type, ebuttdt, style_type
from ebu_tt_live.bindings._ebuttm import divMetadata_type
import copy
import re
from datetime import timedelta

class Denester():
    """
    This class contains methods for unnesting elements of an EBUTT3Document that cannot be nested in EBUTTD
    """
            
    @staticmethod
    def denest(document):
        divs = document.binding.body.div
        unnested_divs = []
        dataset = {}
        if document.binding.head.styling is not None:
            dataset["styles"] = document.binding.head.styling.style
        else:
            dataset["styles"] = []
        dataset["document"] = document.binding
        for div in divs:
            unnested_divs.extend(Denester.recurse(div,dataset))
        unnested_divs = Denester.combine_divs(unnested_divs)
        unnested_divs = Denester.check_p_regions(unnested_divs)
        document.binding.body.div = unnested_divs
        return document

    @staticmethod
    def check_p_regions(divs):
        """
        Keeps only P elements where the region matches the div region or is None
        Then removes region from remaining P elements as it will be the same as the div region
        """

        for div in divs:
            if div.region is not None:
                div.p = [p for p in div.p if p.region == div.region or p.region == None]
                for p in div.p:
                    p.region = None

        # Removes divs that no longer contain any P elements
        divs = [div for div in divs if div.p != []]

        return divs

    @staticmethod
    def combine_divs(divs):
        """
        Takes the list of unnested divs, where one was created to contain each P elements, and attempts to combine them
        A list of new divs is created, the first element being the first div in the list of divs passed in
        Iterating through the passed in divs, where a div has the same attributes as the previous one,
            add its P list to the current new div's P list
        Where the current div does not match, add it to the list of new divs and increment j, making it the current new div
        """
        new_divs = []
        if len(divs) != 0:
            new_divs.append(divs[0])
            i = 1
            j = 0
            while i < len(divs):
                if Denester.div_attr(divs[i]) == Denester.div_attr(divs[i-1]):
                    new_divs[j].p.extend(divs[i].p)
                else:
                    j += 1
                    new_divs.append(divs[i])
                i += 1
        return new_divs



    @staticmethod
    def div_attr(div):
        div_attributes =  {}
        div_attributes["styles"]=div.style
        div_attributes["lang"] = div.lang
        div_attributes["region"] = div.region
        div_attributes["begin"] = div.begin
        div_attributes["end"] = div.end
        return div_attributes
    
    @staticmethod
    def merge_attr(parent_attr, div_attributes):
        merged_attributes ={ "styles": [], "begin": None, "end": None, "lang": None, "region": None }

        if not isinstance(parent_attr["begin"], timedelta) and parent_attr["begin"] is not None:
            parent_attr["begin"] = parent_attr["begin"].timedelta
        if not isinstance(parent_attr["end"], timedelta) and parent_attr["end"] is not None:
            parent_attr["end"] = parent_attr["end"].timedelta
        if not isinstance(div_attributes["begin"], timedelta) and div_attributes["begin"] is not None:
            div_attributes["begin"] = div_attributes["begin"].timedelta
        if not isinstance(div_attributes["end"], timedelta) and div_attributes["end"] is not None:
            div_attributes["end"] = div_attributes["end"].timedelta

        if div_attributes["styles"] is not None:
             merged_attributes["styles"] = div_attributes["styles"] + parent_attr["styles"]
        else:
            merged_attributes["styles"] = parent_attr["styles"]
        if div_attributes["lang"] is not None:
            merged_attributes["lang"] = div_attributes["lang"]
        else:
            merged_attributes["lang"] = parent_attr["lang"]
        if parent_attr["region"] is not None:
            merged_attributes["region"] = parent_attr["region"]
        elif div_attributes["region"] is not None:
            merged_attributes["region"] = div_attributes["region"]
        if parent_attr["begin"] is not None and div_attributes["begin"] is not None:
            merged_attributes["begin"] = parent_attr["begin"] + div_attributes["begin"]
        elif parent_attr["begin"] is not None and div_attributes["begin"] is None:
            merged_attributes["begin"] = parent_attr["begin"]
        elif parent_attr["begin"] is None and div_attributes["begin"] is None:
            merged_attributes["begin"] = None
        else:
            merged_attributes["begin"] = div_attributes["begin"] if parent_attr["begin"] is None else parent_attr["begin"]
        if parent_attr["end"] is not None and div_attributes["end"] is not None:
            merged_attributes["end"] = parent_attr["end"] - div_attributes["end"]
        elif parent_attr["end"] is not None and div_attributes["end"] is None:
            merged_attributes["end"] = parent_attr["end"]
        else:
            merged_attributes["end"] = Denester.calculate_end_times(parent_attr, div_attributes, parent_attr["begin"])
        return merged_attributes

    @staticmethod
    def calculate_end_times(parent_attr, child_attr, time_sync):
        if child_attr["end"] is not None and parent_attr["end"] is None and time_sync is not None:
           return time_sync+child_attr["end"]
        elif parent_attr["end"] is not None and child_attr["end"] is not None:
             return parent_attr["end"]-child_attr["end"]
        else:
            return child_attr["end"]
    
    @staticmethod
    def process_timing_from_timedelta(timing_type):
        if timing_type is None:
            return None
        return ebuttdt.FullClockTimingType.from_timedelta(timing_type)
    
    @staticmethod
    def recurse( div, dataset, merged_attr={"styles": [], "begin": None, "end": None, "lang": None, "region": None }):
        merged_attr = Denester.merge_attr(merged_attr, Denester.div_attr(div))
        new_divs = []
        for c in div.orderedContent():
            if isinstance(c.value,div_type):
                if(div.region != c.value.region and c.value.region !=None and div.region !=None):
                    continue
                new_divs.extend(Denester.recurse(c.value, dataset, merged_attr))
            elif isinstance(c.value,divMetadata_type):
                continue
            else:
                new_spans = []
                for ic in c.value.orderedContent():
                    if isinstance(ic.value,span_type):
                        new_spans.extend(Denester.recurse_span(ic.value,dataset))
                c.value.span = new_spans
                for span in c.value.span:
                    # The following lines address some test cases but are not a
                    # general solution, so commented out, however see comments
                    # on line immediately below.
                    # if c.value.begin is not None:
                    #     p_time = c.value.computed_begin_time
                    # else:
                    #     p_time = div.computed_begin_time

                    # The following line fails if the parent p element's computed 
                    # begin time has
                    # been advanced to its earliest child's computed begin time
                    # and the p's parent div has a different computed begin time.
                    # This situation arises especially when the body element has
                    # a dur but no begin or end times. This may well be some kind
                    # of bug or incorrect behaviour, but it's hard to sort out
                    # without breaking a bunch of stuff.
                    p_time = c.value.computed_begin_time
                    
                    span.compBegin = span.compBegin - p_time
                    span.compEnd = span.compEnd - p_time

                    span.begin = ebuttdt.FullClockTimingType(span.compBegin)
                    span.end = ebuttdt.FullClockTimingType(span.compEnd)

                new_div = div_type(
                    id=div.id,
                    style=None if len(merged_attr["styles"]) == 0  else merged_attr["styles"],
                    begin=Denester.process_timing_from_timedelta(merged_attr["begin"]) if merged_attr["begin"] is not None else merged_attr["begin"],
                    end=Denester.process_timing_from_timedelta(merged_attr["end"]) if merged_attr["end"] is not None else merged_attr["end"],
                    lang=merged_attr["lang"],
                    region=merged_attr["region"],
                )   
                new_div.p.append(c.value)
                new_divs.append(new_div)
        
        return new_divs

    @staticmethod
    def recurse_span(span, dataset, span_styles = []):
        if span.style is not None:
            span_styles = span_styles+span.style
        new_spans = []
        for sc in span.orderedContent():
            if isinstance(sc.value,span_type):
                new_spans.extend(Denester.recurse_span(sc.value, dataset, span_styles))
            else:
                new_span = span_type(
                    sc.value
                )
                
                new_span.compBegin = span.computed_begin_time
                new_span.compEnd = span.computed_end_time

                if len(span_styles) != 0:
                    new_span.style = Denester.compute_span_merged_styles(span_styles, dataset).id if len(span_styles) >1 else span_styles
                else:
                    new_span.style = None
                new_spans.append(new_span)
        return new_spans
                
    @staticmethod
    def compute_span_merged_styles(span_styles, dataset):
        new_style = None
        styles = []
        for style_name in span_styles: # go through styles in xml
            for style in dataset["styles"]:
                if style.id == style_name:
                    styles.append(style)
        new_style = style_type(
            id="".join(span_styles),
            backgroundColor=Denester.get_value_from_style(styles, "backgroundColor"),
            color=Denester.get_value_from_style(styles, "color"),
            fontFamily=Denester.get_value_from_style(styles, "fontFamily"),
            fontSize=Denester.calculate_font_size(styles),
            fontWeight=Denester.get_value_from_style(styles, "fontWeight"),
            lineHeight=Denester.get_value_from_style(styles, "lineHeight"),
            linePadding=Denester.get_value_from_style(styles, "linePadding"),
            padding=Denester.get_value_from_style(styles, "padding"),
            style=Denester.get_value_from_style(styles, "style"),
            textAlign=Denester.get_value_from_style(styles, "textAlign"),
            textDecoration=Denester.get_value_from_style(styles, "textDecoration")
        )
        new_style = Denester.create_new_style(new_style, dataset)
        return new_style

    @staticmethod
    def create_new_style(new_style, dataset):
        for style in dataset["styles"]:
            if new_style.id == style.id:
                return new_style
            if new_style.check_equal(style):
                new_style.id = style.id
                return new_style
        dataset["styles"].append(new_style)
        return new_style

    @staticmethod
    def calculate_font_size(styles):
        font_size = None

        for style in styles:
            if font_size is None: # No existing font size
                font_size = style.fontSize

            elif isinstance(style.fontSize, ebuttdt.percentageFontSizeType) == False and style.fontSize is not None: # Font size is in c/px
                font_size = style.fontSize

            elif isinstance(style.fontSize, ebuttdt.percentageFontSizeType) and font_size is not None:
                # Font size in percent, there is an existing font size (may not be percent)
                font_size = Denester.calculate_percentage_font_size(font_size, style.fontSize)

        return font_size

            
    @staticmethod
    def calculate_percentage_font_size(current_font_size, nested_font_size):
        if isinstance(current_font_size, ebuttdt.percentageFontSizeType):
            stripped_current_font_size = current_font_size.strip("%")
            stripped_nested_font_size = nested_font_size.strip("%")
            calculated_font_size = float(stripped_nested_font_size) * (float(stripped_current_font_size)/100)

            return ebuttdt.percentageFontSizeType('{0:g}%'.format(calculated_font_size))
        elif isinstance(current_font_size, str):
            if current_font_size[-1:] == "x":
                stripped_current_font_size = current_font_size.strip("px")
                stripped_nested_font_size = nested_font_size.strip("%")
                calculated_font_size = float(stripped_nested_font_size) * (float(stripped_current_font_size)/100)

                return '{0:g}px'.format(calculated_font_size)
            else: #current_font_size[-1:] == "c":
                stripped_current_font_size = current_font_size.strip("c")
                stripped_nested_font_size = nested_font_size.strip("%")
                calculated_font_size = float(stripped_nested_font_size) * (float(stripped_current_font_size)/100)

                return '{0:g}c'.format(calculated_font_size)


    @staticmethod
    def get_value_from_style(styles, style_name):
        value = None
        for style in styles: # list in reverse-priority order, so last item (most important) values inherited
            if getattr(style, style_name) is not None:
                value = getattr(style, style_name)
        return value
