from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    bio = models.TextField()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def get_contacts(self):
        ret = {}
        for contact in self.contact_set.all():
            ret[contact.typ] = contact.value

        # FIXME: what if not other?
        other = self.othercontact_set.all().get()

        ret['other'] = other.value

        return ret

    def set_contacts(self, value):
        if not isinstance(value, dict):
            raise ValueError("Contacts should be dict!")

        for contact in self.contact_set.all():
            if contact.typ in value:
                contact.value = value.get(contact.typ)
                contact.save()

        if not 'other' in value:
            return

        other = self.othercontact_set.all().get()
        other.value = value.get('other')
        other.save()

    contacts = property(get_contacts, set_contacts)


class Contact(models.Model):
    TYP_CHOICES = (
        ("skype", "Skype"),
        ("jabber", "JID"),
        ("email", "E-mail"),
    )
    typ = models.CharField(max_length=20, choices=TYP_CHOICES)
    value = models.CharField(max_length=50)
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return u'%s contact of %s' % (self.typ, self.person)


# FIXME: should this really live in separete model?
class OtherContact(models.Model):
    person = models.ForeignKey(Person)
    value = models.TextField()

    def __unicode__(self):
        return u'other contact of %s' % self.person
