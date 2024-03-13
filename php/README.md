# Google Wallet PHP samples

## Overview

The files in this directory each implement a demo class for a specific Google
Wallet pass type. Each class implements methods for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type                  | File                                             |
|----------------------------|--------------------------------------------------|
| Event tickets              | [`demo_eventticket.php`](./demo_eventticket.php) |
| Flight boarding passes     | [`demo_flight.php`](./demo_flight.php)           |
| Generic passes             | [`demo_generic.php`](./demo_generic.php)         |
| Gift cards                 | [`demo_giftcard.php`](./demo_giftcard.php)       |
| Loyalty program membership | [`demo_loyalty.php`](./demo_loyalty.php)         |
| Offers and promotions      | [`demo_offer.php`](./demo_offer.php)             |
| Transit passes             | [`demo_transit.php`](./demo_transit.php)         |

## Prerequisites

*   PHP 7.4
*   Composer 2.x
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

1.  Install the dependencies listed in [composer.json](./composer.json)

    ```bash
    # This must be run from the same location as the composer.json
    composer install
    ```

2.  In your PHP code, import a demo class and call its method(s). An example
    can be found below

    ```php
    // Import the demo class
    require __DIR__ . '/demo_eventticket.php';

    // Your Issuer account ID (@see Prerequisites)
    $issuerId = '3388000000000000000';

    // Create a demo class instance
    $demo = new DemoEventTicket();

    // Create a pass class
    $demo->createClass($issuerId, 'class_suffix');

    // Update a pass class
    $demo->updateClass($issuerId, 'class_suffix');

    // Patch a pass class
    $demo->patchClass($issuerId, 'class_suffix');

    // Add a message to a pass class
    $demo->addClassMessage($issuerId, 'class_suffix', 'header', 'body');

    // Create a pass object
    $demo->createObject($issuerId, 'class_suffix', 'object_suffix');

    // Update a pass object
    $demo->updateObject($issuerId, 'object_suffix');

    // Patch a pass object
    $demo->patchObject($issuerId, 'object_suffix');

    // Add a message to a pass object
    $demo->addObjectMessage($issuerId, 'object_suffix', 'header', 'body');

    // Expire a pass object
    $demo->expireObject($issuerId, 'object_suffix');

    // Generate an Add to Google Wallet link that creates a new pass class and object
    $demo->createJWTNewObjects($issuerId, 'class_suffix', 'object_suffix');

    // Generate an Add to Google Wallet link that references existing pass object(s)
    $demo->createJWTExistingObjects($issuerId);

    // Create pass objects in batch
    $demo->batchCreateObjects($issuerId, 'class_suffix');
    ```
