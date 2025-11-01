 @dataclass
 class UARequest:
-    query: str
+    goal: str
     prefs: Optional[Dict[str, Any]] = None
     session_id: Optional[str] = None
     metadata: Optional[Dict[str, Any]] = None
@@
     def ready(self) -> bool:
         r = self.session.get(f"{self.base_url}/ready", timeout=self.timeout)
         r.raise_for_status()
-        return r.json().get("ready", True)
+        return r.json().get("ok", True)
