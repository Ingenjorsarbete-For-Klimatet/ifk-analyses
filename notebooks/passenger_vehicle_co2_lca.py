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
# Ett steg mot konkreta och effektiva åtgärder är att göra en livscykelanalys för fordon. Nedan en enkel jämförelsemodell för att kunna utvärdera utsläpp ifrån nyproduktion i förhållande till utsläpp från körning. De exempel på siffror som tagits fram kommer från öppna källor på nätet, t ex Volvo Cars LCA-rapporter, men lämnas för användaren att ändra för att kunna göra egna parameterstudier.

import matplotlib.pyplot as plt
import numpy as np

# ## Grundläggande antaganden
# Grundläggande antaganden kommer från Volvo Cars LCA-rapporter, som återfinns här:
#
# https://www.volvocars.com/mt/news/sustainability/transparency-in-action-heres-our-ex90-carbon-footprint-report/
#
# Siffrorna för CO2 per liter bensin kan justeras uppåt något ytterligare enligt denna källa:
#
# https://innovationorigins.com/en/producing-gasoline-and-diesel-emits-more-co2-than-we-thought/
#
# I denna analys har dock datan från Volvo använts.

# Grundläggande antaganden
car_manufacturing_cost = 8  # 8 kg CO2/kg car
battery_manufacturing_cost = 77  # 77 kg CO2/kWh battery (average between 56 & 98, from EX90 and EX30, respectively.)
kgC02_per_kWh_europe = 0.45  # 0.45 kg CO2/kWh electricity (World mix)
kgC02_per_litre = 3  # 3kg C02/litre petrol (extraction, production & combustion)

# ## Definiera bilar
# För att kunna göra jämförelsen behöver vi välja vilka biltyper vi vill titta på. Följande tre typexempel har tagits fram:
#
# ##### Version 1
# |Bil | Vikt exkl batteri (kg) | Batteri (kWh) | Räckvidd el (km) | Energiförbrukning| Användande|
# |---|---|---|---|---|---|
# |A: Liten bensinbil | 1500 | - | - | 0.5 liter bensin/mil |100%|
# |B: Stor elbil | 2200 | 125 | 500 | 0.25 kWh/km |100%|
# |C: Liten elbil | 1500 | 50 | 330 | 0.15 kWh/km |100%|
# |D: Cykel | 10 | 0 | 0 | 0kWh/km |100%|
# |E: Elcykel | 15 |0.5 | 20 | 0.005 kWh/km |100%|
#

cars = {
    "A: Liten bensinbil": [1500, 0, 0, 0.05, 1],
    "B: Stor elbil": [2200, 125, 500, 0.25, 1],
    "C: Liten elbil": [1500, 50, 330, 0.15, 1],
    "D: Cykel": [10, 0, 0, 0, 1],
    "E: Elcykel": [15, 0.5, 20, 0.005, 1],
}
print(cars)


# Definiera funktion som ger CO2 över tid
def co2analysis(cars, driven_distance, co2debt):
    """CO2 accumulator function."""
    car_data = []
    for key, value in cars.items():
        C02_data_constant = (
            co2debt
            + car_manufacturing_cost * value[0]
            + battery_manufacturing_cost * value[1]
        )
        if value[1] == 0:
            C02_data = (
                C02_data_constant
                + kgC02_per_litre
                * value[3]
                * (driven_distance - driven_distance[0])
                * value[4]
            )
        else:
            C02_data = (
                C02_data_constant
                + kgC02_per_kWh_europe
                * value[3]
                * (driven_distance - driven_distance[0])
                * value[4]
            )
        car_data.append([key, driven_distance, C02_data / 1000])

    return car_data


driven_distance = np.linspace(0, 300000, 200)
leg = []
car_data = co2analysis(cars, driven_distance, 0)
for value in car_data:
    plt.plot(value[1], value[2])
    leg.append(value[0])
plt.legend(leg)
plt.xlabel("kördistans [km]")
plt.ylabel("CO2 [metric tonnes]")
plt.show()

# ## Fordonspark
# Många av oss äger ju flera fordon. Hur mycket förbättrar vi situationen om vi cyklar 10km för varje 100km vi kör i vår stora bil? Här jämför vi tre alternativ för omläggning av persontransporterna för någon som tidigare kört en liten bensinbil men som nu vill lägga om sitt liv för att minska klimatpåverkan. Efter 16667mil bilpendling bestämmer sig vår protagonist för att lägga om sitt liv för att minska sitt klimatavtryck, genom att:
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

# +
# Scenario 1: Fortsätta köra samma bensinbil
scenarios = {"1. Fortsätta köra bensinbil": cars["A: Liten bensinbil"]}
driven_distance = np.linspace(0, 300000, 200)
car_data = co2analysis(scenarios, driven_distance, 0)


# Scenario 2: Köpa stor elbil
scenarios = {"2. Köpa stor elbil": [1500, 0, 0, 0.05, 1]}
driven_distance = np.linspace(0, kilometers_at_change, 100)
car_data_1 = co2analysis(scenarios, driven_distance, 0)

