"""Backend data class for vehicle."""

import numpy as np


class Vehicle:
    """Class for vehicles."""

    def __init__(self, data) -> None:
        """Initialization."""
        self.name = data[0]
        self.weight = data[1]
        self.battery_capacity = data[2]
        self.consumption_per_km = data[3]
        self.usage = data[4]
        self.co2_build_cost_per_kg = data[5]
        self.co2_battery_build_cost_per_kWh = data[6]
        self.co2_cost_per_consumption = data[7]
        self.vehicle_life_km = data[8]


def co2analysis(car: Vehicle, driven_distance, co2debt):
    """CO2 accumulator function."""
    C02_data_constant = (
        co2debt
        + car.co2_build_cost_per_kg * car.weight
        + car.co2_battery_build_cost_per_kWh * car.battery_capacity
        )
    C02_data = (
        C02_data_constant
        + car.co2_cost_per_consumption
        * car.consumption_per_km
        * (driven_distance - driven_distance[0])
        * car.usage
        )
    car_data = [car, driven_distance, C02_data]

    return car_data
