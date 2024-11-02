"""Passenger Vehicle CO2 LCA."""

# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # $CO_2$-LCA för olika bilalternativ
#
# **Human activities, principally through emissions of greenhouse gases, have unequivocally
# caused global warming, with global surface temperature reaching 1.1°C above 1850-1900
# in 2011-2020. Global greenhouse gas emissions have continued to increase, with unequal
# historical and ongoing contributions arising from unsustainable energy use, land use and
# land-use change, lifestyles and patterns of consumption and production across regions,
# between and within countries, and among individuals (high confidence)**
# https://www.ipcc.ch/report/ar6/syr/downloads/report/IPCC_AR6_SYR_SPM.pdf
#
# Ett steg mot konkreta och effektiva åtgärder är att göra en livscykelanalys för fordon. Nedan en enkel
# jämförelsemodell för att kunna utvärdera utsläpp ifrån nyproduktion i förhållande till utsläpp från
# körning. De exempel på siffror som tagits fram kommer från öppna källor på nätet, t ex Volvo Cars
# LCA-rapporter, men lämnas för användaren att ändra för att kunna göra egna parameterstudier.

import matplotlib.pyplot as plt
import numpy as np

import ifk_analyses.objects.personal_vehicle_lca as pvl

# ## Grundläggande antaganden
# Grundläggande antaganden kommer från Volvo Cars LCA-rapporter, som återfinns här:
#
# https://www.volvocars.com/mt/news/sustainability/transparency-in-action-heres-our-ex90-carbon-footprint-report/
#
# Siffrorna för CO2 per liter bensin kan justeras uppåt något ytterligare enligt denna källa:
#
# https://innovationorigins.com/en/producing-gasoline-and-diesel-emits-more-co2-than-we-thought/
#
# I denna analys har dock datan från Volvos officiella analyser hänvisade till ovan använts.

# Grundläggande antaganden
vehicle_manufacturing_cost = 8  # 8 kg CO2/kg vehicle
battery_manufacturing_cost = 77  # 77 kg CO2/kWh battery (average between 56 & 98, from EX90 and EX30, respectively.)
kgCO2_per_kWh = 0.45  # 0.45 kg CO2/kWh electricity (World mix)
kgCO2_per_litre = 3  # 3kg C02/litre petrol (extraction, production & combustion)
vehicle_life = 300000  # 300 000 km defined as the average life of a vehicle (from googling Swedish sources)

# ## Definiera bilar
# För att kunna göra jämförelsen behöver vi välja vilka biltyper vi vill titta på. Följande typexempel har tagits fram:
#
# |Bil | Vikt exkl batteri (kg) | Batteri (kWh) | Räckvidd el (km) | Energiförbrukning| Användande|
# |---|---|---|---|---|---|
# |Liten bensinbil | 1500 | - | - | 0.5 liter bensin/mil |100%|
# |Stor elbil | 2200 | 125 | 500 | 0.25 kWh/km |100%|
# |Liten elbil | 1500 | 50 | 330 | 0.15 kWh/km |100%|
# |Cykel | 10 | 0 | 0 | 0kWh/km |100%|
# |Elcykel | 15 |0.5 | 20 | 0.005 kWh/km |100%|
#

