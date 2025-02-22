"""Module with helper functions."""

from functools import cache
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from football_commentator.event import FootballEvent
from football_commentator.match_info import Competition, MatchInfo, Team


def filter_timestamp_event(event: FootballEvent, start: int, end: int) -> bool:
    """Get only events from a time range.

    Args:
        event (FootballEvent): a event to verify.
        start (int): Start of the time interval (in sec)
        end (int): End of the time interval (in sec)

    Returns:
        bool: Either the event is within the range or not.
    """
    timestamp = event.timestamp
    timestamp_minutes = int(timestamp[3:5])
    timestamp_seconds = int(timestamp[6:8])

    timestamp_total_sec = 60 * timestamp_minutes + timestamp_seconds
    return start <= timestamp_total_sec <= end


def format_events_to_string(list_events: list[FootballEvent]) -> str:
    """Format the events as str before calling LLM.

    Args:
        list_events (list[FootballEvent]): events' list

    Returns:
        str: Formatted events.
    """
    return "\n\n".join(str(event) for event in list_events)


def load_team_from_config(config_team: dict[str, Any]) -> Team:
    """Load a Team object from config.

    Args:
        config_team (dict[str, str  |  dict[int, str]]): The config.

    Raises:
        KeyError: One of mandatory fields is not present.

    Returns:
        Team: A team object.
    """
    if ("name" not in config_team) or ("logo" not in config_team) or ("lineup" not in config_team):
        raise KeyError(
            "Please Verify that each team have the following fields: 'name', 'logo' and 'lineup'"
        )

    return Team(
        name=config_team["name"],
        logo=config_team["logo"],
        lineup=config_team["lineup"],
    )


def load_competition_from_config(config_competition: dict[str, str]) -> Competition:
    """Load a Competition object from config.

    Args:
        config_competition (dict[str, str]): The config.

    Raises:
        KeyError: One of mandatory fields is not present.

    Returns:
        Team: A Competition object.
    """
    if ("name" not in config_competition) or ("logo" not in config_competition):
        raise KeyError(
            "Please Verify that competition have the following fields: 'name' and 'logo'"
        )
    return Competition(name=config_competition["name"], logo=config_competition["logo"])


@cache
def load_match_info_from_config(path_to_yaml: Path) -> MatchInfo:
    """Load all match info from config file.

    Args:
        path_to_yaml (Path): File with game information (teams, lineups, competition ..)

    Raises:
        KeyError: The file is correctly loaded but a mandatory field is absent.

    Returns:
        MatchInfo: A MatchInfo object representing the game.
    """
    with open(path_to_yaml) as match_info_file:
        match_info = yaml.safe_load(match_info_file)
        # The YAML file is okay, check if all manadatory fields exist.
        if (
            ("HOME_TEAM" not in match_info)
            or ("AWAY_TEAM" not in match_info)
            or ("COMPETITION" not in match_info)
            or ("DATE" not in match_info)
        ):
            raise KeyError(
                "Please ensure you have: 'HOME_TEAM', 'AWAY_TEAM', "
                "'COMPETITION', and 'DATE' fiels in yaml file."
            )

        # Generate the object of both teams and competition
        home_team = load_team_from_config(match_info["HOME_TEAM"])
        away_team = load_team_from_config(match_info["AWAY_TEAM"])
        competition = load_competition_from_config(match_info["COMPETITION"])
        date = match_info["DATE"]

        return MatchInfo(
            home_team=home_team,
            away_team=away_team,
            competition=competition,
            date=date,
        )
