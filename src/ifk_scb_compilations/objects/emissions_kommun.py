"""
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

from dataclasses import dataclass

from pyscbwrapper import SCB
import pandas as pd

class FetchData:
    """Dataclass for emissions by kommun and year.
    """
    def __init__(self, emissionType = 'växthusgaser, kiloton koldioxidekvivalenter'):
        self.emissionType = emissionType
        self.query = ['MI','MI1301','MI1301B','UtslappKommun']
        self.scb = SCB('sv')
        self.scb.go_down(*self.query)
        self.region_id  = self.scb.info()['variables'][0]['values']
        self.regioner  = self.scb.info()['variables'][0]['valueTexts']
        self.years  = self.scb.info()['variables'][3]['values']

    def fetchData(self) -> dict:
        """Fetch data from scb."""
        self.scb.set_query(
            region=self.regioner,
            ämne=[self.emissionType], 
            år=self.years)
            
        self.scb.get_query()
        return self.scb.get_data()
    
    def dict_to_dataframe(self, request_output)-> pd.DataFrame:
        """Output dict to dataframe."""
        n_data = len(request_output['data'])

        def map_id_to_name() -> list:
            """Map kommun id to kommun."""
            map_id_to_name_dict = dict(zip(self.region_id, self.regioner))
            reg_ids = [request_output['data'][i]['key'][0] for i in range(n_data)]
            region_names = [map_id_to_name_dict[id] for id in reg_ids]
            return region_names 

        data_dict = {'region': map_id_to_name(),
                    'year': [int(request_output['data'][i]['key'][2]) for i in range(n_data)],
                    #'substance': [request_output['data'][i]['key'][1] for i in range(n_data)],
                    'chg value': [float(request_output['data'][i]['values'][0]) for i in range(n_data)],
                    }

        return pd.DataFrame.from_dict(data_dict)

    def temp(self, data_df):

        #data_2021 = data_df[data_df['year'] == 2021].sort_values(by=['chg value'], ascending=False)
        #data_2011 = data_df[data_df['year'] == 2011].sort_values(by=['chg value'], ascending=False)

        data_2021_reg = data_df[data_df['year'] == 2021].sort_values(by=['region'])
        data_2011_reg = data_df[data_df['year'] == 2011].sort_values(by=['region'])

        diff_2021_2011 = data_2021_reg['chg value'].to_numpy() / data_2011_reg['chg value'].to_numpy()

        data_2021_reg['chg 2011'] = data_2011_reg['chg value'].to_numpy()
        data_2021_reg['diff 2011'] = diff_2021_2011
        data_2021_reg.rename(columns={"chg value": "chg 2021"}, inplace=True)

        data_compiled = data_2021_reg.sort_values(by=['chg 2021'], ascending=False)

        
        return data_compiled

if __name__ == "__main__":
    fData = FetchData()
    data_df = fData.dict_to_dataframe(fData.fetchData())

    pd.set_option('display.max_rows', None)
    print(fData.temp(data_df))