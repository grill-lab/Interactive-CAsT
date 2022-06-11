from enum import Enum

class UtteranceType(Enum):
    QUESTION = 1
    REVEALMENT = 2
    FEEDBACK = 3

class ResponseType(Enum):
    ANSWER = 1
    CLARIFICATION = 2
    ELICITATION = 3
    FEEDBACK = 4
    SUGGESTION = 5