vehicles = {
    pvl.Vehicle(
        name="Liten bensinbil",
        weight=1500,
        battery_capacity=0,
        consumption_per_km=0.05,
        co2_build_cost_per_kg=vehicle_manufacturing_cost,
        co2_battery_build_cost_per_kWh=battery_manufacturing_cost,
        co2_cost_per_consumption=kgCO2_per_litre,
        vehicle_life_km=vehicle_life,
    ),
    pvl.Vehicle(
        name="Stor elbil",
        weight=2200,
        battery_capacity=125,
        consumption_per_km=0.25,
        co2_build_cost_per_kg=vehicle_manufacturing_cost,
        co2_battery_build_cost_per_kWh=battery_manufacturing_cost,
        co2_cost_per_consumption=kgCO2_per_kWh,
        vehicle_life_km=vehicle_life,
    ),
    pvl.Vehicle(
        name="Liten elbil",
        weight=1500,
        battery_capacity=50,
        consumption_per_km=0.15,
        co2_build_cost_per_kg=vehicle_manufacturing_cost,
        co2_battery_build_cost_per_kWh=battery_manufacturing_cost,
        co2_cost_per_consumption=kgCO2_per_kWh,
        vehicle_life_km=vehicle_life,
    ),
    pvl.Vehicle(
        name="Cykel",
        weight=10,
        battery_capacity=0,
        consumption_per_km=0,
        co2_build_cost_per_kg=vehicle_manufacturing_cost,
        co2_battery_build_cost_per_kWh=battery_manufacturing_cost,
        co2_cost_per_consumption=kgCO2_per_kWh,
        vehicle_life_km=vehicle_life,
    ),
    pvl.Vehicle(
        name="Elcykel",
        weight=15,
        battery_capacity=0.5,
        consumption_per_km=0.005,
        co2_build_cost_per_kg=vehicle_manufacturing_cost,
        co2_battery_build_cost_per_kWh=battery_manufacturing_cost,
        co2_cost_per_consumption=kgCO2_per_kWh,
        vehicle_life_km=vehicle_life,
    ),
}

driven_distance = np.linspace(0, vehicle_life, 200)
legend = []
for vehicle in vehicles:
    vehicle_data = pvl.co2analysis(vehicle, driven_distance, 1)
    plt.plot(vehicle_data[0], vehicle_data[1])
    legend.append(vehicle.name)
plt.legend(legend)
plt.xlabel("kördistans [km]")
plt.ylabel("CO2 [metric tonnes]")
plt.show()

# ## Fordonspark
# Många av oss äger ju flera fordon. Hur mycket förbättrar vi situationen om
# vi cyklar 10km för varje 100km vi kör i vår stora bil? Här jämför vi
# alternativ för omläggning av persontransporterna för någon som tidigare kört
# en liten bensinbil men som nu vill lägga om sitt liv för att minska klimatpåverkan.
# Efter ett antal mil med bilpendling bestämmer sig vår protagonist för att lägga om
# sitt liv för att minska sitt klimatavtryck, genom att:
#
# 1. Fortsätta köra samma bensinbil
# 2. Köpa en stor elbil
# 3. Köpa en liten elbil
# 4. Köpa en stor elbil och en cykel
# 5. Köpa en stor elbil och en elcykel
# 6. Köpa en elcykel
#
# Låt oss definiera en brytpunkt till att börja med:

kilometers_at_change = (
    166667  # Average current driven distance according to analysis below
)
fraction_bike_rides = 0.1  # 10% biking

# Define support variables for readability
driven_to_split = np.linspace(0, kilometers_at_change, 100)
driven_from_split = np.linspace(kilometers_at_change, vehicle_life, 100)
small_gas_car = next(
    (vehicle for vehicle in vehicles if vehicle.name == "Liten bensinbil"), "None"
)
small_electric_car = next(
    (vehicle for vehicle in vehicles if vehicle.name == "Liten elbil"), "None"
)
large_electric_car = next(
    (vehicle for vehicle in vehicles if vehicle.name == "Stor elbil"), "None"
)
bike = next((vehicle for vehicle in vehicles if vehicle.name == "Cykel"), "None")
electric_bike = next(
    (vehicle for vehicle in vehicles if vehicle.name == "Cykel"), "None"
)


