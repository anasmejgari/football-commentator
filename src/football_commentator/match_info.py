"""Module to structure a game, plyer, competition and a team."""

import datetime
from dataclasses import dataclass

from openai import BaseModel
from pydantic import field_validator


@dataclass
class Player:
    """Class to represent a player."""

    number: int
    name: str


@dataclass
class Competition:
    """Class to represent a competition."""

    name: str
    logo: str


class Team(BaseModel):
    """Class to represnet a team."""

    name: str
    logo: str
    lineup: list[Player]

    @field_validator("lineup", mode="before")
    @classmethod
    def validate_lineup(cls, v: dict[int, str]) -> list[Player]:
        """Validate the correctness of the line ups fed by the user.

        Args:
            v (dict[int, str]): the lineup dictionnary (jersey number: player name)

        Raises:
            ValueError: The line up is invalid since you don't have 11 players,
                        or players with the same jersey.

        Returns:
            list[Player]: list of player instances
        """
        if len(v) != 11:
            raise ValueError("Please ensure that each line up contains 11 players.")

        list_players = [Player(number, name) for number, name in v.items()]
        return list_players


class MatchInfo(BaseModel):
    """Class to represent a game."""

    competition: Competition
    home_team: Team
    away_team: Team
    date: datetime.date

    @field_validator("date", mode="before")
    def validate_date(cls, date: str) -> datetime.date:
        """Validate the date of the game.

        Args:
            date (str): The dat fed by the user in the config file.

        Returns:
            datetime.date: The date formatted YYYY-MM-DD
        """
        return datetime.date.fromisoformat(date)
