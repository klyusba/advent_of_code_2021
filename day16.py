

def read(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.readline()


def to_bites(hexstr: str) -> str:
    v = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }
    return ''.join(v[c] for c in hexstr)


class BitesIO:
    def __init__(self, hexstr: str):
        self._bites = to_bites(hexstr)
        self._pos = 0

    def read(self, n: int) -> int:
        v = self._bites[self._pos: self._pos + n]
        self._pos += n
        return int(v, 2)

    def tell(self):
        return self._pos


class Packet:
    def __init__(self, version, type_id, body):
        self.version = version
        self.type_id = type_id
        self.body = body

    @staticmethod
    def _read_literal_value(bites) -> int:
        not_end, v = 1, 0
        while not_end:
            not_end = bites.read(1)
            v = v * 16 + bites.read(4)
        return v

    @staticmethod
    def _read_length(bites: BitesIO, length: int):
        pos_end = bites.tell() + length
        v = []
        while bites.tell() != pos_end:
            p = Packet.from_bites(bites)
            v.append(p)
        return v

    @staticmethod
    def _read_number(bites: BitesIO, number: int):
        v = []
        for _ in range(number):
            p = Packet.from_bites(bites)
            v.append(p)
        return v

    @classmethod
    def from_bites(cls, bites: BitesIO):
        ver = bites.read(3)
        typ = bites.read(3)
        if typ == 4:
            v = cls._read_literal_value(bites)
        elif bites.read(1) == 0:
            length = bites.read(15)
            v = cls._read_length(bites, length)
        else:
            number = bites.read(11)
            v = cls._read_number(bites, number)
        return cls(ver, typ, v)

    def get_value(self):
        if self.type_id == 0:
            return sum(p.get_value() for p in self.body)
        elif self.type_id == 1:
            res = 1
            for p in self.body:
                res *= p.get_value()
            return res
        elif self.type_id == 2:
            return min(p.get_value() for p in self.body)
        elif self.type_id == 3:
            return max(p.get_value() for p in self.body)
        elif self.type_id == 4:
            return self.body
        elif self.type_id == 5:
            p1, p2 = self.body
            return 1 if p1.get_value() > p2.get_value() else 0
        elif self.type_id == 6:
            p1, p2 = self.body
            return 1 if p1.get_value() < p2.get_value() else 0
        elif self.type_id == 7:
            p1, p2 = self.body
            return 1 if p1.get_value() == p2.get_value() else 0
        else:
            raise NotImplementedError()


def main_part1(hexstr: str) -> int:
    data = BitesIO(hexstr)
    p = Packet.from_bites(data)

    sum_versions = 0
    stack = [p, ]
    while stack:
        p = stack.pop()
        sum_versions += p.version
        if p.type_id != 4:
            stack.extend(p.body)
    return sum_versions


def test_parse_literal():
    data = BitesIO("D2FE28")
    p = Packet.from_bites(data)
    assert p.version == 6
    assert p.type_id == 4
    assert p.body == 2021


def test_parse_operator0():
    data = BitesIO("38006F45291200")
    p = Packet.from_bites(data)
    assert p.version == 1
    assert p.type_id == 6
    assert len(p.body) == 2
    assert p.body[0].body == 10
    assert p.body[1].body == 20


def test_parse_operator1():
    data = BitesIO("EE00D40C823060")
    p = Packet.from_bites(data)
    assert p.version == 7
    assert p.type_id == 3
    assert len(p.body) == 3
    assert p.body[0].body == 1
    assert p.body[1].body == 2
    assert p.body[2].body == 3


def test_part1_1():
    assert main_part1("8A004A801A8002F478") == 16


def test_part1_2():
    assert main_part1("620080001611562C8802118E34") == 12


def test_part1_3():
    assert main_part1("C0015000016115A2E0802F182340") == 23


def test_part1_4():
    assert main_part1("A0016C880162017C3686B18A3D4780") == 31


def main_part2(hexstr: str) -> int:
    data = BitesIO(hexstr)
    p = Packet.from_bites(data)
    return p.get_value()


def test_part2_sum():
    assert main_part2("C200B40A82") == 3


def test_part2_prod():
    assert main_part2("04005AC33890") == 54


def test_part2_min():
    assert main_part2("880086C3E88112") == 7


def test_part2_max():
    assert main_part2("CE00C43D881120") == 9


def test_part2_lt():
    assert main_part2("D8005AC2A8F0") == 1


def test_part2_gt():
    assert main_part2("F600BC2D8F") == 0


def test_part2_eq():
    assert main_part2("9C005AC2F8F0") == 0


def test_part2_eq_sub():
    assert main_part2("9C0141080250320F1802104A08") == 1


if __name__ == "__main__":
    input_data = read('input')
    print(main_part1(input_data))
    print(main_part2(input_data))
