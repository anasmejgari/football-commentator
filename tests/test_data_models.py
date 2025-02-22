from datetime import date

import pytest

from football_commentator.match_info import (Competition, MatchInfo, Player,
                                             Team)


def test_player_creation():
    player = Player(number=10, name="Lionel Messi")
    assert player.number == 10
    assert player.name == "Lionel Messi"


def test_team_creation():
    lineup = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Striker",
        5: "Winger",
        6: "Defender",
        7: "Midfielder",
        8: "Striker",
        9: "Winger",
        10: "Playmaker",
        11: "Striker",
    }
    team = Team(name="Chelsea LFC", logo="https://example.com/logo.png", lineup=lineup)
    assert team.name == "Chelsea LFC"
    assert len(team.lineup) == 11


def test_invalid_team_lineup():
    with pytest.raises(
        ValueError, match="Please ensure that each line up contains 11 players."
    ):
        Team(
            name="Manchester City WFC",
            logo="https://example.com/logo.png",
            lineup={1: "Goalkeeper"},
        )


def test_match_info_creation():
    competition = Competition(
        name="FA Women's Super League", logo="https://example.com/logo.png"
    )
    team_home = Team(
        name="Chelsea LFC",
        logo="https://example.com/logo.png",
        lineup={i: f"Player {i}" for i in range(1, 12)},
    )
    team_away = Team(
        name="Manchester City WFC",
        logo="https://example.com/logo.png",
        lineup={i: f"Player {i}" for i in range(1, 12)},
    )
    match = MatchInfo(
        competition=competition,
        home_team=team_home,
        away_team=team_away,
        date="2024-11-11",
    )

    assert match.date == date(2024, 11, 11)
    assert match.competition.name == "FA Women's Super League"
