from datetime import datetime
from dataclasses import dataclass
from typing import NamedTuple


def get_current_year() -> str:
    return str(datetime.now().year)

class RangeYear(NamedTuple):
    year_from:str = '0'
    year_to:str = '2025'

    def is_default(self):
        return self.year_from =='0' and self.year_to == get_current_year()