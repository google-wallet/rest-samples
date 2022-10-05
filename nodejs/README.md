# Google Wallet Node.js samples

## Overview

The files in this directory each implement a demo class for a specific Google
Wallet pass type. Each class implements methods for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type | File |
|-----------|------|
| Event tickets | [demo-eventticket.js](./demo-eventticket.js) |
| Flight boarding passes | [demo-flight.js](./demo-flight.js) |
| Generic passes | [demo-generic.js](./demo-generic.js) |
| Gift cards | [demo-giftcard.js](./demo-giftcard.js) |
| Loyalty program membership | [demo-loyalty.js](./demo-loyalty.js) |
| Offers and promotions | [demo-offer.js](./demo-offer.js) |
| Transit passes | [demo-transit.js](./demo-transit.js) |

## Prerequisites

* Node.js 18.x
* NPM 8.x
* Follow the steps outlined in the
[Google Wallet prerequisites](https://developers.google.com/wallet/generic/web/prerequisites)
to create the Google Wallet issuer account and Google Cloud service account

## Environment variables

The following environment variables must be set. Alternatively, you can update
the code files to set the values directly. They can be found in the constructor
for each class file.

| Enviroment variable | Description | Example |
|---------------------|-------------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to a Google Cloud service account key file | `/path/to/key.json` |

## How to use the code samples

1. Use `npm` to install the dependencies in the [package.json](./package.json)

    ```bash
    # This must be run from the same location as the package.json
    npm install
    ```

2. In your Node.js code, import a demo class and call its method(s). An example
can be found below

    ```javascript
    // Import the demo class
    const { DemoEventTicket } = require('./demo-eventticket');

    // Create a demo class instance
    let demo = new DemoEventTicket();

    // Create the authenticated HTTP client
    demo.auth();

    // Create a pass class
    demo.createEventTicketClass('issuer_id', 'class_suffix');

    // Create a pass object
    demo.createEventTicketObject('issuer_id', 'class_suffix', 'user_id');

    // Create an Add to Google Wallet link
    demo.createJwtSaveUrl('issuer_id', 'class_suffix', 'user_id');

    // Create an issuer account
    demo.createIssuerAccount('issuer_name', 'issuer_email');

    // Create pass objects in batch
    demo.batchCreateEventTicketObjects('issuer_id', 'class_suffix');
    ```
