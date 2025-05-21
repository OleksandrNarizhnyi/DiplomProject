from enum import Enum


class RoomType(str, Enum):
    APARTMENT = "Apartment"
    SUITE = "Suit"
    SHARED_ROOM = "Shared room"
    PRIVATE_ROOM_IN_SHARED = "Private room in shared"
    LOFT = "Loft"
    STUDIO = "Studio"

    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]