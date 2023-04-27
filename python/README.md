# Google Wallet Python samples

## Overview

The files in this directory each implement a demo class for a specific Google
Wallet pass type. Each class implements methods for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type                  | File                                           |
|----------------------------|------------------------------------------------|
| Event tickets              | [`demo_eventticket.py`](./demo_eventticket.py) |
| Flight boarding passes     | [`demo_flight.py`](./demo_flight.py)           |
| Generic passes             | [`demo_generic.py`](./demo_generic.py)         |
| Gift cards                 | [`demo_giftcard.py`](./demo_giftcard.py)       |
| Loyalty program membership | [`demo_loyalty.py`](./demo_loyalty.py)         |
| Offers and promotions      | [`demo_offer.py`](./demo_offer.py)             |
| Transit passes             | [`demo_transit.py`](./demo_transit.py)         |

## Prerequisites

*   Python 3.x
*   The [`pipenv` library](https://pipenv.pypa.io/en/latest/installation/)
*   Follow the steps outlined in the
    [Google Wallet prerequisites](https://developers.google.com/wallet/generic/web/prerequisites)
    to create the Google Wallet issuer account and Google Cloud service account

## Environment variables

The following environment variables must be set. Alternatively, you can update
the code files to set the values directly. They can be found in the constructor
for each class file.

| Enviroment variable              | Description                                     | Example             |
|----------------------------------|-------------------------------------------------|---------------------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a Google Cloud service account key file | `/path/to/key.json` |

## How to use the code samples

1.  Create a [virtual environment](https://docs.python.org/3/library/venv.html)
    in your workspace

    ```bash
    # This creates a .venv directory in the current working path
    python3 -m venv .venv
    ```

2.  Activate the virtual environment

    ```bash
    # This must be run in the same location as the .venv directory
    source .venv/bin/activate
    ```

3.  Use `pipenv` to install the dependencies in the [Pipfile](./Pipfile)

    ```bash
    # This must be run from the same location as the Pipfile
    pipenv install
    ```

4.  In your Python code, import a demo class and call its method(s). An example
    can be found below

    ```python
    # Import the demo class
    from .demo_eventticket import DemoEventTicket

    # Create a demo class instance
    # Creates the authenticated HTTP client
    demo = DemoEventTicket()

    # Create a pass class
    demo.create_class(issuer_id='issuer_id',
                      class_suffix='class_suffix')

    # Update a pass class
    demo.update_class(issuer_id='issuer_id',
                      class_suffix='class_suffix')

    # Patch a pass class
    demo.patch_class(issuer_id='issuer_id',
                     class_suffix='class_suffix')

    # Add a message to a pass class
    demo.add_class_message(issuer_id='issuer_id',
                           class_suffix='class_suffix',
                           header='header',
                           body='body')

    # Create a pass object
    demo.create_object(issuer_id='issuer_id',
                       class_suffix='class_suffix',
                       object_suffix='object_suffix')

    # Update a pass object
    demo.update_object(issuer_id='issuer_id',
                       object_suffix='object_suffix')

    # Patch a pass object
    demo.patch_object(issuer_id='issuer_id',
                      object_suffix='object_suffix')

    # Add a message to a pass object
    demo.add_object_message(issuer_id='issuer_id',
                            object_suffix='object_suffix',
                            header='header',
                            body='body')

    # Expire a pass object
    demo.expire_object(issuer_id='issuer_id',
                       object_suffix='object_suffix')

    # Create an "Add to Google Wallet" link
    # that generates a new pass class and object
    demo.create_jwt_new_objects(issuer_id='issuer_id',
                                class_suffix='class_suffix',
                                object_suffix='object_suffix')

    # Create an "Add to Google Wallet" link
    # that references existing pass classes and objects
    demo.create_jwt_existing_objects(issuer_id='issuer_id')

    # Create pass objects in batch
    demo.batch_create_objects(issuer_id='issuer_id',
                              class_suffix='class_suffix')
    ```
