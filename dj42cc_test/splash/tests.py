from django.test import TestCase
from models import Person, Contact, OtherContact


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
