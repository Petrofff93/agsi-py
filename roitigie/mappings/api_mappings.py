import enum


class APIType(str, enum.Enum):
    """Enum representing the GIE API: ALSI or AGSI."""

    AGSI = "https://agsi.gie.eu/api/"
    ALSI = "https://alsi.gie.eu/api/"
