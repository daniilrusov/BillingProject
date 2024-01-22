from dataclasses import dataclass
import numpy as np

@dataclass
class Task:
    job_id: int
    model: str
    status: str
    data: list
    result: str = None
