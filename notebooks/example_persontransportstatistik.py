"""Example."""

# %% [markdown]
# ## Example on how to run

# %% [markdown]
# Import packages.

# %%
import json

#%matplotlib inline
import ifk_scb_compilations.objects.passenger_transport as passenger_transport
import requests

# %% [markdown]
# Start a request session and fetch data from scb, based on the query defined in ifk_scb_compilations.queries.passenger_transport.Request_input.query.

# %%
session = requests.Session()
response = session.post(passenger_transport.Request_input.url,
                        json=passenger_transport.Request_input.query)
response_json = json.loads(response.content.decode('utf-8-sig'))

# %% [markdown]
# Create an instance of passenger_transport.Analysis and execute the analysis, compiliation or whatever you want to do with the data.

# %%
passenger_analysis = passenger_transport.Analysis(response_json)
passenger_analysis.plot_co2_transports()
passenger_analysis.plot_co2_national_international()


