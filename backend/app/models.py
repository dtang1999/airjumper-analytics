# models.py
# Define the data structures and validation rules using Pydantic.
# These models are used for parsing and validating incoming JSON payloads from the client.

from pydantic import BaseModel
from typing import List, Optional

class CheckpointData(BaseModel):
    time: float
    jumps: int

class AnalyticsPayload(BaseModel):
    session_id: str
    level_index: int
    regular_platform_count: int
    building_platform_count: int
    total_jump_count: int
    game_over_count: int
    checkpoint_data: List[CheckpointData]
    time_to_flag: float
    jumps_to_flag: int
    health_after_kills: Optional[List[int]]