# And define additional vehicle combinations
large_electric_and_bike = pvl.Vehicle(
    name="Stor elbil och cykel",
    weight=large_electric_car.weight + bike.weight,
    battery_capacity=large_electric_car.battery_capacity + bike.battery_capacity,
    consumption_per_km=large_electric_car.consumption_per_km * (1 - fraction_bike_rides)
    + bike.consumption_per_km * fraction_bike_rides,
    co2_build_cost_per_kg=vehicle_manufacturing_cost,
    co2_battery_build_cost_per_kWh=battery_manufacturing_cost,
    co2_cost_per_consumption=kgCO2_per_kWh,
    vehicle_life_km=vehicle_life,
)
small_electric_and_bike = pvl.Vehicle(
    name="Liten elbil och cykel",
    weight=small_electric_car.weight + bike.weight,
    battery_capacity=small_electric_car.battery_capacity + bike.battery_capacity,
    consumption_per_km=small_electric_car.consumption_per_km * (1 - fraction_bike_rides)
    + bike.consumption_per_km * fraction_bike_rides,
    co2_build_cost_per_kg=vehicle_manufacturing_cost,
    co2_battery_build_cost_per_kWh=battery_manufacturing_cost,
    co2_cost_per_consumption=kgCO2_per_kWh,
    vehicle_life_km=vehicle_life,
)

# Define the scenarios as described above
scenarios = {
    "Kör vidare liten bensinbil": {0: [small_gas_car, driven_distance]},
    "Köpa stor elbil": {
        0: [small_gas_car, driven_to_split],
        1: [large_electric_car, driven_from_split],
    },
    "Köpa liten elbil": {
        0: [small_gas_car, driven_to_split],
        1: [small_electric_car, driven_from_split],
    },
    "Köpa stor elbil och cykel": {
        0: [small_gas_car, driven_to_split],
        1: [large_electric_and_bike, driven_from_split],
    },
    "Köpa liten elbil och cykel": {
        0: [small_gas_car, driven_to_split],
        1: [small_electric_and_bike, driven_from_split],
    },
    "Köpa elcykel": {
        0: [small_gas_car, driven_to_split],
        1: [electric_bike, driven_from_split],
    },
    "Aldrig skaffa bil": {0: [bike, driven_distance]},
}


vehicle_data = []
for scenario, data in scenarios.items():
    co2debt = 0
    scenario_driven_distance = []
    scenario_CO2data = []
    for _, vehicleanddistance in data.items():
        a, b = pvl.co2analysis(vehicleanddistance[0], vehicleanddistance[1], co2debt)
        scenario_driven_distance = np.append(scenario_driven_distance, a)
        scenario_CO2data = np.append(scenario_CO2data, b)
        co2debt = scenario_CO2data[-1]
    vehicle_data.append([scenario, scenario_driven_distance, scenario_CO2data])

plt.figure(figsize=(10, 6), dpi=100)
leg = []
for value in vehicle_data:
    plt.plot(value[1], value[2])
    leg.append(value[0])
plt.legend(leg)
plt.xlabel("kördistans [km]")
plt.ylabel("CO2 [metric tonnes]")
plt.show()

