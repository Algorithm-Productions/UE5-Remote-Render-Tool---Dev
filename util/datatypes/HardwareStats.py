class HardwareStats(object):
    def __init__(
            self,
            name='',
            cpu='',
            gpu='',
            ram='',
            vram=''
    ):
        self.name = name
        self.cpu = cpu
        self.gpu = gpu
        self.ram = ram
        self.vram = vram

    @classmethod
    def from_dict(cls, data):
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

    def to_dict(self):
        return self.__dict__
