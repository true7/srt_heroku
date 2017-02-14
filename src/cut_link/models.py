from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from .utils import create_shortlink
from .validators import validate_url

SHORTLINK_MAX = getattr(settings, "SHORTLINK_MAX", 15)


class CutURLManager(models.Manager):

    def all(self, *args, **kwargs):
        qs_main = super(CutURLManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)
        return qs

    # def active_links(self, *args, **kwargs):
    #     return super(CutURLManager, self).filter(active=True, *args, **kwargs)

    def refresh(self, items=None):
        # following code == objects.all() in normal model manager
        # but I override it, so I need to go this way
        qs = CutURL.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('timestamp')[:items]
        new_codes = 0
        for q in qs:
            q.shortlink = create_shortlink(q)
            q.save()
            new_codes += 1


class CutURL(models.Model):
    url = models.CharField(max_length=1000, validators=[validate_url, ])
    shortlink = models.CharField(max_length=SHORTLINK_MAX, unique=True, blank=True)
    pub_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = CutURLManager()

    def save(self, *args, **kwargs):
        if not self.shortlink:
            self.shortlink = create_shortlink(self)
        # if not self.url.startswith('http'):
        #     self.url = 'http://' + self.url
        super(CutURL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)

    def get_short_url(self):
        return reverse('cut:short', kwargs={'shortlink': self.shortlink})
