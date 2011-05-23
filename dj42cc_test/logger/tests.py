from django.test import TestCase
from models import HttpLogEntry, ModelLogEntry
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
    LINK = 'href="/requests"'

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
                for path in self.PATHS]

        logs = HttpLogEntry.objects.all()

        self.assertEqual(logs.count(), len(responses))

        for path, response, log in zip(self.PATHS, responses, logs):
            self.assertEqual(path, log.data.get('path'))
            self.assertEqual("GET", log.data.get("method"))
            self.assertEqual(response.status_code, log.data.get("code"))

    def tearDown(self):
        HttpLogEntry.objects.all().delete()


class LogPathsTest(TestCase):
    TRIES = 20
    PATHS = [str(uuid4()) for x in range(TRIES)]
    PATHS.append("/")

    def test_logs_view(self):
        responses = [
                self.client.get(path)
                for path in self.PATHS]

        response = self.client.get('/requests')

        for path in self.PATHS[:10]:
            self.assertContains(response, path)

    def tearDown(self):
        HttpLogEntry.objects.all().delete()


class LogDbTest(TestCase):
    def setUp(self):
        ModelLogEntry.objects.all().delete()

    def test_create(self,):

        ModelLogEntry.objects.all().delete()
        http = HttpLogEntry(data="crap")
        http.save()

        log_all = ModelLogEntry.objects.filter(action='create')

        self.assertEqual(1, log_all.count())
        log = log_all.get()
        self.assertEqual(log.action, 'create')
        self.assertEqual(log.model_name, 'logger.httplogentry')
        self.assertEqual(log.changed_pk, http.pk)

    def test_edit(self,):
        ModelLogEntry.objects.all().delete()
        http = HttpLogEntry(data="crap")
        http.save()

        http.data = [1, 2, 3]
        http.save()

        log_all = ModelLogEntry.objects.filter(action='edit')

        self.assertEqual(1, log_all.count())

        log = log_all.get()
        self.assertEqual(log.action, 'edit')
        self.assertEqual(log.model_name, 'logger.httplogentry')
        self.assertEqual(log.changed_pk, http.pk)

    def test_delete(self,):
        ModelLogEntry.objects.all().delete()
        http = HttpLogEntry(data="crap")
        http.save()

        pk = http.pk

        http.delete()

        log_all = ModelLogEntry.objects.all()

        self.assertEqual(2, log_all.count())

        log_all = ModelLogEntry.objects.filter(action='delete')

        self.assertEqual(1, log_all.count())

        log = log_all.get()
        self.assertEqual(log.action, 'delete')
        self.assertEqual(log.model_name, 'logger.httplogentry')
        self.assertEqual(log.changed_pk, pk)


class HttpPriorityTest(TestCase):
    TRIES = 30

    def setUp(self):
        HttpLogEntry.objects.all().delete()

        for x in range(self.TRIES):
            self.client.get("/")

    def tearDown(self):
        HttpLogEntry.objects.all().delete()

    def test_priority(self):

        log = HttpLogEntry.objects.all()[0]

        assert hasattr(log, 'priority')

    def test_edit_priority(self):
        log = HttpLogEntry.objects.all()[0]

        pri = log.priority or 0  # handle None
        pri += 1

        PREFIX = "httplogentry-%d-%s"
        _PREFIX = "httplogentry-%s-FORMS"

        data = {
                PREFIX % (0, "id"): log.pk,
                PREFIX % (0, "priority"): pri,
                _PREFIX % 'TOTAL': 1,
                _PREFIX % 'MAX': 1,
        }

        response = self.client.post("/reqiests/edit", data)
        self.assertRedirects(response, "/response")

        edit_log = HttpLogEntry.objects.get(pk=log.pk)

        self.assertEqual(edit_log.priority, pri)