scenarios = {
    "tmp1": cars[
        "B: Stor elbil"
    ],  # add percentage of driving with current mode of transport
}
driven_distance = np.linspace(kilometers_at_change, 300000, 100)
car_data_2 = co2analysis(scenarios, driven_distance, car_data_1[0][2][-1] * 1000)
# ([key,driven_distance,C02_data/1000])
car_data_1[0][1] = np.append(car_data_1[0][1], car_data_2[0][1])
car_data_1[0][2] = np.append(car_data_1[0][2], car_data_2[0][2])
car_data.append(car_data_1[0])


# Scenario 3: Köpa liten elbil
scenarios = {"3. Köpa liten elbil": cars["A: Liten bensinbil"]}
driven_distance = np.linspace(0, kilometers_at_change, 100)
car_data_1 = co2analysis(scenarios, driven_distance, 0)

scenarios = {
    "tmp1": cars["C: Liten elbil"],
}
driven_distance = np.linspace(kilometers_at_change, 300000, 100)
car_data_2 = co2analysis(scenarios, driven_distance, car_data_1[0][2][-1] * 1000)

car_data_1[0][1] = np.append(car_data_1[0][1], car_data_2[0][1])
car_data_1[0][2] = np.append(car_data_1[0][2], car_data_2[0][2])
car_data.append(car_data_1[0])


# Scenario 4: Köpa stor elbil och cykel
scenarios = {"4. Köpa stor elbil och cykel": cars["A: Liten bensinbil"]}
driven_distance = np.linspace(0, kilometers_at_change, 100)
car_data_1 = co2analysis(scenarios, driven_distance, 0)

scenarios = {
    "tmp1": cars["B: Stor elbil"],
}
scenarios["tmp1"][4] = 0.9  # percentage with current mode of transport
driven_distance = np.linspace(kilometers_at_change, 300000, 100)
car_data_2 = co2analysis(scenarios, driven_distance, car_data_1[0][2][-1] * 1000)
# ([key,driven_distance,C02_data/1000])
scenarios = {
    "tmp2": cars[
        "D: Cykel"
    ],  # add percentage of driving with current mode of transport
}
scenarios["tmp2"][4] = 0.1
driven_distance = np.linspace(kilometers_at_change, 300000, 100)
car_data_2_2 = co2analysis(scenarios, driven_distance, 0)
car_data_2[0][2] = car_data_2[0][2] + car_data_2_2[0][2]

car_data_1[0][1] = np.append(car_data_1[0][1], car_data_2[0][1])
car_data_1[0][2] = np.append(car_data_1[0][2], car_data_2[0][2])
car_data.append(car_data_1[0])


# Scenario 5: Köpa liten elbil och cykel
scenarios = {"5. Köpa liten elbil och cykel": cars["A: Liten bensinbil"]}
driven_distance = np.linspace(0, kilometers_at_change, 100)
car_data_1 = co2analysis(scenarios, driven_distance, 0)

scenarios = {
    "tmp1": cars["C: Liten elbil"],
}
scenarios["tmp1"][4] = 0.9  # percentage with current mode of transport
driven_distance = np.linspace(kilometers_at_change, 300000, 100)
car_data_2 = co2analysis(scenarios, driven_distance, car_data_1[0][2][-1] * 1000)
# ([key,driven_distance,C02_data/1000])

scenarios = {
    "tmp2": cars[
        "D: Cykel"
    ],  # add percentage of driving with current mode of transport
}
scenarios["tmp2"][4] = 0.1
driven_distance = np.linspace(kilometers_at_change, 300000, 100)
car_data_2_2 = co2analysis(scenarios, driven_distance, 0)
car_data_2[0][2] = car_data_2[0][2] + car_data_2_2[0][2]

car_data_1[0][1] = np.append(car_data_1[0][1], car_data_2[0][1])
car_data_1[0][2] = np.append(car_data_1[0][2], car_data_2[0][2])
car_data.append(car_data_1[0])


# Scenario 6: Köpa elcykel
scenarios = {"6. Köpa elcykel": cars["A: Liten bensinbil"]}
driven_distance = np.linspace(0, kilometers_at_change, 100)
car_data_1 = co2analysis(scenarios, driven_distance, 0)

scenarios = {"tmp1": cars["E: Elcykel"]}
driven_distance = np.linspace(kilometers_at_change, 300000, 100)
car_data_2 = co2analysis(scenarios, driven_distance, car_data_1[0][2][-1] * 1000)
# ([key,driven_distance,C02_data/1000])

car_data_1[0][1] = np.append(car_data_1[0][1], car_data_2[0][1])
car_data_1[0][2] = np.append(car_data_1[0][2], car_data_2[0][2])
car_data.append(car_data_1[0])

# Scenario 7: Aldrig köpa bil
scenarios = {
    "7. Aldrig köpa bil": cars["D: Cykel"],
}
driven_distance = np.linspace(0, 300000, 100)
car_data_1 = co2analysis(scenarios, driven_distance, 0)
car_data.append(car_data_1[0])
# -

