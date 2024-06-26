# SPDX-License-Identifier: MIT
#
# Copyright (c) 2024 The Anvil Extras project team members listed at
# https://github.com/anvilistas/media-manager/graphs/contributors
#
# This software is published at https://github.com/anvilistas/media-manager
import anvil.server
from anvil.tables import app_tables

from . import helpers


def _fetch_media(request, hash, **kwargs):
    row = app_tables.media.get(hash=hash, verified=True)
    return row["content"] if row else anvil.server.HttpResponse(404)


def _store_media(request, hash=None, verify=None, **kwargs):
    content = request.body
    if not content:
        return

    verify = helpers.boolean_from_string(verify, default=True)

    verified = None
    if hash is None:
        hash = helpers.hash_media(content)
        verified = True

    if hash is not None and verify:
        verified = hash == helpers.hash_media(content)
        if not verified:
            return anvil.server.HttpResponse(400, "Invalid hash for given body")

    existing_row = app_tables.media.get(hash=hash)
    if existing_row is None:
        app_tables.media.add_row(hash=hash, content=content, verified=verified)
    elif not existing_row["verified"]:
        return anvil.server.HttpResponse(
            400, "Unverified content already exists with this hash"
        )

    return hash


ACTIONS = {"GET": _fetch_media, "POST": _store_media}


@anvil.server.http_endpoint("/media/:hash", authenticate_users=True)
def handle_media_request(hash, **kwargs):
    hash = hash or None
    request = anvil.server.request
    return ACTIONS[request.method](request, hash, **kwargs)
