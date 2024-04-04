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

    verify = verify or True
    if isinstance(verify, str):
        mapping = {"true": True, "false": False}
        verify = mapping.get(verify.lower(), True)

    verified = None
    if hash is None:
        hash = helpers.hash_media(content)
        verified = True

    if hash is not None and verify:
        verified = hash == helpers.hash_media(content)
        if not verified:
            return anvil.server.HttpResponse(400, "Invalid hash for given body")

    if app_tables.media.get(hash=hash):
        return anvil.server.HttpResponse(400, "Content already exists with this hash")

    app_tables.media.add_row(hash=hash, content=content, verified=verified)
    return hash


@anvil.server.http_endpoint("/media/:hash")
def handle_media_request(hash, **kwargs):
    hash = hash or None
    request = anvil.server.request
    actions = {"GET": _fetch_media, "POST": _store_media}
    action = actions[request.method]
    return action(request, hash, **kwargs)