plt.figure(figsize=(10, 6), dpi=100)
leg = []
for value in car_data:
    plt.plot(value[1], value[2])
    leg.append(value[0])
plt.legend(leg)
plt.xlabel("kördistans [km]")
plt.ylabel("CO2 [metric tonnes]")
plt.show()

# ## Från det personliga planet till världens fordonsflotta
# Genom att tillgripa en naivistisk analys (vi ger inte någon rabatt då en bil säljs, vilket innebär att inköp av begagnad bil skulle ge en initial-CO2-kostnad av 0 ton och därmed räknar vi inte med avskrivning. Eftersom koldioxid ackumuleras i atmosfären är det dock i vår mening det rimligaste sättet att förhålla sig till problemet) har vi visat hur elektrifiering, i dagens SUV-tider, sällan innebär sänkta koldioxidutsläpp, och en övergång till 10% cykel *i kombination med inköp av elbil* endast är marginellt bättre.
#
# Vad har vi för siffror att förhålla oss till på samhällsnivå? I världen finns det grovt räknat två miljarder bilar. Hur gamla dessa är har jag svårt att hitta siffror för, men den omfattande svenska statistiken har siffror som vi kan tillgripa: I Sverige är en bil i genomsnitt 10år gammal, och skrotas i genomsnitt efter 18år.
#
# Låt oss vidare anta att de svenska förhållandena är representativa för världen i stort och att en bil körs 300000km i genomsnitt innan den skrotas (vilket är siffror som dyker upp vid googling - jag hittar inte någon siffra från scb eller trafa för att bekräfta detta för tillfället).
#
# Slutligen antar vi att bilarna rullar med konstant körsträcka varje år. Det innebär alltså att en tio år gammal genomsnittsbil har:
#
# $$
# \frac{(18-10)}{18}*300000=133333\text{km}
# $$
#
# kvar att köra innan den skrotas. Anta nu att de allra flesta bilar i världsflottan fortfarande är bensinbilar, och att de i genomsnitt har en förbrukning om 0,7l/mil. Vi kan då räkna ut hur många miljarder ton CO2 den befintliga fordonsflottan förväntas släppa ut innan den är förbrukad:

# +
average_remaining_distance = 133333  # km
average_fuel_consumption = 0.07  # l / km
total_number_of_cars = 2e9  # two billion cars world wide

133000 * 0.07 * kgC02_per_litre * 2000000000 / 1000000 / 1000
remaining_CO2_output_from_current_fleet = (
    average_remaining_distance
    * average_fuel_consumption
    * kgC02_per_litre
    * total_number_of_cars
    / 1e9
    / 1e3
)
print("The expected CO2-output from the current world car fleet is approximately")
print("{:3.0f} Gton CO2".format(remaining_CO2_output_from_current_fleet))

# -

# ### Hur mycket är det?
# För att sätta denna siffra i kontext är det lämpligt att gå till IPCC-referensen ovan. När det kommer till kvarvarande budget för koldioxidekvivalentutsläpp säger rapporten detta:
#
# > *For every 1000 GtCO2 emitted by human activity, global surface temperature rises by 0.45°C (best estimate, with a likely
# range from 0.27°C to 0.63°C). The best estimates of the remaining carbon budgets from the beginning of 2020 are
# 500 GtCO2 for a 50% likelihood of limiting global warming to 1.5°C and 1150 GtCO2 for a 67% likelihood of limiting
# warming to 2°C. The stronger the reductions in non-CO2 emissions, the lower the resulting temperatures are for a given
# remaining carbon budget or the larger remaining carbon budget for the same level of temperature change.*
#
# Av de 500 GtCO2 som fanns att tillgå 2020 har omkring 4/5 redan förbrukats. Av den kvarvarande budgeten äter alltså redan den befintliga fordonsflottan upp omkring hälften.
#
# Om vi väljer att växla till en större elbil för alla bilar så kommer den att öka mängden C02-utsläpp till totalt resta 3000000km med:

increase_from_current_fleet_if_electrified = car_data[1][2][-1] / car_data[0][2][-1]
print("{:3.0f} percent".format((increase_from_current_fleet_if_electrified - 1) * 100))


# Vilket ger de totala utsläppen från fordonsflottan istället till:

remaining_CO2_output_from_current_fleet_if_electrified = (
    car_data[1][2][-1] / car_data[0][2][-1] * remaining_CO2_output_from_current_fleet
)
print("The expected CO2-output from the lifetime of the current world car fleet,")
print("when everyone changes to an electric car now, would be approximately")
print("{:3.0f} Gton CO2".format(remaining_CO2_output_from_current_fleet_if_electrified))


# De nya elbilarna, i egenskap av nya, skulle därtill fortsätta släppa ut CO2 så länge inte all elektricitet kommer från fossilfria alternativ i ytterligare nästan 170000km.

# Denna analys har inte tagit hänsyn till CO2-kostnaden för att skapa och upprätthålla väginfrastruktur för dessa miljardvis med vägbundna fordon.
