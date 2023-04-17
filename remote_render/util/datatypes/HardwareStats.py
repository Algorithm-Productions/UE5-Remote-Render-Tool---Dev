"""
    Copyright Algorithm Productions LLC. 2023.
"""

from remote_render.util.datatypes.abstracts.StorableProperty import StorableProperty


class HardwareStats(StorableProperty):
    """
        Property Object Class to keep the Hardware Stats of a Machine.

        :type: StorableProperty.
        :author: vitor@bu.edu.
    """

    def __init__(
            self,
            name='',
            cpu='',
            gpu='',
            ram='',
            vram=''
    ):
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param name: Name of the Machine in question.
            :type name: String.
            :param cpu: Name of the CPU in the Machine.
            :type cpu: String.
            :param gpu: Name of the GPU in the Machine.
            :type gpu: String.
            :param ram: Amount of RAM in the Machine.
            :type ram: String.
            :param vram: Amount of VRAM in the Machine.
            :type vram: Float.
        """
        self.name = name
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.vram = vram

    @classmethod
    def from_dict(cls, data):
        """
            @inheritDoc - StorableProperty
        """
        name = (data.get('name') or '') if data else ''
        cpu = (data.get('cpu') or '') if data else ''
        gpu = (data.get('gpu') or '') if data else ''
        ram = (data.get('ram') or '') if data else ''
        vram = (data.get('vram') or '') if data else ''

        return cls(
            name=name,
            cpu=cpu,
            gpu=gpu,
            ram=ram,
            vram=vram
        )
