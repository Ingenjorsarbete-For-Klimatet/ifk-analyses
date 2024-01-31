from dataclasses import dataclass

@dataclass
class passenger_transport:
    """data class for passenger transport query

    query går att få färdigformulerat direkt på den önskade SCB-sidan i statistikdatabasen
    """
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/MI/MI0107/TotaltUtslappN"
    query = {
    "query": [
        {
        "code": "Vaxthusgaser",
        "selection": {
            "filter": "item",
            "values": [
            "CO2-ekv."
            ]
        }
        },
        {
        "code": "Sektor",
        "selection": {
            "filter": "item",
            "values": [
            "0.2",
            "0.4",
            "8.0",
            "5.0"
            ]
        }
        }
    ],
    "response": {
        "format": "json"
    }
    }
