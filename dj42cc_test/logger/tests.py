from django.test import TestCase
from models import HttpLogEntry

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
