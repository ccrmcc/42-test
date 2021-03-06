from django.test import TestCase
from django.utils import simplejson

from models import Person, Contact, OtherContact
from uuid import uuid4
from random import randint


class DbLoadedTest(TestCase):
    def test_person_exists(self):
        person = Person.objects.get()
        self.assertIsNotNone(person)

    def test_contacts_loaded(self):
        contacts = Contact.objects.all()

        self.assertNotEqual(contacts.count(), 0)

    def test_othercontacts_loaded(self):
        other_contacts = OtherContact.objects.all()

        self.assertNotEqual(other_contacts.count(), 0)


class IndexOkTest(TestCase):
    def test_index_ok(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_person(self):
        person = Person.objects.get()
        response = self.client.get('/')

        self.assertContains(response, person.first_name)
        self.assertContains(response, person.last_name)
        self.assertContains(response, person.bio)

        # TODO: cant test birth_date, because of locale
        #self.assertContains(response, person.birth_date)

    def test_index_contacts(self):
        contacts = Contact.objects.all()
        response = self.client.get('/')

        for contact in contacts:
            self.assertContains(response, contact.typ)
            self.assertContains(response, contact.value)

    def test_index_no_contacts(self):
        contacts = list(Contact.objects.all())
        Contact.objects.all().delete()

        response = self.client.get('/')
        for contact in contacts:
            self.assertNotContains(response, contact.typ)
            self.assertNotContains(response, contact.value)

    def test_index_other_contact(self):

        other = OtherContact.objects.get()

        response = self.client.get('/')
        self.assertContains(response, other.value)

    def test_index_no_other_contact(self):

        other = OtherContact.objects.get()
        other.delete()

        response = self.client.get('/')
        self.assertNotContains(response, other.value)

LOGIN = {
        "username": "admin",
        "password": "admin",
}


class EditDataTest(TestCase):
    FN = 'FN_%s' % str(uuid4())
    LN = 'LN %s' % str(uuid4())

    MAIL = 'me%d@example.com' % randint(1, 2 ** 32)
    JABBER = 'me%d@jabber.org' % randint(1, 2 ** 32)
    SKYPE = 'me%d_2011' % randint(1, 2 ** 32)
    OTHER = ('%s ' % str(uuid4())) * randint(1, 10)

    CONTACTS = {
            'email': MAIL,
            'jabber': JABBER,
            'skype': SKYPE,
            'value': OTHER,
    }

    @classmethod
    def load_data(cls):
        person = Person.objects.get()

        ret = {
                "first_name": person.first_name,
                "last_name": person.last_name,
                "bio": person.bio,
                "birth_date": person.birth_date,  # hmmm
        }

        for x, contact in enumerate(person.contact_set.all()):
            ret['contact_set-%d-person' % x] = person.pk
            ret['contact_set-%d-typ' % x] = contact.typ
            ret['contact_set-%d-value' % x] = contact.value
            ret['contact_set-%d-id' % x] = contact.id

            fake = cls.CONTACTS[contact.typ]
            cls.CONTACTS['contact_set-%d-value' % x] = fake

        MAX = x + 1
        ret['contact_set-TOTAL_FORMS'] = MAX
        ret['contact_set-INITIAL_FORMS'] = MAX

        other_contact = person.othercontact_set.all().get()

        ret['value'] = other_contact.value
        ret['person'] = person.pk

        return ret

    def test_edit_name(self):
        data = self.load_data()

        data['first_name'] = self.FN
        data['last_name'] = self.LN

        self.client.post("/accounts/login/", LOGIN)

        response = self.client.post("/contact_edit", data)
        self.assertRedirects(response, "/")

        response = self.client.get('/')
        self.assertContains(response, self.FN)
        self.assertContains(response, self.LN)

    def test_edit_contacts(self):
        data = self.load_data()
        data.update(self.CONTACTS)

        self.client.post("/accounts/login/", LOGIN)

        response = self.client.post("/contact_edit", data)
        self.assertRedirects(response, "/")

        response = self.client.get('/')
        for value in self.CONTACTS.values():
            self.assertContains(response, value)

    def test_login(self):
        data = self.load_data()
        data['first_name'] = 'ZOMG p0wned'
        response = self.client.post("/contact_edit", data)

        self.assertRedirects(response, "/accounts/login/?next=/contact_edit")

        person = Person.objects.get()
        self.assertNotEqual(person.first_name, data['first_name'])


class ViewFormTest(TestCase):
    def test_csrf_token(self):
        self.client.post("/accounts/login/", LOGIN)

        response = self.client.get("/contact_edit")
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_get_form(self):
        self.client.post("/accounts/login/", LOGIN)

        response = self.client.get("/contact_edit")
        self.assertEqual(response.status_code, 200)

        data = EditDataTest.load_data()

        check_keys = data.keys()

        for key in check_keys:
            self.assertContains(response, data[key])


class IndexEditLinkTest(TestCase):
    LINK = 'href="/contact_edit"'

    def test_link(self):
        response = self.client.get("/")

        self.assertContains(response, self.LINK)


class EditJqueryTest(TestCase):
    DATEPICKER = 'class="jquery-date"'
    JQUERY = ['jquery.min.js', 'jquery-ui.min.js', 'jquery-ui.css',
            'jquery.form.min.js', ]

    def test_classname(self):

        self.client.post("/accounts/login/", LOGIN)

        response = self.client.get("/contact_edit")
        self.assertContains(response, self.DATEPICKER)

    def test_jquery(self):
        self.client.post("/accounts/login/", LOGIN)
        response = self.client.get("/contact_edit")

        for js in self.JQUERY:
            self.assertContains(response, js)


class EditPutTest(TestCase):
    def test_json_errors(self):
        self.client.post("/accounts/login/", LOGIN)
        response = self.client.get("/contact_edit/ajax")

        self.assertEqual(response.status_code, 405)


class EditAjaxError(TestCase):
    def test_json_errors(self):
        self.client.post("/accounts/login/", LOGIN)
        data = EditDataTest.load_data()
        fail_keys = []
        for key in data.keys():
            if 'value' in key:
                data.pop(key)
                fail_keys.append(key)

        response = self.client.post("/contact_edit/ajax", data)

        errors = simplejson.loads(response.content)

        field_errors = errors['fields']
        data = EditDataTest.load_data()

        for key in fail_keys:
            err = field_errors.get(key)[0]
            self.assertEqual('This field is required.', err)


class EditHtmlError(TestCase):
    def test_html_errors(self):
        self.client.post("/accounts/login/", LOGIN)
        data = EditDataTest.load_data()
        fail_keys = []
        for key in data.keys():
            if '-value' in key:
                data.pop(key)
                fail_keys.append(key)

        response = self.client.post("/contact_edit", data)

        errors = len(fail_keys)
        self.assertContains(response, 'This field is required.', errors)


class AdminLinkTest(TestCase):
    URL = '/admin/splash/person/1/'
    LINK = 'href="%s"' % URL

    def test_link(self):
        response = self.client.get("/")
        self.assertContains(response, self.LINK)
