# Media Manager

Media objects can increase the size of your app's tables making the app difficult to clone.

Instead, the Media Manager can store those objects in a separate app and give you a hash value
to use for later retrieval.

Any time you would normally add a media column to a table, you instead add a text column, use it
to store the hash value of the media object and let the media manager store the object itself.

The Media Manager is an implementation of  [Content Addressable Storage](https://en.wikipedia.org/wiki/Content-addressable_storage)
to store anvil media objects.

## Installation

The Media Manager is a standalone app and is not intended to be used as a dependency.

Instead, you will need to create a blank anvil app and use git on your local machine to
fetch the code from this repository and push it to anvil.

### Create and Clone a Blank App
* In your browser, create a new, blank app from within the Anvil IDE.
* From the 'Version History' tab, click the dropdown menu and click the 'Clone with Git' button.
* Copy the clone command (the second displayed option) to you clipboard.
* In your terminal, navigate to a folder where you would like to create your local copy
* Paste the command from your clipboard into your terminal and run it.
* You should now have a new folder named with the ID of your new app. You can rename
that folder to something more meaningful if you wish.

### Configure the Remote Repositories
Your local repository is now configured with a known remote repository pointing to your copy of the app at Anvil.
That remote is currently named 'origin'. We will now rename it to something more meaningful and also add a second remote pointing to the repository on github.

* In your terminal, navigate to your new folder.
* Rename the 'origin' remote to 'anvil' with the command:

.. code-block::

    git remote rename origin anvil

* Add the github repository with the command:

.. code-block::

    git remote add github git@github.com:anvilistas/media-manager.git

### Update your local app
To update your app, we will now fetch the latest version from github to your local copy and push it from there to Anvil.

* In your terminal, fetch the lastest code from github using the commands:

.. code-block::

    git fetch github
    git reset --hard github/main

* Finally, push those changes to your copy of the app at Anvil:

.. code-block::

    git push -f anvil

## Usage

### Fetching Media

Make a `GET` request to the app's `media` endpoint passing the object's hash value in the path.

You will also need to pass a valid username and password using HTTP basic authentication.

Using anvil's `http` module:

```python
import anvil.http

url = "<media-manager-url>/_/api/media/<hash_value>"
obj = anvil.http.request(url, username="<username">, password="<password>")
```

### Storing Media

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

If you have cloned this repository to your local machine, you can also run the tests
from your terminal:

```bash
cd server_code
python -m unittest
```
