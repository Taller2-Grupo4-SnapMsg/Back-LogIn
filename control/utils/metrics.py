# auth.py

"""
Module dedicated to classes for metrics
"""
import json
import os
import ssl
import pika

LOGIN_EVENT = "login"
REGISTER_EVENT = "registration"
GEOZONE_EVENT = "geozone"
BLOCK_EVENT = "block"
EMAIL_ENTITY = "email"
GOOGLE_ENTITY = "Google"
BIOMETRICS_ENTITY = "Biometrics"
QUEUE_NAME = "metrics"


class RabbitMQManager:
    """
    Class that manages the rabbitmq channel.

    You can get the rabbitmq queue and send the message yourself
    Or directly call push_metric, which checks the channel and then sends
    the message.
    """

    def __init__(self):
        """
        Start the connection
        """
        self._channel = self._establish_rabbitmq_connection()

    def _establish_rabbitmq_connection(self):
        """
        Function to establish the channel
        for the rabbitmq queue
        """
        rabbitmq_url = os.environ.get("RABBITMQ_URL")
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Create a connection to the RabbitMQ server
        connection_params = pika.URLParameters(rabbitmq_url)
        connection_params.ssl_options = pika.SSLOptions(context, rabbitmq_url)

        connection = pika.BlockingConnection(connection_params)

        return connection.channel()

    def get_channel(self):
        """
        Returns the channel for the connection.
        If the channel was closed, it reestableshes the connection.
        Then returns the valid channel
        """
        if not self._channel or self._channel.is_closed:
            self._channel = self._establish_rabbitmq_connection()
        return self._channel

    def push_metric(self, json_body):
        """
        Gets a valid channel and publishes the metric
        """
        rabbitmq_channel = self.get_channel()
        rabbitmq_channel.basic_publish(
            exchange="", routing_key=QUEUE_NAME, body=json_body
        )


class RegistrationMetric:
    """
    Class to represent a new Registration Metric
    It's initialized with the timestamp_start
    and later the user calls the functions that complete
    the metric
    """

    def __init__(self, timestamp_start):
        """
        initialization
        """
        self.timestamp_start = timestamp_start
        self.timestamp_finish = None
        self.event_type = REGISTER_EVENT
        self.user_email = None

    def set_timestamp_finish(self, timestamp_finish):
        """
        sets up the timestamp_finish
        """
        self.timestamp_finish = timestamp_finish
        return self

    def set_user_email(self, user_email):
        """
        sets up the user email
        """
        self.user_email = user_email
        return self

    def to_json(self):
        """
        converts to a json that can be pushed to the queue
        """
        metrics_dict = {
            "timestamp_start": self.timestamp_start.isoformat(),
            "timestamp_finish": self.timestamp_finish.isoformat(),
            "user_email": self.user_email,
            "event_type": self.event_type,
        }
        return json.dumps(metrics_dict, indent=2)


class LoginMetric:
    """
    Class to represent a new Login Metric
    It's initialized with the timestamp_start
    and later the user calls the functions that complete
    the metric
    """

    def __init__(self, timestamp_start):
        """
        initialization
        """
        self.timestamp_start = timestamp_start
        self.timestamp_finish = None
        self.successful = False
        self.login_entity = EMAIL_ENTITY
        self.event_type = LOGIN_EVENT
        self.user_email = None

    def set_timestamp_finish(self, timestamp_finish):
        """
        sets up the timestamp_finish
        """
        self.timestamp_finish = timestamp_finish
        return self

    def set_user_email(self, user_email):
        """
        sets up the user email
        """
        self.user_email = user_email
        return self

    def set_success(self, successful):
        """
        sets up if the login was successful
        """
        self.successful = successful
        return self

    def set_login_entity(self, login_entity):
        """
        sets up the login entity
        """
        self.login_entity = login_entity
        return self

    def to_json(self):
        """
        converts to a json that can be pushed to the queue
        """
        metrics_dict = {
            "timestamp_start": self.timestamp_start.isoformat(),
            "timestamp_finish": self.timestamp_finish.isoformat(),
            "successful": self.successful,
            "login_entity": self.login_entity,
            "user_email": self.user_email,
            "event_type": self.event_type,
        }
        return json.dumps(metrics_dict, indent=2)


class GeoZoneMetric:
    """
    Class to represent a new GeoZone Metric
    It's initialized with the timestamp_start
    and later the user calls the functions that complete
    the metric
    """

    def __init__(self, timestamp_start):
        """
        initialization
        """
        self.timestamp_start = timestamp_start
        self.timestamp_finish = None
        self.event_type = GEOZONE_EVENT
        self.user_email = None
        self.old_location = None
        self.new_location = None

    def set_timestamp_finish(self, timestamp_finish):
        """
        sets up the timestamp_finish
        """
        self.timestamp_finish = timestamp_finish
        return self

    def set_user_email(self, user_email):
        """
        sets up the user email
        """
        self.user_email = user_email
        return self

    def set_old_location(self, old_location):
        """
        sets up the old location
        """
        self.old_location = old_location
        return self

    def set_new_location(self, new_location):
        """
        sets up the new location
        """
        self.new_location = new_location
        return self

    def to_json(self):
        """
        converts to a json that can be pushed to the queue
        """
        metrics_dict = {
            "timestamp_start": self.timestamp_start.isoformat(),
            "timestamp_finish": self.timestamp_finish.isoformat(),
            "event_type": self.event_type,
            "user_email": self.user_email,
            "old_location": self.old_location,
            "new_location": self.new_location,
        }
        return json.dumps(metrics_dict, indent=2)


class BlockMetric:
    """
    Class to represent a new Block Metric
    It's initialized with the timestamp_start
    and later the user calls the functions that complete
    the metric
    """

    def __init__(self, timestamp_start):
        """
        initialization
        """
        self.timestamp_start = timestamp_start
        self.timestamp_finish = None
        self.event_type = BLOCK_EVENT
        self.user_email = None
        self.admin_email = None
        self.blocked = False

    def set_timestamp_finish(self, timestamp_finish):
        """
        sets up the timestamp_finish
        """
        self.timestamp_finish = timestamp_finish
        return self

    def set_user_email(self, user_email):
        """
        sets up the user email
        """
        self.user_email = user_email
        return self

    def set_admin_email(self, admin_email):
        """
        sets up the admin_email of the admin
        that blocked or unblocked the person
        """
        self.admin_email = admin_email
        return self

    def set_blocked(self, blocked):
        """
        sets up the blocked state
        (True or False)
        """
        self.blocked = blocked
        return self

    def to_json(self):
        """
        converts to a json that can be pushed to the queue
        """
        metrics_dict = {
            "timestamp_start": self.timestamp_start.isoformat(),
            "timestamp_finish": self.timestamp_finish.isoformat(),
            "event_type": self.event_type,
            "user_email": self.user_email,
            "admin_email": self.admin_email,
            "blocked": self.blocked,
        }
        return json.dumps(metrics_dict, indent=2)
