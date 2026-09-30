from dataclasses import dataclass


# Entities the repository stores. The dict stands in for the database.
# A dataclass, fields only.


@dataclass
class User:
    # Row the repository and the service pass around.
    id: int
    name: str
