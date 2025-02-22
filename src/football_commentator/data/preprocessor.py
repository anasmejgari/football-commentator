"""Module for preprocessing data."""

from abc import ABC, abstractmethod
from typing import Any

from football_commentator.event import FootballEvent
from football_commentator.utils import filter_timestamp_event


class Preprocessor(ABC):
    """Abstract class to organize preprocessing."""

    def __init__(self):
        """Class Initializer."""
        self.events = []

    @abstractmethod
    def load_player(self, event: dict[str, Any]) -> str | None:
        """Extract player name.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: Name of the player associated to the event.
        """
        pass

    @abstractmethod
    def load_description(self, event: dict[str, Any]) -> str:
        """Extract a description.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: description of the event.
        """
        pass

    @abstractmethod
    def load_loaction(self, event: dict[str, Any]) -> tuple[float | None, float | None]:
        """Extract the position in the field.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            tuple[float | None, float | None]: (X, Y) of the player's position.
        """
        pass

    @abstractmethod
    def load_timestamp(self, event: dict[str, Any]) -> str:
        """Extract timestamp of the event.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: The timestap of the event.
        """
        pass

    @abstractmethod
    def load_event_type(self, event: dict[str, Any]) -> str:
        """Get event type.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: The vent type.
        """
        pass

    @abstractmethod
    def load_team(self, event: dict[str, Any]) -> str:
        """Get team name.

        Args:
            event (dict[str, Any]): event to process

        Returns:
            str: The team associated to the event.
        """
        pass

    def process_football_event(self, event: dict[str, Any]) -> FootballEvent | None:
        """Process one event and generate appropriate representation.

        Args:
            event (dict[str, Any]): The event to process.

        Returns:
            FootballEvent | None: The representation of the event.
        """
        event_type = self.load_event_type(event)
        if event_type != "Starting XI":
            position = self.load_loaction(event)

            event_object = FootballEvent(
                timestamp=self.load_timestamp(event),
                event_type=event_type,
                team=self.load_team(event),
                player=self.load_player(event),
                position_x=position[0],
                position_y=position[1],
                description=self.load_description(event),
            )
            return event_object
        return None

    def load_all_events_in_intervall(self, start: int, end: int) -> list[FootballEvent]:
        """Load all events with a time interval.

        Args:
            start (int): start of the event (game's seconds).
            end (int): start of the event (game's seconds).

        Returns:
            list[FootballEvent]: The list of events that are within the interval.
        """
        events = []
        for event in self.events:
            event_object = self.process_football_event(event)
            if event_object and filter_timestamp_event(event=event_object, start=start, end=end):
                events.append(event_object)
        return events
