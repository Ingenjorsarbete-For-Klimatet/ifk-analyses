"""Function to search in scb.

This function needs improval due to the fact that there is a limit on how many
request one can for a time period. Due to that a pause is added in the function,
hence the function is very slow. One can think about a solution where the
search tree is saved in a txt. If so, fast searches can be done in the txt.
However, this will be left as an issue for now.
"""
import copy
import time
import warnings

from pyscbwrapper import SCB


def search_substring(substring: str, entry_ids: list = None) -> list:
    """Search for substring in scb db.

    Args:
        substring: String to search for
        entry_ids: a list of list with entry ids

    Returns:
        list: elements are tuple with search path and title containing substring
    """
    scb = SCB("sv")
    results = []

    def recursive_search(nodes: list) -> None:
        """Recursively search for substring.

        Method is based on the assumption that the categorization structure is identified
        as list, while the objects are identified as dicts.

        Args:
            nodes: list of scb ids.
        """
        scb.ids = []
        scb.go_down(*nodes)
        info = scb.info()

        if isinstance(info, list):
            for child in info:
                # Too many request in too short time will give error...
                time.sleep(0.5)
                if "id" in child.keys():
                    new_nodes = copy.deepcopy(nodes)
                    new_nodes.append(child["id"])
                    recursive_search(new_nodes)
                else:
                    warnings.warn("Error. id not in keys.", stacklevel=2)
        elif isinstance(info, dict) and "title" in info.keys():
            title = info["title"]
            if substring in title:
                results.append((nodes, title))
        else:
            warnings.warn("Error: ", scb.info(), stacklevel=2)

    if not entry_ids:  # use all ids
        for entry in scb.info():
            recursive_search([entry["id"]])
    else:
        for entry in entry_ids:
            recursive_search(entry)

    return results


if __name__ == "__main__":
    a = search_substring("region", entry_ids=[["MI"]])
    for val in a:
        print(val)
