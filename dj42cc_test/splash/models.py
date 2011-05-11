from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    bio = models.TextField()

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)


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
