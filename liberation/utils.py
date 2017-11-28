##
#    Copyright (C) 2013, 2014, 2015, 2016, 2017 Jessica Tallon & Matt Molyneaux
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

from email.header import Header
from email.message import Message
from io import BytesIO
import base64
import quopri
import uu

import six

from inboxen.models import HEADER_PARAMS


INBOXEN_ENCODING_ERROR_HEADER_NAME = "Inboxen-Liberation-Error"


def _add_error(msg, error_msg):
    msg[INBOXEN_ENCODING_ERROR_HEADER_NAME] = error_msg


def set_base64_payload(msg, data):
    """Encodees the payload with base64"""
    enc_data = base64.standard_b64encode(data)
    msg.set_payload(enc_data)


def set_quopri_payload(msg, data):
    """Encodees the payload with quoted-printable"""
    # this won't encode spaces if binascii is not available
    enc_data = quopri.encodestring(data, True)
    msg.set_payload(enc_data)


def set_uuencode_payload(msg, data):
    """Encodees the payload with uuencode"""
    outfile = BytesIO()

    ct = msg.get("Content-Type", "")
    cd = msg.get("Content-Disposition", "")

    params = dict(HEADER_PARAMS.findall(ct))
    params.update(dict(HEADER_PARAMS.findall(cd)))

    name = params.get("filename") or params.get("name")

    uu.encode(BytesIO(data), outfile, name=name)
    enc_data = outfile.getvalue()
    msg.set_payload(enc_data)


def set_noop_payload(msg, data):
    """Does no encoding"""
    msg.set_payload(data)


def set_unknown_payload(msg, data):
    """Does no encoding and sets a header on the MIME part with an error"""
    cte = msg.get("Content-Transfer-Encoding")
    _add_error(msg, "Unknown Content-Transfer-Encoding: %s" % cte)
    msg.set_payload(data)


def make_message(message):
    """ Make a Python  email.message.Message from our models """
    parents = {}
    part_list = message.parts.all()
    first = None

    for part in part_list:
        msg = Message()

        header_set = part.header_set.order_by("ordinal").select_related("name", "data")
        for header in header_set:
            # Deal with Python 2/3 differences
            if six.PY3:
                encoded_header = Header(header.data.data).encode()
            else:
                encoded_header = Header(header.data.data, "utf-8").encode()
            msg[header.name.name] = encoded_header

        if part.is_leaf_node():
            cte = msg.get("Content-Transfer-Encoding", "7-bit")
            data = six.binary_type(part.body.data)

            if cte == "base64":
                set_base64_payload(msg, data)
            elif cte == "quoted-printable":
                set_quopri_payload(msg, data)
            elif cte in ["uuencode", "x-uuencode", "uue", "x-uue"]:
                set_uuencode_payload(msg, data)
            elif cte in ["8-bit", "7-bit"]:
                set_noop_payload(msg, data)
            else:
                set_unknown_payload(msg, data)
        else:
            parents[part.id] = msg

        if first is None:
            first = msg
        else:
            parents[part.parent_id].attach(msg)

    return first
