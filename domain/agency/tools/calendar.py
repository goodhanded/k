from domain.agency import AgentTool

class CalendarTool(AgentTool):
    def _handle_get_events(self, params):
        return "get_events"

    def _handle_add_event(self, params):
        return "add_event"

    def _handle_remove_event(self, params):
        return "remove_event"

    def _handle_update_event(self, params):
        return "update_event"