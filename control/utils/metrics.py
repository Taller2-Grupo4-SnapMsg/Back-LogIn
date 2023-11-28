# auth.py

"""
Module dedicated to classes for metrics
"""
import json

LOGIN_EVENT = "login"
REGISTER_EVENT = "registration"
GEOZONE_EVENT = "geozone"
EMAIL_ENTITY = "email"
GOOGLE_ENTITY = "Google"
QUEUE_NAME = "metrics"


class RegistrationMetric:
    """
    Class to represent a new Registration Metric
    It's initialized with the timestamp_start
    and later the user calls the function that complete
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
    and later the user calls the function that complete
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
    and later the user calls the function that complete
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
