import hashlib
import secrets
import time


# =========================================================
# ACTIVE SESSIONS
# =========================================================

SESSIONS = {}

# SESSION LIFETIME (24 HOURS)
SESSION_DURATION = 60 * 60 * 24


# =========================================================
# PASSWORD HASH
# =========================================================

def hash_pw(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# AUTH SYSTEM
# =========================================================

class AuthSystem:

    # =====================================================
    # REGISTER
    # =====================================================

    def register(self, db, user_id, password):

        # CHECK USER EXISTS
        if db.get_user(user_id):

            return {
                "error": "User already exists"
            }

        # VALIDATION
        if len(user_id.strip()) < 3:

            return {
                "error": "Username too short"
            }

        if len(password.strip()) < 4:

            return {
                "error": "Password too short"
            }

        # CREATE USER
        db.create_user(
            user_id=user_id,
            password=password
        )

        return {
            "status": "registered"
        }

    # =====================================================
    # LOGIN
    # =====================================================

    def login(self, db, user_id, password):

        user = db.get_user(user_id)

        if not user:

            return {
                "error": "User not found"
            }

        # VERIFY PASSWORD
        if user["password"] != hash_pw(password):

            return {
                "error": "Invalid password"
            }

        # CREATE TOKEN
        token = secrets.token_hex(32)

        SESSIONS[token] = {
            "user_id": user_id,
            "created_at": time.time(),
            "expires_at": time.time() + SESSION_DURATION,
            "role": "user"
        }

        return {
            "token": token,
            "expires_in": SESSION_DURATION
        }

    # =====================================================
    # AUTHENTICATE
    # =====================================================

    def authenticate(self, token):

        if token not in SESSIONS:
            return None

        session = SESSIONS[token]

        # SESSION EXPIRED
        if time.time() > session["expires_at"]:

            del SESSIONS[token]

            return None

        return session["user_id"]

    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self, token):

        if token in SESSIONS:

            del SESSIONS[token]

            return {
                "status": "logged_out"
            }

        return {
            "error": "Invalid token"
        }

    # =====================================================
    # GET SESSION INFO
    # =====================================================

    def session_info(self, token):

        session = SESSIONS.get(token)

        if not session:
            return None

        return {
            "user_id": session["user_id"],
            "created_at": session["created_at"],
            "expires_at": session["expires_at"],
            "role": session["role"]
        }