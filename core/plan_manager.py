class PlanManager:

    def __init__(self):

        # simple plan rules (Matrix X SaaS tiers)
        self.plans = {
            "FREE": {
                "memory_limit": 20,
                "streaming": False,
                "priority": 0
            },
            "STARTER": {
                "memory_limit": 50,
                "streaming": False,
                "priority": 1
            },
            "PRO": {
                "memory_limit": 200,
                "streaming": True,
                "priority": 2
            },
            "ELITE": {
                "memory_limit": 500,
                "streaming": True,
                "priority": 3
            },
            "BUSINESS": {
                "memory_limit": 2000,
                "streaming": True,
                "priority": 4
            },
            "ENTERPRISE": {
                "memory_limit": 10000,
                "streaming": True,
                "priority": 5
            },
            "LEGEND": {
                "memory_limit": -1,
                "streaming": True,
                "priority": 999
            }
        }

    # ---------------------------------
    # GET PLAN DATA
    # ---------------------------------
    def get(self, plan_name):

        return self.plans.get(plan_name.upper(), self.plans["FREE"])

    # ---------------------------------
    # MEMORY LIMIT CHECK
    # ---------------------------------
    def memory_limit(self, plan_name):

        plan = self.get(plan_name)

        return plan["memory_limit"]

    # ---------------------------------
    # CHECK UPGRADE RULE
    # ---------------------------------
    def can_upgrade(self, current, new_plan):

        current_plan = self.get(current)
        new_plan = self.get(new_plan)

        return new_plan["priority"] > current_plan["priority"]