from typing import Any, Optional
from dataclasses import dataclass


@dataclass
class Address:
    country: str
    street: str
    zipCode: str
    city: str

    def to_dict(self) -> dict[str, str]:
        return {
            "country": self.country,
            "street": self.street,
            "zipCode": self.zipCode,
            "city": self.city,
        }


@dataclass
class GeoCoordinate:
    longitude: float
    latitude: float

    def to_dict(self) -> dict[str, float]:
        return {"longitude": self.longitude, "latitude": self.latitude}


class Destination:
    def __init__(
        self,
        address: Optional[Address] = None,
        geoCoordinate: Optional[GeoCoordinate] = None,
        name: str = "Destination",
        poiProvider: str = "unknown",
    ):
        if address is None and geoCoordinate is None:
            raise ValueError("At least one of address or lat/lon must be provided.")
        if address is not None and geoCoordinate is not None:
            raise ValueError("Only one of address or lat/lon must be provided.")

        self.address = address
        self.geoCoordinate = geoCoordinate
        self.name = name
        self.poiProvider = poiProvider

    def valid(self) -> bool:
        return bool(self.name) and (self.address is not None or self.geoCoordinate is not None)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "poiProvider": self.poiProvider,
            "destinationName": self.name,
            "destinationSource": "MobileApp",
        }

        if self.address is not None:
            data["address"] = self.address.to_dict()
        elif self.geoCoordinate is not None:
            data["geoCoordinate"] = self.geoCoordinate.to_dict()

        return data


class Route:
    def __init__(self, destinations: list[Destination] = []):
        if (
            destinations is None
            or not isinstance(destinations, list)
            or not all(isinstance(dest, Destination) for dest in destinations)
        ):
            raise ValueError("destinations must be a list of Destination objects.")

        self.destinations = destinations

    def valid(self) -> bool:
        return bool(self.destinations) and all(
            isinstance(dest, Destination) and dest.valid() for dest in self.destinations
        )

    def to_list(self) -> list[dict[str, Any]]:
        route = []
        for i, destination in enumerate(self.destinations):
            data = destination.to_dict()
            if i < len(self.destinations) - 1:
                data["destinationType"] = "stopover"
            route.append(data)

        return route
