# Media Manager

Media objects can increase the size of your app's tables making the app difficult to clone.

Instead, the Media Manager can store those objects in a separate app and give you a hash value
to use for later retrieval.

Any time you would normally add a media column to a table, you instead add a text column, use it
to store the hash value of the media object and let the media manager store the object itself.

The Media Manager is an implementation of  [Content Addressable Storage](https://en.wikipedia.org/wiki/Content-addressable_storage)
to store anvil media objects.

## Fetching Media

Make a `GET` request to the app's `media` endpoint passing the object's hash value in the path.

You will also need to pass a valid username and password using HTTP basic authentication.

Using anvil's `http` module:

```python
import anvil.http

url = "<media-manager-url>/_/api/media/<hash_value>"
obj = anvil.http.request(url, username="<username">, password="<password>")
```

## Storing Media

Make a 'POST' request to the app's `media` endpoint, passing the object in the request body.

The response will return the hash value of the object which you could store in your app's
data tables.

Again, you will need to provide a valid username and password.

Using anvil's `http` module:

```python
import anvil.http

url="<media-manager-url>/_/api/media",
hash_value = anvil.http.request(
    url,
    method="POST",
    data=obj,
    username="<username>",
    password="<password>",
)
```

If you already have the hash for the media object, you can pass that to the endpoint:

```python
from hashlib import sha256
import anvil.http

hasher = sha256()
hasher.update(obj.get_bytes())
hash_value = hasher.hexdigest()

url=f"<media-manager-url>/_/api/media/{hash_value}",
anvil.http.request(
    url,
    method="POST",
    data=obj,
    username="<username>",
    password="<password>",
)
```
by default, the hash will be verified before the call completes. However, that can take
some time if the media object is large. You can choose to defer
the verification by using a query string parameter in the url:

```python
import anvil.http

url="<media-manager-url>/_/api/media/<hash value>?verify=false",
anvil.http.request(
    url,
    method="POST",
    data=obj,
    username="<username>",
    password="<password>",
)
```
In this case, a background task will carry out the verification at some point later. The
media object will be unavailable until that verification succeeds. If it fails, the object
is removed from the store.

## Development

### Running the Tests

from the app's server console:

```py
from . import tests; tests.run()
```

You can increase the verbosity of the test output:
```py
from . import tests; test.run(verbosity=2)
```
