import json
import os
from typing import List

from rich import print
from thefuzz import fuzz

from .llm_backends.llmBackendBase import LLMBase


def filter_section_names(
    maybe_sections: List[str], backend: LLMBase, is_verbose: bool = False
):
    """
    This function takes a list of strings and returns a list of strings that are most likely to be section names.

    It utilizes the AI to filter out the strings that are most likely to be section names.
    Then in order to mitigate the Risk of the AI rewriting the section names, it uses fuzzy matching to match the AI generated text with the original text.

    Parameters
    ----------
    maybe_sections : List[str]
        A list of strings that are most likely to be section names.
    backend : LLMBase
        The backend to use for the AI operations.

    Returns
    -------
    List[str]
        A list of strings that are most likely to be section names.
    """

    # Get path for this file
    path = os.path.dirname(os.path.abspath(__file__))

    # join the path with the prompts file
    path = os.path.join(path, "prompts/clean_up_maybe_sections.txt")
    with open(path, "r") as f:
        prompt = f.read()

    prompt += "\n".join(maybe_sections)

    if is_verbose:
        print("Computed prompt " + prompt)

    # Ask to LLM backend to filter the section names
    res = backend.completion(
        prompt=prompt,
        max_tokens=512,
        temperature=0.8,
        override_system_message="You're a helpful AI, please help the user the best you can. Be as concise and short as possible.",
    )

    if is_verbose:
        print("AI response " + res)

    # Parse the response
    if type(res) == str:
        try:
            res = json.loads(res)
        except json.decoder.JSONDecodeError as e:
            print(e)
            print("Could not parse json")
            return

    # Fuzzy match sections with ai_service_response
    # Create each combination of sections and ai_text array elements
    combinations = []
    for section in maybe_sections:
        for ai_text_element in res:
            combinations.append((section, ai_text_element))

    # Calculate the fuzz ratio for each combination
    fuzz_ratios = []
    for combination in combinations:
        fuzz_ratios.append(fuzz.ratio(combination[0], combination[1]))

    # Order the combinations by fuzz ratio and create a new list wher each element is a tuple of (fuzz_ratio, section, ai_text_element)
    ordered_combinations = []
    for i in range(len(combinations)):
        ordered_combinations.append(
            (fuzz_ratios[i], combinations[i][0], combinations[i][1])
        )
    ordered_combinations.sort(key=lambda tup: tup[0], reverse=True)

    if is_verbose:
        print(ordered_combinations)

    N = next(
        (
            i
            for i, combination in enumerate(ordered_combinations)
            if combination[0] < 75
        ),
        len(maybe_sections),
    )

    # Print the first N elements of the ordered combinations where N is the number of elements in original sections array that have a fuzz ratio of greater than 75
    if is_verbose:
        print(ordered_combinations[:N])

    # Create a list of the sections that have a fuzz ratio of greater than 75
    return [ordered_combinations[i][1] for i in range(N)]


def summarize_section(section_text: str, backend: LLMBase, is_verbose: bool = False):
    """
    Summarizes a section using the AI.

    Parameters
    ----------
    section_text : str
        The text of the section to summarize.
    backend : LLMBase
        The backend to use for the AI operations.

    Returns
    -------
    str
        The summary of the section.
    """
    # Get path for this file
    path = os.path.dirname(os.path.abspath(__file__))

    # join the path with the prompts file
    path = os.path.join(path, "prompts/summarize_section_prompt.txt")
    with open(path, "r") as f:
        prompt = f.read()

    prompt += section_text

    if is_verbose:
        print("Computed prompt " + prompt)

    # Ask to LLM backend to summarize the section
    res = backend.completion(
        prompt=prompt,
        max_tokens=2048,
        temperature=0.8,
        override_system_message="You're a helpful AI, please help the user the best you can. Be as concise and short as possible.",
    )

    if is_verbose:
        print("AI response " + res)

    return res
