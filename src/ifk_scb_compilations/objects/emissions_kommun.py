"""Fetch emission data by kommun.

Observera att i tabellen över utsläpp från transporter ingår för närvarande endast vägtransporter.
Miljöräkenskapernas statistik om utsläpp till luft utgår från ett produktionsperspektiv och redovisar därför
direkta utsläpp från svenska ekonomiska aktörer. Produktionsperspektivet är annorlunda från det territoriella
perspektivet (som används för att rapportera Sveriges utsläpp till FN), vilket avgränsas till utsläpp som
sker inom Sveriges gränser. Samtidigt används ett territoriellt perspektiv i mycket av den underlagsdata
som används för att producera miljöräkenskapernas statistik om utsläpp till luft. För att justera för
skillnaden mellan miljöräkenskapernas produktionsperspektiv och det territoriella perspektivet används
en så kallad residensjustering. Residensjusteringen appliceras framförallt på transportrelaterade utsläpp.
Mer information om beräkningsmetodiken och underlagsdata som används för residensjusteringen redovisas i
statistikens Kvalitetsdeklarationen.
"""


import pandas as pd
from pyscbwrapper import SCB


class FetchData:
    """Class for emissions by kommun and year."""

    def __init__(
        self, emission_type: str = "växthusgaser, kiloton koldioxidekvivalenter"
    ):
        """Initialization.

        Args:
            emission_type: emission type to fetch
        """
        self.emission_type = emission_type
        self.query = ["MI", "MI1301", "MI1301B", "UtslappKommun"]
        self.scb = SCB("sv")
        self.scb.go_down(*self.query)
        self.region_id = self.scb.info()["variables"][0]["values"]
        self.regioner = self.scb.info()["variables"][0]["valueTexts"]
        self.years = self.scb.info()["variables"][3]["values"]

    def get_data(self) -> dict:
        """Get data from scb.

        Returns:
            dict: data from scb
        """
        self.scb.set_query(
            region=self.regioner, ämne=[self.emission_type], år=self.years
        )

        self.scb.get_query()
        return self.scb.get_data()

    def dict_to_dataframe(self, request_output: dict) -> pd.DataFrame:
        """Output dict to dataframe.

        Args:
            request_output: scb raw output data

        Returns:
            pd.DataFrame: scb data as DataFrame
        """
        n_data = len(request_output["data"])

        def map_id_to_name() -> list:
            """Map kommun id to kommun."""
            map_id_to_name_dict = dict(zip(self.region_id, self.regioner))
            reg_ids = [request_output["data"][i]["key"][0] for i in range(n_data)]
            region_names = [map_id_to_name_dict[id] for id in reg_ids]
            return region_names

        data_dict = {
            "region": map_id_to_name(),
            "year": [int(request_output["data"][i]["key"][2]) for i in range(n_data)],
            #'substance': [request_output['data'][i]['key'][1] for i in range(n_data)],
            "chg value": [
                float(request_output["data"][i]["values"][0]) for i in range(n_data)
            ],
        }

        return pd.DataFrame.from_dict(data_dict)

    def print_emission_labels(self) -> None:
        """Print all availible emissions."""
        availible_emissions = self.scb.get_variables()["ämne"]
        print("\n".join(availible_emissions))
        pass


def compare_years_and_sort_chg(
    data_df: pd.DataFrame, lower_year: int, upper_year: int
) -> pd.DataFrame:
    """Compare CHG between two years.

    Args:
        data_df: scb output data
        lower_year: lower year to comapare
        upper_year: upper year to compare

    Returns:
        pd.DataFrame: compiled data for lower and upper year
    """
    data_lower_reg = data_df[data_df["year"] == lower_year].sort_values(by=["region"])
    data_upper_reg = data_df[data_df["year"] == upper_year].sort_values(by=["region"])
    diff = (
        data_upper_reg["chg value"].to_numpy() / data_lower_reg["chg value"].to_numpy()
    )

    data_upper_reg["chg " + str(lower_year)] = data_lower_reg["chg value"].to_numpy()
    data_upper_reg["diff " + str(lower_year)] = diff
    data_upper_reg.rename(columns={"chg value": "chg 2021"}, inplace=True)

    data_compiled = data_upper_reg.sort_values(by=["chg 2021"], ascending=False)

    return data_compiled


if __name__ == "__main__":
    fData = FetchData()
    # fData.print_emission_labels()
    data_df = fData.dict_to_dataframe(fData.get_data())

    year0 = 2016
    year1 = 2021
    pd.set_option("display.max_rows", None)
    print(compare_years_and_sort_chg(data_df, year0, year1))
