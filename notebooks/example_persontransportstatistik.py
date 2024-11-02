"""Example."""

# %% [markdown]
# ## Example on how to run

# %% [markdown]
# Import packages.

# %%
# %matplotlib inline
import ifk_analyses.objects.passenger_transport as passenger_transport

# %% [markdown]
# Start a request session and fetch data from scb, based on the query defined in ifk_scb_compilations.queries.passenger_transport.Request_input.query.

# %%
scb_data = passenger_transport.FetchScbData()

# %% [markdown]
# Create an instance of passenger_transport.Analysis and execute the analysis, compiliation or whatever you want to do with the data.

# %%
passenger_analysis = passenger_transport.Analysis(scb_data.data)
passenger_analysis.plot_co2_transports()
passenger_analysis.plot_co2_national_international()
