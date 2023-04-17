"""
    Copyright Algorithm Productions LLC. 2023.
"""

from ..abstracts.EnumProperty import EnumProperty


class RenderStatus(EnumProperty):
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

    @classmethod
    def contains(cls, item):
        return item in [cls.unassigned, cls.ready_to_start, cls.in_progress, cls.finished, cls.errored,
                        cls.cancelled, cls.paused]
