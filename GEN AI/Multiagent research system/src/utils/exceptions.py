class AgentError(Exception):
    """Base class for agent-related errors."""
    pass

class ResearcherError(AgentError):
    pass

class SummarizerError(AgentError):
    pass

class WriterError(AgentError):
    pass
