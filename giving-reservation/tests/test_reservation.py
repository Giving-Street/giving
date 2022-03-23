from datetime import datetime

from giving_reservation.models import Reservation


def test_reservation_model():
    r = Reservation(
        id=1,
        name="Test",
        purpose="Just Play",
        created_by=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    rc = Reservation(**r.__dict__)  # just copy

    assert r == rc
