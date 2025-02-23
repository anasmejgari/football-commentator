"""Module to preprocess JSON-based data."""

import json
from pathlib import Path
from typing import Any

from football_commentator.constants import SUPPORTED_EVENTS
from football_commentator.data.preprocessor import Preprocessor


class JSONPreprocessor(Preprocessor):
    """Class to preprocess JSON data."""

    def __init__(self, source: Path):
        """Initialize class.

        Args:
            source (Path): path to JSON source data.

        Raises:
            ValueError: The file is not of JSON format.
        """
        super().__init__()
        if source.suffix != ".json":
            raise ValueError(f"The '{source.suffix}' is not yet supported to store events.")
        with open(source) as file:
            self.events: list[dict[str, Any]] = json.load(file)

    def load_player(self, event: dict[str, Any]) -> str | None:
        """Extract player name.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: Name of the player associated to the event.
        """
        if "player" in event and ("name" in event["player"]):
            player = event["player"]["name"]
        else:
            player = None
        return player

    def load_description(self, event: dict[str, Any]) -> str:
        """Extract a description.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: description of the event.
        """
        # The structure of file introduce some fields provindin description
        # Those fields have dict as value
        # A field 'name' contains description of this field
        description: dict[str, str] = {}

        for event_detail in SUPPORTED_EVENTS.intersection(event.keys()):
            details: dict[str, Any] = event[event_detail]
            for key, val in details.items():  # Check if name is in the field.
                if (isinstance(val, dict)) and ("name" in val):
                    description[key] = val["name"]

        # Generate textual description
        text_description = "Additional Informations: " + ", ".join(
            f"({key}: {val})" for key, val in description.items()
        )
        return text_description

    def load_loaction(self, event: dict[str, Any]) -> tuple[float | None, float | None]:
        """Extract the position in the field.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            tuple[float | None, float | None]: (X, Y) of the player's position.
        """
        if "location" in event:
            position_x = event["location"][0]
            position_y = event["location"][1]
        else:
            position_x = None
            position_y = None
        return position_x, position_y

    def load_timestamp(self, event: dict[str, Any]) -> str:
        """Extract timestamp of the event.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: The timestap of the event.
        """
        return event["timestamp"]

    def load_event_type(self, event: dict[str, Any]) -> str:
        """Get event type.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: The vent type.
        """
        return event["type"]["name"]

    def load_team(self, event: dict[str, Any]) -> str:
        """Get team name.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: The team associated to the event.
        """
        return event["team"]["name"]
