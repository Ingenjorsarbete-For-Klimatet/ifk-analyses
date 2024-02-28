"""Function to search in scb."""
import copy
import logging
import time
from datetime import datetime

from pyscbwrapper import SCB


class ScbSearch:
    """Class for efficient scb searches."""

    def __init__(self):
        """Initialization."""
        self.search_tree_file_path = "data/search_tree.txt"
        self.log_file_path = "log/update_search_tree.log"
        self.sleep_time = 0.7

    def update_search_tree(self) -> list:
        """Generate scb search tree.

        Args:
            entry_ids: a list of list with entry ids

        Returns:
            list: elements are tuple with search path and title containing substring
        """
        with open(self.search_tree_file_path, "w") as f:
            f.write(f"updated {datetime.today()}\n")
        scb = SCB("sv")
        results: list[tuple] = []

        def recursive_search(nodes: list) -> None:
            """Recursively dig in search tree.

            Method is based on the assumption that the categorization structure is identified
            as list, while the objects are identified as dicts.

            Args:
                nodes: list of scb ids.
            """
            scb.ids = []
            scb.go_down(*nodes)
            info = scb.info()
            logging.basicConfig(filename=self.log_file_path)

            if isinstance(info, list):
                for child in info:
                    time.sleep(self.sleep_time)
                    if "id" in child.keys():
                        new_nodes = copy.deepcopy(nodes)
                        new_nodes.append(child["id"])
                        recursive_search(new_nodes)
                    else:
                        logging.warning(f"Error. id not in keys for {nodes}")
            elif isinstance(info, dict) and "title" in info.keys():
                title = info["title"]
                with open(self.search_tree_file_path, "a") as file:
                    file.write(f"{nodes}; {title}\n")
            else:
                logging.warning(f"{nodes} not list or dict.")

        for entry in scb.info():
            recursive_search([entry["id"]])

        return results

    def search_substring(self, *arg: str):
        """Search for substring in scb db.

        Args:
            arg: Strings to search for

        Returns:
            list: elements are tuple with search path and title containing substring
        """
        with open(self.search_tree_file_path, "rt") as f:
            for line in f:
                if all(s.lower() in line.lower() for s in arg):
                    print(line)

        pass


if __name__ == "__main__":
    sSearch = ScbSearch()
    # sSearch.update_search_tree()
    sSearch.search_substring("darndidu")
