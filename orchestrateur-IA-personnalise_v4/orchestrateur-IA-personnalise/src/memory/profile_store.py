class ProfileStore:
    def __init__(self):
        self.profile = {
            "style": {"ton": "coach direct", "registre": "familier", "format": "listes courtes"},
            "tolerance_ambiguite": "faible",
            "preferences": {"citations": "toujours", "exemples": "souhaités"}
        }
        self._overrides = {}

    def update_overrides(self, d):
        self._overrides.update(d)

    def current_style(self):
        style = self.profile.get("style", {}).copy()
        style.update(self._overrides.get("style", {}))
        return style

    def ingest_event(self, event: str, payload: dict):
        # TODO: implement real scoring & adaptation
        return {"event": event, "status": "recorded"}


    def record_metrics(self, metrics: dict):
        # In real app write to DB; here we keep last metrics in memory for demo.
        self.profile.setdefault("last_metrics", {}).update(metrics)
        return self.profile["last_metrics"]
