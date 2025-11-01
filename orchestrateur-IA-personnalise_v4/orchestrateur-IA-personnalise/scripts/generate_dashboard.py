import pathlib, json, datetime
from src.memory.profile_store import ProfileStore

def main():
    prof = ProfileStore()
    metrics = prof.profile.get("last_metrics", {})
    score = metrics.get("last_meta_score", 0)
    cites = "oui" if metrics.get("citations") else "non"
    notes = metrics.get("notes", ["(aucune note)"])
    out = """# Tableau de bord cognitif

_Généré le: {ts}_

## Dernières métriques
- Score meta global: **{score}**
- Citations présentes: **{cites}**

## Notes d'amélioration
{notes}
""".format(
        ts=datetime.datetime.utcnow().isoformat(),
        score=score,
        cites=cites,
        notes="\n".join(f"- {n}" for n in notes)
    )
    pathlib.Path("docs/dashboard.md").write_text(out, encoding="utf-8")
    print("Dashboard écrit dans docs/dashboard.md")

if __name__ == "__main__":
    main()
