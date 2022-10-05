# Google Wallet PHP samples

## Overview

The files in this directory each implement a demo class for a specific Google
Wallet pass type. Each class implements methods for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type | File |
|-----------|------|
| Event tickets | [demo_eventticket.php](./demo_eventticket.php) |
| Flight boarding passes | [demo_flight.php](./demo_flight.php) |
| Generic passes | [demo_generic.php](./demo_generic.php) |
| Gift cards | [demo_giftcard.php](./demo_giftcard.php) |
| Loyalty program membership | [demo_loyalty.php](./demo_loyalty.php) |
| Offers and promotions | [demo_offer.php](./demo_offer.php) |
| Transit passes | [demo_transit.php](./demo_transit.php) |

## Prerequisites

* PHP 8.x
* Composer 2.x
* Follow the steps outlined in the
[Google Wallet prerequisites](https://developers.google.com/wallet/generic/web/prerequisites)
to create the Google Wallet issuer account and Google Cloud service account
* Download the PHP
[Google Wallet API Client library](https://developers.google.com/wallet/generic/resources/libraries#php)

## Environment variables

The following environment variables must be set. Alternatively, you can update
the code files to set the values directly. They can be found in the constructor
for each class file.

| Enviroment variable | Description | Example |
|---------------------|-------------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a Google Cloud service account key file | `/path/to/key.json` |

## How to use the code samples

1. Install the dependencies listed in [composer.json](./composer.json)

    ```bash
    # This must be run from the same location as the composer.json
    composer install
    ```

2. Copy the path to the Google Wallet API Client library (`Walletobjects.php`
file) you downloaded. If needed, update the path in the demo class PHP file
(line 22).

    ```php
    // Download the PHP client library from the following URL
    // https://developers.google.com/wallet/generic/resources/libraries
    require __DIR__ . '/lib/Walletobjects.php';
    ```

3. In your PHP code, import a demo class and call its method(s). An example
can be found below

    ```php
    // Import the demo class
    require __DIR__ . 'demo_eventticket.php';

    // Create a demo class instance
    $demo = new DemoEventTicket();

    // Create the authenticated HTTP client
    $demo->auth();

    // Create a pass class
    $demo->createEventTicketClass('issuer_id', 'class_suffix');

    // Create a pass object
    $demo->createEventTicketObject('issuer_id', 'class_suffix', 'user_id');

    // Create an Add to Google Wallet link
    $demo->createJwtSaveUrl('issuer_id', 'class_suffix', 'user_id');

    // Create an issuer account
    $demo->createIssuerAccount('issuer_name', 'issuer_email');

    // Create pass objects in batch
    $demo->batchCreateEventTicketObjects('issuer_id', 'class_suffix');
    ```
