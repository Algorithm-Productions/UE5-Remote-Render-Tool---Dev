"""
    Copyright Algorithm Productions LLC. 2023.
"""

from enum import Enum


class RenderStatus(Enum):
    """
        Enum Class to Represent all Statuses of a Render Job.

        :type: Enum.
        :author: vitor@bu.edu.
    """
    unassigned = 'Un-Assigned'
    ready_to_start = 'Ready to Start'
    in_progress = 'In Progress'
    finished = 'Finished'
    errored = 'Errored'
    cancelled = 'Cancelled'
    paused = 'Paused'
