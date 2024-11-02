"""Backend data class and some methods for vehicle."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Vehicle:
    """Class for vehicles."""

    name: str
    weight: int
    battery_capacity: int
    consumption_per_km: int
    co2_build_cost_per_kg: int
    co2_battery_build_cost_per_kWh: int
    co2_cost_per_consumption: int
    vehicle_life_km: int


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
    )

    return driven_distance, C02_data
