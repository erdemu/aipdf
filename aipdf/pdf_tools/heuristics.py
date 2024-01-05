from typing import Dict, List, Set, Tuple, Union


def try_to_find_known_text_that_can_be_a_subtitle(
    fontmap: Dict[str, Dict[str, Union[List[float], Set[float], Dict[float, List[str]]]]]
) -> Tuple[str, float]:
    """
    Tries to find known text that can be a subtitle.

    Parameters:
    ----------

    fontmap: Dict[str, Dict[str, Union[List[float], Set[float], Dict[float, List[str]]]]]
        The fontmap that is extracted from the PDF file.

    Returns:
    ----------
    Tuple[str, float]
        The font family and font size that is most likely to be a subtitle.
    """
    known_texts = [
        "abstract",
        "introduction",
        "approach",
        "methodology",
        "conclusion",
        "references",
        "future work",
        "acknowledgements",
    ]

    top_hit_font_size = 0
    top_hit_font_family = ""

    max_hit_count = -1

    for font_family in fontmap.keys():
        for fontsize in fontmap[font_family]["fontsizes"]:
            hit_count = 0

            for text in fontmap[font_family]["texts"][fontsize]:
                if len(text) > 50 or len(text) < 5:
                    # Skip the text if it's too long or too short to be a subtitle
                    continue

                for known_text in known_texts:
                    if known_text in text.lower():
                        hit_count += 1

            if hit_count > max_hit_count:
                max_hit_count = hit_count
                top_hit_font_size = fontsize
                top_hit_font_family = font_family
    return top_hit_font_family, top_hit_font_size
