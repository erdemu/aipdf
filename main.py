import argparse
import time

import rich
import tqdm

from aipdf.pdf_tools.fontmap import extract_fontmap_from_pdf
from aipdf.pdf_tools.heuristics import try_to_find_known_text_that_can_be_a_subtitle
from aipdf.pdf_tools.pdfutils import read_whole_text, split_text_into_sections

from aipdf.ai_helpers import filter_section_names, summarize_section
from aipdf.llm_backends.openrouter_models import (
    Mixtral8x7bInstructBeta,
    Zephyr7b,
    GPT4_Turbo,
    Capybara7b,
)
from aipdf.llm_backends.openRouter import OpenRouter


def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf_file", help="The PDF file to extract text from.")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose mode.", default=False
    )
    parser.add_argument(
        "--dry_run", "-d", action="store_true", help="Dry run mode.", default=False
    )

    args = parser.parse_args()

    with open(args.pdf_file, "rb") as f:
        fonts = extract_fontmap_from_pdf(f)
        family, size = try_to_find_known_text_that_can_be_a_subtitle(fonts)
        # Print the text from max_hit_count
        sections = []
        for text in fonts[family]["texts"][size]:
            sections.append(text)

        # Filter the sections
        backend = OpenRouter(Mixtral8x7bInstructBeta())
        sections_to_process = filter_section_names(sections, backend, args.verbose)

        whole_text = read_whole_text(f)
        sections_text = split_text_into_sections(whole_text, sections)

        # Create a dictionary of the sections and their corresponding text
        sections_dict = dict()

        for section in sections_to_process:
            sections_dict[section] = sections_text[section]

        if not args.dry_run:
            # For each section that is not a reference section, create a prompt and get the AI to generate summary text for that section using minimum tokens.
            chapter_summaries = dict()

            # copy keys from sections_dict to chapter_summaries
            for key in sections_dict.keys():
                chapter_summaries[key] = ""

            for section in tqdm.tqdm(sections_to_process, desc="Generating summaries"):
                # delay for 5 seconds due to api limits
                time.sleep(5)
                # if section is not references or appendix
                if (
                    "references" not in section.lower()
                    and "appendix" not in section.lower()
                ):
                    chapter_summaries[section] = summarize_section(
                        sections_dict[section], backend, args.verbose
                    )

            rich.print(chapter_summaries)


if __name__ == "__main__":
    main()
