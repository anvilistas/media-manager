from hashlib import sha256


def hash_media(media):
    hasher = sha256()
    hasher.update(media.get_bytes())
    return hasher.hexdigest()
