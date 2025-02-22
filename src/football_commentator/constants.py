"""Module to store constants."""

import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")
if OPENAI_MODEL_NAME is None:
    OPENAI_MODEL_NAME = "gpt-4o-mini"

retrieved_temperature = os.getenv("MODEL_TEMPERATURE")
MODEL_TEMPERATURE = 0.05 if retrieved_temperature is None else float(retrieved_temperature)

PATH_MATCH_INFO = os.getenv("MATCH_METADATA_PATH")
SOURCE_EVENTS = os.getenv("SOURCE_EVENTS")
SUPPORTED_EVENTS = {
    "goalkeeper",
    "pass",
    "dribble",
    "shot",
    "bad_behaviour",
    "interception",
    "ball_receipt",
    "duel",
}