# ## Från det personliga planet till världens fordonsflotta
# Genom att tillgripa en naivistisk analys (vi ger inte någon rabatt då en bil
# säljs, vilket innebär att inköp av begagnad bil skulle ge en initial-CO2-kostnad
# av 0 ton och därmed räknar vi inte med avskrivning. Eftersom koldioxid ackumuleras
# i atmosfären är det dock i vår mening det rimligaste sättet att förhålla sig till
# problemet) har vi visat hur elektrifiering, i dagens SUV-tider, sällan innebär
# sänkta koldioxidutsläpp, och en övergång till 10% cykel *i kombination med inköp
# av elbil* endast är marginellt bättre.
#
# Vad har vi för siffror att förhålla oss till på samhällsnivå? I världen
# finns det grovt räknat 1,475 miljarder bilar.
# https://hedgescompany.com/blog/2021/06/how-many-cars-are-there-in-the-world/
# Hur gamla dessa är har jag svårt att hitta siffror för, men den omfattande
# svenska statistiken har siffror som vi kan tillgripa: I Sverige är en bil i
# genomsnitt 10år gammal, och skrotas i genomsnitt efter 18år.
#
# Låt oss vidare anta att de svenska förhållandena är representativa för
# världen i stort och att en bil körs 300000km i genomsnitt innan den skrotas
# (vilket är siffror som dyker upp vid googling - jag hittar inte någon siffra
# från scb eller trafa för att bekräfta detta för tillfället).
#
# Slutligen antar vi att bilarna rullar med konstant körsträcka varje år. Det
# innebär alltså att en tio år gammal genomsnittsbil har:
#
# $$
# \frac{(18-10)}{18}*300000=133333\text{km}
# $$
#
# kvar att köra innan den skrotas. Anta nu att de allra flesta bilar i
# världsflottan fortfarande är bensinbilar, och att de i genomsnitt har en
# förbrukning om 0,7l/mil. Vi kan då räkna ut hur många miljarder ton CO2
# den befintliga fordonsflottan förväntas släppa ut innan den är förbrukad:

# +
average_remaining_distance = 133333  # km
average_fuel_consumption = 0.07  # l / km
total_number_of_cars = 1.475e9  # cars world wide

remaining_CO2_output_from_current_fleet = (
    average_remaining_distance
    * average_fuel_consumption
    * kgCO2_per_litre
    * total_number_of_cars
    / 1e9
    / 1e3
)
print("The expected CO2-output from the current world car fleet is approximately")
print("{:3.0f} Gton CO2".format(remaining_CO2_output_from_current_fleet))

# -

# ### Hur mycket är det?
# För att sätta denna siffra i kontext är det lämpligt att gå till IPCC-referensen
# ovan. När det kommer till kvarvarande budget för koldioxidekvivalentutsläpp säger
# rapporten detta:
#
# > *For every 1000 GtCO2 emitted by human activity, global surface temperature
# rises by 0.45°C (best estimate, with a likely range from 0.27°C to 0.63°C).
# The best estimates of the remaining carbon budgets from the beginning of 2020
# are 500 GtCO2 for a 50% likelihood of limiting global warming to 1.5°C and 1150
# GtCO2 for a 67% likelihood of limiting warming to 2°C. The stronger the reductions
# in non-CO2 emissions, the lower the resulting temperatures are for a given
# remaining carbon budget or the larger remaining carbon budget for the same
# level of temperature change.*
#
# Av de 500 GtCO2 som fanns att tillgå 2020 har omkring 4/5 redan förbrukats.
# Av den kvarvarande budgeten äter alltså redan den befintliga fordonsflottan
# upp omkring hälften.
#
# Om vi väljer att växla till en större elbil för alla bilar så kommer den att
# öka mängden C02-utsläpp till totalt resta 3000000km med:

increase_from_current_fleet_if_electrified = (
    vehicle_data[1][2][-1] / vehicle_data[0][2][-1]
)
print("{:3.0f} percent".format((increase_from_current_fleet_if_electrified - 1) * 100))


# Vilket ger de totala utsläppen från fordonsflottan istället till:

remaining_CO2_output_from_current_fleet_if_electrified = (
    vehicle_data[1][2][-1]
    / vehicle_data[0][2][-1]
    * remaining_CO2_output_from_current_fleet
)
print("The expected CO2-output from the lifetime of the current world car fleet,")
print("when everyone changes to an electric car now, would be approximately")
print("{:3.0f} Gton CO2".format(remaining_CO2_output_from_current_fleet_if_electrified))


# De nya elbilarna, i egenskap av nya, skulle därtill fortsätta släppa ut CO2
# så länge inte all elektricitet kommer från fossilfria alternativ i ytterligare
# nästan 170000km.

# Denna analys har inte tagit hänsyn till CO2-kostnaden för att skapa och
# upprätthålla väginfrastruktur för dessa miljardvis med vägbundna fordon.
