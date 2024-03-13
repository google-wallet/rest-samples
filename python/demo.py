import os

from demo_eventticket import DemoEventTicket
from demo_flight import DemoFlight
from demo_generic import DemoGeneric
from demo_giftcard import DemoGiftCard
from demo_loyalty import DemoLoyalty
from demo_offer import DemoOffer
from demo_transit import DemoTransit

if __name__ == "__main__":

    # Create a demo class instance
    # Creates the authenticated HTTP client
    demo = DemoTransit() # change to demo a different pass type

    issuer_id = os.environ.get("WALLET_ISSUER_ID", "your-issuer-id")
    class_suffix = os.environ.get("WALLET_CLASS_SUFFIX", "your-class-suffix") + demo.__class__.__name__
    object_suffix = os.environ.get("WALLET_OBJECT_SUFFIX", "your-object-suffix") + demo.__class__.__name__

    # Create a pass class
    demo.create_class(issuer_id=issuer_id,
                      class_suffix=class_suffix)

    # Update a pass class
    demo.update_class(issuer_id=issuer_id,
                      class_suffix=class_suffix)

    # Patch a pass class
    demo.patch_class(issuer_id=issuer_id,
                     class_suffix=class_suffix)

    # Create a pass object
    demo.create_object(issuer_id=issuer_id,
                       class_suffix=class_suffix,
                       object_suffix=object_suffix)

    # Update a pass object
    demo.update_object(issuer_id=issuer_id,
                       object_suffix=object_suffix)

    # Patch a pass object
    demo.patch_object(issuer_id=issuer_id,
                      object_suffix=object_suffix)

    # Expire a pass object
    demo.expire_object(issuer_id=issuer_id,
                       object_suffix=object_suffix)

    # Create an "Add to Google Wallet" link
    # that generates a new pass class and object
    demo.create_jwt_new_objects(issuer_id=issuer_id,
                                class_suffix=class_suffix,
                                object_suffix=object_suffix)

    # Create an "Add to Google Wallet" link
    # that references existing pass classes and objects
    demo.create_jwt_existing_objects(issuer_id=issuer_id)

    # Create pass objects in batch
    demo.batch_create_objects(issuer_id=issuer_id,
                              class_suffix=class_suffix)
