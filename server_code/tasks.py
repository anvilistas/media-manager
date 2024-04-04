import datetime as dt

import anvil.server
import anvil.tables.query as q
from anvil.tables import app_tables

from . import helpers

BATCH_SIZE = 100


@anvil.server.background_task
def verify_media():
    task_type = "verify_media"
    if app_tables.tasks.get(task_type=task_type):
        print(f"{task_type} task already running")
        return

    task_id = anvil.server.context.background_task_id
    task_row = app_tables.tasks.add_row(
        task_type=task_type, task_id=task_id, started_at=dt.datetime.now()
    )
    rows = app_tables.media.search(verified=q.not_(True))
    if len(rows) == 0:
        print("No media to verify")
        task_row.delete()
        return

    task_row.update(status={"total": len(rows)})
    result = {
        "todo": len(rows),
        "verified": 0,
        "removed": 0,
    }
    for row in rows[:BATCH_SIZE]:
        if not row["content"]:
            row.delete()
            result["removed"] += 1
            continue

        hash = helpers.hash_media(row["content"])
        if hash == row["hash"]:
            row["verified"] = True
            result["verified"] += 1
        else:
            row.delete()
            result["removed"] += 1

    print(result)
    task_row.delete()
