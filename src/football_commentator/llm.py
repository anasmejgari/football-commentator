"""Module to handle LLM calls."""

from operator import itemgetter

from langchain.schema.runnable import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from football_commentator.constants import OPENAI_MODEL_NAME
from football_commentator.event import FootballEvent
from football_commentator.prompt import SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE
from football_commentator.utils import format_events_to_string


def invoke_llm(list_events: list[FootballEvent]) -> str:
    """Invoke an LLM to comment on events.

    Args:
        list_events (list[FootballEvent]): list of events to comment.

    Returns:
        str: LLM's commentary on successive events
    """
    # Template for the prompt
    prompt = ChatPromptTemplate.from_messages(
        messages=[("system", SYSTEM_PROMPT_TEMPLATE), ("human", USER_PROMPT_TEMPLATE)],
        template_format="f-string",
    )
    # The model must be set through env variables,
    # Otherwise the default one is gpt-4o-mini
    # Same for the temperature, default is 0.05 (small variability)
    llm = ChatOpenAI(model=OPENAI_MODEL_NAME)  # type: ignore

    # Chain of calling the llm, format events -> Inject in prompt -> Comment
    rag_chain = (  # type: ignore
        {  # type: ignore
            "list_events": itemgetter("list_events") | RunnableLambda(format_events_to_string),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    response = rag_chain.invoke(input={"list_events": list_events})
    return response
