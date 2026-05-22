import time
import traceback
import threading


class Executor:

    def __init__(self):

        self.tools = {}

        # =========================
        # EXECUTION LOGS
        # =========================
        self.logs = []

        # =========================
        # TOOL TIME LIMIT (SEC)
        # =========================
        self.timeout = 10

    # =========================================================
    # REGISTER TOOL
    # =========================================================

    def register_tool(self, name, func):

        self.tools[name] = func

    # =========================================================
    # INTERNAL EXECUTION WRAPPER
    # =========================================================

    def _execute(self, name, args, kwargs, result_container):

        try:

            result = self.tools[name](*args, **kwargs)

            result_container["result"] = result
            result_container["success"] = True

        except Exception as e:

            result_container["success"] = False
            result_container["error"] = str(e)
            result_container["trace"] = traceback.format_exc()

    # =========================================================
    # RUN TOOL (SAFE EXECUTION)
    # =========================================================

    def run(self, name, *args, **kwargs):

        if name not in self.tools:

            return {
                "success": False,
                "error": f"Tool '{name}' not found"
            }

        result_container = {
            "success": False,
            "result": None,
            "error": None
        }

        thread = threading.Thread(
            target=self._execute,
            args=(name, args, kwargs, result_container)
        )

        start_time = time.time()

        thread.start()
        thread.join(timeout=self.timeout)

        # TIMEOUT HANDLING
        if thread.is_alive():

            return {
                "success": False,
                "tool": name,
                "error": "Tool execution timeout"
            }

        end_time = time.time()

        log_entry = {
            "tool": name,
            "args": str(args),
            "kwargs": str(kwargs),
            "success": result_container["success"],
            "timestamp": start_time,
            "duration": end_time - start_time
        }

        self.logs.append(log_entry)

        return {
            "success": result_container["success"],
            "tool": name,
            "result": result_container["result"],
            "error": result_container["error"]
        }

    # =========================================================
    # LIST TOOLS
    # =========================================================

    def list_tools(self):

        return list(self.tools.keys())

    # =========================================================
    # TOOL METADATA
    # =========================================================

    def tool_info(self):

        return {
            name: {
                "function": str(func)
            }
            for name, func in self.tools.items()
        }

    # =========================================================
    # LOGS
    # =========================================================

    def get_logs(self, limit=50):

        return self.logs[-limit:]