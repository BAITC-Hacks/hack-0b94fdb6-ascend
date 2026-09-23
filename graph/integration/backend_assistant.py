"""Compatibility adapter; maintained integration lives in ai_agent.api."""

def register_assistant(app, get_snapshot):
    from ai_agent.api import install
    return install(app, get_snapshot, replace_disabled=True)
