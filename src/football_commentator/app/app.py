"""Module for the streamlit interface."""

import time
from pathlib import Path

import streamlit as st

from football_commentator.constants import PATH_MATCH_INFO, SOURCE_EVENTS
from football_commentator.data.preprocessor_json import JSONPreprocessor
from football_commentator.llm import invoke_llm
from football_commentator.utils import load_match_info_from_config

MATCH_INFO = load_match_info_from_config(PATH_MATCH_INFO)


# ----------------- Remove top space with custom CSS -----------------
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    /* Remove top padding in the main content area */
    .main .block-container {
        padding-top: 0rem;
    }
    /* Remove top padding in the sidebar */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem;
        margin-top: 0rem;
    }

    /* Styles for commentary presentation */
    .commentary-container {
      width: 80%;
      margin: auto;
      padding: 20px;
      background-color: #f9f9f9;
      border-radius: 10px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      max-height: 500px;
      overflow-y: auto;
    }
    .commentary-entry {
      padding: 10px;
      margin-bottom: 10px;
      border-left: 4px solid #007bff;
      background-color: #fff;
      border-radius: 5px;
    }
    .commentary-time {
      font-weight: bold;
      margin-right: 10px;
      color: #333;
    }
    .commentary-text {
      font-size: 16px;
      color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- Session State Setup -----------------
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "comment_index" not in st.session_state:
    st.session_state.comment_index = 0
if "commentary_data" not in st.session_state:
    st.session_state.commentary_data = []

SCORE = {"HOME_TEAM": 0, "AWAY_TEAM": 0}

# ----------------- Sidebar (Left Side) -----------------
with st.sidebar:
    competition_header_html = f"""
    <div style="text-align: center; font-size: 24px; font-weight: bold; margin-bottom: 10px;">
        {MATCH_INFO.competition.name} | {MATCH_INFO.date}
    </div>
    """
    st.sidebar.markdown(competition_header_html, unsafe_allow_html=True)
    # Placeholder for the timer
    timer_placeholder = st.empty()

    # Team Info
    team_html = f"""
    <div style="padding: 10px;">
      <div style="display: flex; justify-content: space-around; align-items: flex-start;">
        <!-- HOME TEAM Block -->
        <div style="text-align: center;">
            <img src="{MATCH_INFO.home_team.logo}" width="80"><br>
            <h2 style="margin-bottom: 5px;">{MATCH_INFO.home_team.name}</h2>
            <h1 style="margin-top: 0px;">{SCORE["HOME_TEAM"]}</h1>
            <h4 style="margin-bottom: 5px;">Line-up</h4>
            <ul style="list-style: none; padding: 0; text-align: left;">
    """
    for player in MATCH_INFO.home_team.lineup:
        team_html += f"<li>{player.number}.{player.name}</li>"
    team_html += """
            </ul>
        </div>
        <!-- AWAY TEAM Block -->
        <div style="text-align: center;">
            <img src="{away_logo}" width="80"><br>
            <h2 style="margin-bottom: 5px;">{away_name}</h2>
            <h1 style="margin-top: 0px;">{away_score}</h1>
            <h4 style="margin-bottom: 5px;">Line-up</h4>
            <ul style="list-style: none; padding: 0; text-align: left;">
    """.format(
        away_logo=MATCH_INFO.away_team.logo,
        away_name=MATCH_INFO.away_team.name,
        away_score=SCORE["AWAY_TEAM"],
    )
    for player in MATCH_INFO.away_team.lineup:
        team_html += f"<li>{player.number}.{player.name}</li>"
    team_html += """
            </ul>
        </div>
      </div>
    </div>
    """
    st.markdown(team_html, unsafe_allow_html=True)

# ----------------- Main Area (Right Side) -----------------
# Header with Title (left) and Competition Logo (right)
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("<h1>Live Commentary</h1>", unsafe_allow_html=True)
with col2:
    st.image(MATCH_INFO.competition.logo, width=80)

# Commentary container placeholder
commentary_placeholder = st.empty()

# ----------------- Add Initial Kick Off Event -----------------
st.session_state.commentary_data.append({"Time": "00'00", "Commentary": "Kick Off"})

last_minutes, last_secondes = 0, 0
# ----------------- Main Loop -----------------
while True:
    # Calculate elapsed time for the timer
    elapsed = time.time() - st.session_state.start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    timer_str = f"{minutes:02d}'{seconds:02d}"

    # Update the timer in the sidebar with a nice gradient
    timer_html = f"""
    <div style="text-align:center; font-size:36px; font-weight:bold;
         background: linear-gradient(to right, #6a11cb, #2575fc); color:white;
         padding:10px; border-radius:10px; margin-bottom:10px;">
         {timer_str}
    </div>
    """
    timer_placeholder.markdown(timer_html, unsafe_allow_html=True)

    # Every 20 seconds, add a new commentary if available
    if (seconds in (20, 40, 0)) and (minutes != 0 or seconds != 0):
        new_events = JSONPreprocessor(
            source=Path(str(SOURCE_EVENTS))
        ).load_all_events_in_intervall(
            start=60 * last_minutes + last_secondes,
            end=60 * minutes + seconds,
        )
        response = invoke_llm(new_events)

        new_entry = {
            "Time": timer_str,
            "Commentary": response,
        }
        st.session_state.commentary_data.append(new_entry)
        st.session_state.comment_index += 1
        last_minutes, last_secondes = minutes, seconds

    # Build custom HTML for commentary container (no sliding animation)
    commentary_html = """<div class="commentary-container">"""
    commentary_html_list = "".join(
        [
            f'<div class="commentary-entry"><span class="commentary-time">{entry["Time"]}'
            f'</span> <span class="commentary-text">{entry["Commentary"]}</span></div>'
            for entry in st.session_state.commentary_data
        ]
    )
    commentary_html += f"{commentary_html_list}\n</div>"

    # Render the commentary container
    commentary_placeholder.markdown(commentary_html, unsafe_allow_html=True)

    time.sleep(1)
