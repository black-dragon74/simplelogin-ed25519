import arrow
import newrelic.agent

from app.log import LOG
from app.models import SyncEvent
from events.event_sink import EventSink
from events.event_source import EventSource


class Runner:
    def __init__(self, source: EventSource, sink: EventSink):
        self.__source = source
        self.__sink = sink

    def run(self):
        self.__source.run(self.__on_event)

    @newrelic.agent.background_task()
    def __on_event(self, event: SyncEvent):
        try:
            can_process = event.mark_as_taken()
            if can_process:
                event_created_at = event.created_at
                start_time = arrow.now()
                success = self.__sink.process(event)
                if success:
                    event_id = event.id
                    SyncEvent.delete(event.id, commit=True)
                    LOG.info(f"Marked {event_id} as done")

                    end_time = arrow.now() - start_time
                    time_between_taken_and_created = start_time - event_created_at

                    newrelic.agent.record_custom_metric(
                        "Custom/sync_event_processed", 1
                    )
                    newrelic.agent.record_custom_metric(
                        "Custom/sync_event_process_time", end_time.total_seconds()
                    )
                    newrelic.agent.record_custom_metric(
                        "Custom/sync_event_elapsed_time",
                        time_between_taken_and_created.total_seconds(),
                    )
            else:
                LOG.info(f"{event.id} was handled by another runner")
        except Exception as e:
            LOG.warn(f"Exception processing event [id={event.id}]: {e}")
            newrelic.agent.record_custom_metric("Custom/sync_event_failed", 1)
