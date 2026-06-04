import unittest
from unittest.mock import Mock

from database import postgres


class FakeCursor:
    def __init__(self, inserted_job):
        self.inserted_job = inserted_job
        self.executed_sql = ""

    def execute(self, sql, params):
        self.executed_sql = sql
        self.params = params

    def fetchone(self):
        return (1,) if self.inserted_job else None

    def close(self):
        pass


class FakeConnection:
    def __init__(self, inserted_job):
        self.cursor_instance = FakeCursor(inserted_job)
        self.committed = False
        self.closed = False

    def cursor(self):
        return self.cursor_instance

    def commit(self):
        self.committed = True

    def close(self):
        self.closed = True


class SaveJobNotificationTests(unittest.TestCase):
    def setUp(self):
        self.original_get_connection = postgres.get_connection
        self.original_notify_new_job = getattr(postgres, "notify_new_job", None)

    def tearDown(self):
        postgres.get_connection = self.original_get_connection
        if self.original_notify_new_job is None:
            if hasattr(postgres, "notify_new_job"):
                delattr(postgres, "notify_new_job")
        else:
            postgres.notify_new_job = self.original_notify_new_job

    def test_notifies_when_job_is_new(self):
        conn = FakeConnection(inserted_job=True)
        notifier = Mock()
        postgres.get_connection = lambda: conn
        postgres.notify_new_job = notifier

        postgres.save_job("https://example.com/job/1", "software intern", "Example Co")

        self.assertIn("RETURNING id", conn.cursor_instance.executed_sql)
        notifier.assert_called_once_with(
            "https://example.com/job/1",
            "software intern",
            "Example Co",
        )

    def test_does_not_notify_when_job_already_exists(self):
        conn = FakeConnection(inserted_job=False)
        notifier = Mock()
        postgres.get_connection = lambda: conn
        postgres.notify_new_job = notifier

        postgres.save_job("https://example.com/job/1", "software intern", "Example Co")

        notifier.assert_not_called()


if __name__ == "__main__":
    unittest.main()
