from django.test import TestCase
from django.conf import settings


class SettingsPageTest(TestCase):
    KEYS = [
            'STATIC_ROOT',
            'STATIC_URL',
            'TIME_ZONE',
            'ADMIN_MEDIA_PREFIX',
    ]

    def test_page_exists(self):
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, 200)

    def test_settings_values(self):
        response = self.client.get('/settings')
        fmt = '%s = %s'

        for key in self.KEYS:
            value = fmt % (key, getattr(settings, key))
            self.assertContains(response, value)

class IndexLinkTest(TestCase):
    LINK = 'href="/settings"'

    def test_link(self):
        response = self.client.get('/')
        self.assertContains(response, self.LINK)
