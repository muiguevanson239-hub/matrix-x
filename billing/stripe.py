import stripe
import os


class StripeBilling:

    def __init__(self):

        # =====================================================
        # LOAD FROM ENV (SECURE)
        # =====================================================

        self.secret_key = os.getenv("STRIPE_SECRET_KEY", "")

        if not self.secret_key:
            raise Exception("Missing STRIPE_SECRET_KEY")

        stripe.api_key = self.secret_key

        # FRONTEND URL (CHANGE IN PROD)
        self.success_url = os.getenv(
            "SUCCESS_URL",
            "http://localhost:8000/ui"
        )

        self.cancel_url = os.getenv(
            "CANCEL_URL",
            "http://localhost:8000/ui"
        )

    # =========================================================
    # CREATE CHECKOUT SESSION
    # =========================================================

    def create_checkout(self, user_id, plan, price_id):

        try:

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

                success_url=self.success_url,
                cancel_url=self.cancel_url
            )

            return session.url

        except stripe.error.StripeError as e:

            return {
                "error": f"Stripe error: {str(e)}"
            }

        except Exception as e:

            return {
                "error": f"Server error: {str(e)}"
            }