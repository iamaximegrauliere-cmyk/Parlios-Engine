-import os
-from fastapi import Header, HTTPException
-
-def require_api_key(x_api_key: str | None = Header(default=None)):
-    expected = os.getenv("PARLIOS_API_KEY")
-    if not expected:
-        return  # pas d'auth si la variable n'est pas définie
-    if x_api_key != expected:
-        raise HTTPException(status_code=401, detail="invalid api key")
+import os
+from fastapi import Header, HTTPException, status
+
+def require_api_key(
+    authorization: str | None = Header(default=None),
+    x_api_key: str | None = Header(default=None),
+):
+    expected = os.getenv("PARLIOS_API_KEY")
+    if not expected:
+        return  # Auth off en l'absence de variable -> dev UX
+    token = None
+    if authorization and authorization.startswith("Bearer "):
+        token = authorization.split(" ", 1)[1]
+    elif x_api_key:
+        token = x_api_key
+    if token != expected:
+        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid api key")
