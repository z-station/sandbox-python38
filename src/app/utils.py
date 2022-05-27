import re
from typing import Optional


def clean_str(value: Optional[str]) -> Optional[str]:
    if isinstance(value, str):
        return value.replace('\r', '').rstrip('\n')
    return value


def clean_error(value: Optional[str]) -> Optional[str]:
    if isinstance(value, str):
        value = re.sub(r'\s*File\s+".+\.py",\s+', '', value)
    return value
