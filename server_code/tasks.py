# SPDX-License-Identifier: MIT
#
# Copyright (c) 2024 The Anvil Extras project team members listed at
# https://github.com/anvilistas/media-manager/graphs/contributors
#
# This software is published at https://github.com/anvilistas/media-manager
import datetime as dt

import anvil.server
import anvil.tables
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
    actions = {"verify": [], "remove": []}
    for row in rows[:BATCH_SIZE]:
        if not row["content"]:
            actions["remove"].append(row)
            continue

        hash = helpers.hash_media(row["content"])
        if hash == row["hash"]:
            actions["verify"].append(row)
        else:
            actions["remove"].append(row)

    with anvil.tables.batch_update:
        for row in actions["verify"]:
            row.update(verified=True)

    with anvil.tables.batch_delete:
        for row in actions["remove"]:
            row.delete()

    result["verified"] += len(actions["verify"])
    result["removed"] += len(actions["remove"])

    print(result)
    task_row.delete()
