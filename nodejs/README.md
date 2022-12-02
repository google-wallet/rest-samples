# Google Wallet Node.js samples

## Overview

The files in this directory each implement a demo class for a specific Google
Wallet pass type. Each class implements methods for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type                  | File                                         |
|----------------------------|----------------------------------------------|
| Event tickets              | [demo-eventticket.js](./demo-eventticket.js) |
| Flight boarding passes     | [demo-flight.js](./demo-flight.js)           |
| Generic passes             | [demo-generic.js](./demo-generic.js)         |
| Gift cards                 | [demo-giftcard.js](./demo-giftcard.js)       |
| Loyalty program membership | [demo-loyalty.js](./demo-loyalty.js)         |
| Offers and promotions      | [demo-offer.js](./demo-offer.js)             |
| Transit passes             | [demo-transit.js](./demo-transit.js)         |

## Prerequisites

*   Node.js 18.x
*   NPM 8.x
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

1.  Use `npm` to install the dependencies in the [package.json](./package.json)

    ```bash
    # This must be run from the same location as the package.json
    npm install
    ```

2.  In your Node.js code, import a demo class and call its method(s). An example
    can be found below

    ```javascript
    // Import the demo class
    const { DemoEventTicket } = require('./demo-eventticket');

    // Create a demo class instance
    // Creates the authenticated HTTP client
    let demo = new DemoEventTicket();

    // Create a pass class
    demo.createClass('issuer_id', 'class_suffix');

    // Update a pass class
    demo.updateClass('issuer_id', 'class_suffix');

    // Patch a pass class
    demo.patchClass('issuer_id', 'class_suffix');

    // Add a message to a pass class
    demo.addClassMessage('issuer_id', 'class_suffix', 'header', 'body');

    // Create a pass object
    demo.createObject('issuer_id', 'class_suffix', 'object_suffix');

    // Update a pass object
    demo.updateObject('issuer_id', 'object_suffix');

    // Patch a pass object
    demo.patchObject('issuer_id', 'object_suffix');

    // Add a message to a pass object
    demo.addObjectMessage('issuer_id', 'object_suffix', 'header', 'body');

    // Expire a pass object
    demo.expireObject('issuer_id', 'object_suffix');

    // Generate an Add to Google Wallet link that creates a new pass class and object
    demo.createJWTNewObjects('issuer_id', 'class_suffix', 'object_suffix');

    // Generate an Add to Google Wallet link that references existing pass object(s)
    demo.createJWTExistingObjects('issuer_id');

    // Create pass objects in batch
    demo.batchCreateObjects('issuer_id', 'class_suffix');
    ```
