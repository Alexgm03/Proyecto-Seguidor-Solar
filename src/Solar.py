from pysolar.solar import get_altitude, get_azimuth
from datetime import datetime
from pytz import timezone


def getSolarPosition(
    latitude=-0.2105367,
    longitude=-78.491614,
    date=None
):
    """
    Retorna:
        azimuth (grados)
        elevation (grados)
    """

    if date is None:
        date = datetime.now(
            tz=timezone("America/Guayaquil")
        )

    azimuth = get_azimuth(latitude, longitude, date)
    elevation = get_altitude(latitude, longitude, date)

    return azimuth, elevation