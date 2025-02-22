"""Module to represent an event in a game."""

from enum import Enum

from pydantic import BaseModel


class EventType(Enum):
    """Enumerate event types."""

    DUEL = "Duel"
    GOAL_KEEPER = "Goal Keeper"
    PASS = "Pass"
    CAMERA_OFF = "Camera off"
    DISPOSSESSED = "Dispossessed"
    SUBSTITUTION = "Substitution"
    CLEARANCE = "Clearance"
    PLAYER_ON = "Player On"
    FOUL_COMMITTED = "Foul Committed"
    DRIBBLED_PAST = "Dribbled Past"
    FOUL_WON = "Foul Won"
    TACTICAL_SHIFT = "Tactical Shift"
    INJURY_STOPPAGE = "Injury Stoppage"
    SHOT = "Shot"
    PRESSURE = "Pressure"
    ERROR = "Error"
    PLAYER_OFF = "Player Off"
    BAD_BEHAVIOUR = "Bad Behaviour"
    INTERCEPTION = "Interception"
    MISCONTROL = "Miscontrol"
    SHIELD = "Shield"
    HALF_START = "Half Start"
    CAMERA_ON = "Camera On"
    OFFSIDE = "Offside"
    STARTING_XI = "Starting XI"
    BALL_RECEIPT = "Ball Receipt*"
    DRIBBLE = "Dribble"
    BLOCK = "Block"
    HALF_END = "Half End"
    BALL_RECOVERY = "Ball Recovery"


class FootballEvent(BaseModel):
    """Represent event's details."""

    team: str
    event_type: str
    timestamp: str
    player: str | None
    position_x: float | None
    position_y: float | None
    description: str
