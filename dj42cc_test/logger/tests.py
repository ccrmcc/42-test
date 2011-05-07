from django.test import TestCase
from models import HttpLogEntry
from uuid import uuid4

class LogEmptyTest(TestCase):
    def test_nologs(self):
        logs = HttpLogEntry.objects.all()

        self.assertEqual(logs.count(), 0)

class LogWriteTest(TestCase):
    TRIES = 20
    def test_add(self):
        for x in range(1, self.TRIES):
            self.client.get("/")
            count = HttpLogEntry.objects.count()

            self.assertEqual(count, x)

    def tearDown(self):
        HttpLogEntry.objects.all().delete()

class LogLinkTest(TestCase):
    LINK = ['href="/requests"']
    def test_index_link(self):
        response = self.client.get('/')
        self.assertContains(response, self.LINK)


class LogWriteTest(TestCase):
    TRIES = 20
    PATHS = [str(uuid4()) for x in range(TRIES)]
    PATHS.append("/")

    def test_path(self):
        responses = [
                self.client.get(path)
                for path in self.PATHS
        ]

        logs = HttpLogEntry.objects.all()

        self.assertEqual(logs.count(), len(responses))

        for path, response, log in zip(self.PATHS, responses, logs):
            self.assertEqual(path, log.data.get('path'))
            self.assertEqual("GET", log.data.get("method"))
            self.assertEqual(response.status_code, log.data.get("code"))


    def test_logs_view(self):
        response = self.client.get('/requests')

        for path in self.PATHS[:10]:
            self.assertContains(response, path)



    def tearDown(self):
        HttpLogEntry.objects.all().delete()
