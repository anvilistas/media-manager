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


def boolean_from_string(value, default):
    options = {True: ("true", "yes", "1"), False: ("false", "no", "0")}
    return value in options[default]
