from core.matrix_engine import MatrixXEngine
from config.plans import PLANS


# =========================================================
# SINGLETON HOLDER
# =========================================================

_engine_instance = None


# =========================================================
# GET ENGINE INSTANCE
# =========================================================

def get_engine():
    global _engine_instance

    if _engine_instance is None:

        _engine_instance = MatrixXEngine(
            config={
                "plans": PLANS
            }
        )

    return _engine_instance


# =========================================================
# COMPATIBILITY LAYER (OLD IMPORT SUPPORT)
# =========================================================

engine = get_engine()