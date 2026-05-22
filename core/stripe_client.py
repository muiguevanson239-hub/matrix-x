import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class StripeClient:

    def create_checkout(self, user_id, plan, price_id):

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            metadata={
                "user_id": user_id,
                "plan": plan
            },
            success_url="http://127.0.0.1:8000/ui",
            cancel_url="http://127.0.0.1:8000/ui"
        )

        return session.url