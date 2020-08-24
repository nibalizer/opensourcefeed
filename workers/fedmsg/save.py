# GPL 2.0
# Portions (c) Fedora Maintainers
# Portions (c) IBM

import os
import requests

from fedora_messaging import config

ttvopenfeed_host = "localhost:3000"

def format_output(event):
    str_rep = "User: {0} did a {1} on {2} at {3}".format()


def submit_event(ev_str):
    requests.post("http://" + ttvopenfeed_host + "/submit",
                  json={"message": ev_str})


class SaveMessage(object):
    """
    A fedora-messaging consumer that saves the message to a file.

    A single configuration key is used from fedora-messaging's
    "consumer_config" key, "path", which is where the consumer will save
    the messages::

        [consumer_config]
        path = "/tmp/fedora-messaging/messages.txt"
    """

    def __init__(self):
        """Perform some one-time initialization for the consumer."""
        self.path = config.conf["consumer_config"]["path"]

        # Ensure the path exists before the consumer starts
        if not os.path.exists(os.path.dirname(self.path)):
            os.mkdir(os.path.dirname(self.path))

    def __call__(self, message):
        """
        Invoked when a message is received by the consumer.

        Args:
            message (fedora_messaging.api.Message): The message from AMQP.
        """

        # TODO handle these events
        # - org.fedoraproject.prod.github.pull_request.opened
        # - org.fedoraproject.prod.github.issue.comment
        # - org.fedoraproject.prod.github.status
        # - org.fedoraproject.prod.github.pull_request_review

        # handle comment added
        if message.topic == 'org.fedoraproject.prod.pagure.pull-request.comment.added':
            print(message.body)
            # body.
            print(message.body["pullrequest"]["comments"]["comment"])
            # TODO handle this event

        if message.topic == "org.fedoraproject.prod.hotness.update.drop":
            print(message.body)
            project_name = message.body['trigger']['msg']['project']['name']
            project_version = message.body['trigger']['msg']['project']['version']
            project_backend = message.body['trigger']['msg']['project']['backend']
            event = "[{0}] New Upstream Release. Project: {1} Version: {2}".format(project_backend, project_name, project_version)
            print(event)
            submit_event(event)

