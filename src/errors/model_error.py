from dataclasses import dataclass




@dataclass(eq=False)
class AppExeption(Exception):
    status_code: int
    detail: str
    error_code: str | None