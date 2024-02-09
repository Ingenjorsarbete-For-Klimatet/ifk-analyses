"""Inputs for request, and analysis."""

import json
from dataclasses import dataclass

import matplotlib.pyplot as plt
import pandas as pd
import requests


@dataclass
class RequestInput:
    """Dataclass for passenger transport query.

    Query info can be found at url.
    """

    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/MI/MI0107/TotaltUtslappN"
    query = {
        "query": [
            {
                "code": "Vaxthusgaser",
                "selection": {"filter": "item", "values": ["CO2-ekv."]},
            },
            {
                "code": "Sektor",
                "selection": {"filter": "item", "values": ["0.2", "0.4", "8.0", "5.0"]},
            },
        ],
        "response": {"format": "json"},
    }


class FetchScbData:
    """Fetch data class from scb."""

    def __init__(self) -> None:
        """Initialization."""
        self.session = requests.Session()
        self.response = self.session.post(RequestInput.url, json=RequestInput.query)
        request_output = json.loads(self.response.content.decode("utf-8-sig"))
        self.data = self.transform_json_to_df(request_output)

    def transform_json_to_df(self, request_output: dict) -> pd.DataFrame:
        """Transform json format to dataframe.

        Args:
            request_output: The first parameter.

        Returns:
            pd.Dataframe: request output as dataframe
        """
        n_vals = len(request_output["data"])

        data_dict = {
            "emission measure": list(
                request_output["data"][i]["key"][0] for i in range(n_vals)
            ),
            "emission type": list(
                request_output["data"][i]["key"][1] for i in range(n_vals)
            ),
            "year": list(
                float(request_output["data"][i]["key"][2]) for i in range(n_vals)
            ),
            "value": list(
                float(request_output["data"][i]["values"][0]) for i in range(n_vals)
            ),
        }

        return pd.DataFrame.from_dict(data_dict)


class Analysis:
    """Container for plotting data corresponding to fetch spec by Request_input."""

    def __init__(self, request_output: pd.DataFrame) -> None:
        """Initialization.

        Args:
            request_output: Output from scb api response.
        """
        self.data = request_output

    def plot_co2_transports(self) -> None:
        """Plot CO2 for transports."""
        labels = {
            "0.2": "NATIONELL TOTAL (exklusive LULUCF, inklusive internationella transporter)",
            "0.4": "NATIONELL TOTAL (inklusive LULUCF, inklusive internationella transporter)",
            "8.0": "INRIKES TRANSPORTER, TOTALT",
            "5.0": "UTRIKES TRANSPORTER, TOTALT",
        }

        def _plot_individual(emission_type: str) -> None:
            """Plot based on emission type.

            Args:
                emission_type (str): emission type code
            """
            ax.plot(
                self.data[self.data["emission type"] == emission_type]["year"],
                self.data[self.data["emission type"] == emission_type]["value"],
                label=labels[emission_type],
            )

        ax = plt.subplot(111)
        _plot_individual("0.2")
        _plot_individual("0.4")
        _plot_individual("8.0")
        _plot_individual("5.0")

        ax.set_title("Utsläpp av växthusgaser i CO2-ekvivalent. Källa:SCB")
        ax.set_xlabel("År")
        ax.set_ylabel("kiloTon CO2-ekvivalent")
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05))
        box = ax.get_position()
        ax.set_position(
            [box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9]
        )
        plt.show()
        pass

    def plot_co2_national_international(self) -> None:
        """Plot CO2 National vs international."""
        years = self.data[self.data["emission type"] == "0.2"]["year"]
        amount_domestic = (
            self.data[self.data["emission type"] == "8.0"]["value"].to_numpy()
            / self.data[self.data["emission type"] == "0.2"]["value"].to_numpy()
        )
        amount_international = (
            self.data[self.data["emission type"] == "5.0"]["value"]
            / self.data[self.data["emission type"] == "0.2"]["value"].to_numpy()
        )
        plt.plot(years, 100 * amount_domestic)
        plt.plot(years, 100 * amount_international)
        plt.xlabel("År")
        plt.ylabel("%")
        plt.title("Andel totalutsläpp av CO2-ekvivalenter")
        plt.legend(["Nationella transporter", "Internationella transporter"])
        plt.show()
        pass
