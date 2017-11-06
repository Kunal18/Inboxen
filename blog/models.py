# -*- coding: utf-8 -*-
##
#    Copyright (C) 2013, 2014 Jessica Tallon & Matt Molyneaux
#
#    This file is part of Inboxen.
#
#    Inboxen is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Inboxen is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with Inboxen.  If not, see <http://www.gnu.org/licenses/>.
##
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils import safestring
from django.utils.encoding import python_2_unicode_compatible

from django_extensions.db.fields import AutoSlugField
import markdown


@python_2_unicode_compatible
class BlogPost(models.Model):
    """Basic blog post, body stored as MarkDown"""
    subject = models.CharField(max_length=512)
    body = models.TextField()
    date = models.DateTimeField('posted', null=True, blank=True, editable=False)
    modified = models.DateTimeField('modified', auto_now=True, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    draft = models.BooleanField(default=True)

    slug = AutoSlugField(populate_from="subject", max_length=64)

    @property
    def rendered_body(self):
        """Render MarkDown to HTML"""
        return safestring.mark_safe(markdown.markdown(self.body))

    def __str__(self):
        draft = ""
        if self.draft:
            draft = " (draft)"

        if not self.subject:
            subject = "(untitled)"
        elif len(self.subject) > 64:
            subject = "%s…" % self.subject[:63]
        else:
            subject = self.subject

        return "%s%s" % (subject, draft)

    class Meta:
        ordering = ["-date"]
