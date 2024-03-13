# Google Wallet C# samples

## Overview

The files in this directory each implement a demo class for a specific Google
Wallet pass type. Each class implements methods for performing tasks such as
creating a pass class, updating issuer permissions, and more.

| Pass type                  | File                                       |
|----------------------------|--------------------------------------------|
| Event tickets              | [DemoEventTicket.cs](./DemoEventTicket.cs) |
| Flight boarding passes     | [DemoFlight.cs](./DemoFlight.cs)           |
| Generic passes             | [DemoGeneric.cs](./DemoGeneric.cs)         |
| Gift cards                 | [DemoGiftCard.cs](./DemoGiftCard.cs)       |
| Loyalty program membership | [DemoLoyalty.cs](./DemoLoyalty.cs)         |
| Offers and promotions      | [DemoOffer.cs](./DemoOffer.cs)             |
| Transit passes             | [DemoTransit.cs](./DemoTransit.cs)         |

## Prerequisites

*   .NET 6.0
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

1.  Open the [`wallet-rest-samples.csproj`](./wallet-rest-samples.csproj) file
    in your .NET editor of choice.
2.  Copy the path to the Google Wallet API Client library (
    `Google.Apis.Walletobjects.v1.csproj` file) you downloaded. If needed, update
    the path in [`wallet-rest-samples.csproj`](./wallet-rest-samples.csproj) (line
    19).

    ```xml
    <CodeFiles Include="lib/Google.Apis.Walletobjects.v1.cs" />
    ```

3.  Build the project to install the dependencies.
4.  In your C# code, import a demo class and call its method(s). An example
    can be found below

    ```csharp
    // Create a demo class instance
    // Creates the authenticated HTTP client
    DemoEventTicket demo = new DemoEventTicket();

    // Create a pass class
    demo.CreateClass("issuer_id", "class_suffix");

    // Update a pass class
    demo.UpdateClass("issuer_id", "class_suffix");

    // Patch a pass class
    demo.PatchClass("issuer_id", "class_suffix");

    // Add a message to a pass class
    demo.AddClassMessage("issuer_id", "class_suffix", "header", "body");

    // Create a pass object
    demo.CreateObject("issuer_id", "class_suffix", "object_suffix");

    // Update a pass object
    demo.UpdateObject("issuer_id", "object_suffix");

    // Patch a pass object
    demo.PatchObject("issuer_id", "object_suffix");

    // Add a message to a pass object
    demo.AddObjectMessage("issuer_id", "object_suffix", "header", "body");

    // Expire a pass object
    demo.ExpireObject("issuer_id", "object_suffix");

    // Generate an Add to Google Wallet link that creates a new pass class and object
    demo.CreateJWTNewObjects("issuer_id", "class_suffix", "object_suffix");

    // Generate an Add to Google Wallet link that references existing pass object(s)
    demo.CreateJWTExistingObjects("issuer_id");

    // Create pass objects in batch
    demo.BatchCreateObjects("issuer_id", "class_suffix");
    ```
