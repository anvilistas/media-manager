# SPDX-License-Identifier: MIT
#
# Copyright (c) 2024 The Anvil Extras project team members listed at
# https://github.com/anvilistas/media-manager/graphs/contributors
#
# This software is published at https://github.com/anvilistas/media-manager
from hashlib import sha256


def hash_media(media):
    hasher = sha256()
    hasher.update(media.get_bytes())
    return hasher.hexdigest()


def boolean_from_string(value, default=False):
    options = {True: ["true", "yes", "1"], False: ["false", "no", "0"]}
    options[default].extend([None, ""])
    str_to_bool = {v: _bool for _bool, _list in options.items() for v in _list}
    if value is not None:
        value = value.lower()
    return str_to_bool.get(value, default)
