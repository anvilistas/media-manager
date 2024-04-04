# Media Manager

The media manager uses [Content Addressable Storage](https://en.wikipedia.org/wiki/Content-addressable_storage)
to store anvil media objects.

Each object in the store is indexed by its hash value and can be retrieved using that value as an id.

The hash can either be computed prior to storing or the app itself will calculate the hash. If the hash
is passed in from elsewhere, it must be verified before the object becomes available. The
verification can be carried out immediately or will eventually be done by a background task.

If that verification fails, the object is removed from the store.

## Fetching Media

Make a `GET` request to the app's `media` endpoint passing the object's id in the path.

Using anvil's `http` module:

```python
import anvil.http

obj = anvil.http.request("<media-manager-url>/_/api/media/<object_id>")
```

## Storing Media

Make a 'POST' request to the app's `media` endpoint, passing the object in the request body.

Using anvil's `http` module:

```python
import anvil.http

anvil.http.request(
    url="<media-manager-url>/_/api/media",
    method="POST",
    data=obj,
)
```

If you already have the hash for the media object, you can pass that to the endpoint:

```python
import anvil.http

anvil.http.request(
    url="<media-manager-url>/_/api/media/<hash value>",
    method="POST",
    data=obj,
)
```
by default, the hash will be verified before the call completes. If you wish to defer
the verification, you can use a query string parameter in the url:

```python
import anvil.http

anvil.http.request(
    url="<media-manager-url>/_/api/media/<hash value>?verify=false",
    method="POST",
    data=obj,
)
```
