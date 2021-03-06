##
#    Copyright (C) 2018 Jessica Tallon & Matt Molyneaux
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

from cms.templatetags import cms_tags
from inboxen.test import InboxenTestCase


class CmsTemplateTagTestCase(InboxenTestCase):
    def test_live(self):
        output = cms_tags.render_live(True)
        self.assertIn('<span class="label label-primary"', output)
        self.assertNotIn("Draft", output)
        self.assertIn("Live", output)

        output = cms_tags.render_live(False)
        self.assertIn('<span class="label label-default"', output)
        self.assertIn("Draft", output)
        self.assertNotIn("Live", output)

    def test_in_menu(self):
        output = cms_tags.render_in_menu(True)
        self.assertIn('<span class="label label-primary"', output)
        self.assertIn("In menu", output)

        output = cms_tags.render_in_menu(False)
        self.assertEqual(output, "&nbsp;")
