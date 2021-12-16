from dataclasses import dataclass
from typing import List
from functools import reduce

puzzle_input = "A20D790042F1274011955491808B802F1C60B20030327AF2CC248AA800E7CDD726F3D78F4966F571A300BA54D668E2519249265160803EA9DE562A1801204ACE53C954ACE53C94C659BDF318FD1366EF44D96EB11005FB39154E0068A7C3A6B379646C80348A0055E6642B332109B8D6F0F12980452C9D322B28012EC72D51B300426CF70017996DE6C2B2C70C01A04B67B9F9EC8DAFE679D0992A80380104065FA8012805BD380120051E380146006380142004A00E920034C0801CA007B0099420053007144016E28018800CCC8CBB5FE79A3D91E1DC9FB151A1006CC0188970D6109803B1D61344320042615C198C2A014C589D00943096B3CCC081009173D015B004C401C8E10421E8002110BA18C193004A52257E0094BCE1ABB94C2C9005112DFAA5E80292B405927020106BC01494DFA6E329BF4DD273B69E233DB04C435BEF7A0CC00CFCDF31DC6AD20A3002A498CC01D00042229479890200E4438A91700010F88F0EA251802D33FE976802538EF38E2401B84CA05004833529CD2A5BD9DDAC566009CC33E8024200CC528E71F40010A8DF0C61D8002B5076719A5D418034891895CFD320730F739A119CB2EA0072D25E870EA465E189FDC1126AF4B91100A03600A0803713E2FC7D00043A25C3B8A12F89D2E6440242489A7802400086C788FB09C0010C8BB132309005A1400D2CBE7E7F2F9F9F4BB83803B25286DFE628E129EBCB7483C8802F3D0A2542E3004AC0169BD944AFF263361F1B48010496089807100BA54A66675769B1787D230C621EF8B9007893F058A009AE4ED7A5BBDBE05262CEC0002FC7C20082622E0020D0D66A2D04021D5003ED3D396E19A1149054FCA3586BD00020129B0037300042E0CC1184C000874368F70A251D840239798AC8DC9A56F7C6C0E0728015294D9290030B226938A928D0"

def hex_to_binary(input):
    scale = 16
    res = bin(int(input, scale)).zfill(8)
    return res[2:]

def binary_to_int(input):
    return int(input, 2)

def is_operator_packet(type_id):
    return type_id != 4


@dataclass
class Packet:
    version: int
    type_id: int

    def sum_of_versions(self):
        raise NotImplementedError

    def evaluate(self):
        raise NotImplementedError


@dataclass
class LiteralPacket(Packet):
    value: int

    def sum_of_versions(self):
        return self.version

    def evaluate(self):
        return self.value


@dataclass
class OperatorPacket(Packet):
    version: int
    type_id: int
    sub_packets: List[Packet]

    def sum_of_versions(self):
        return self.version + sum(map(lambda x: x.sum_of_versions(), self.sub_packets))

    def evaluate(self):
        if self.type_id == 0: #sum
            return sum(map(lambda x: x.evaluate(), self.sub_packets))
        elif self.type_id == 1: #product
            return reduce(lambda a, b: a*b, map(lambda x: x.evaluate(), self.sub_packets))
        elif self.type_id == 2: #minimum
            return min(map(lambda x: x.evaluate(), self.sub_packets))
        elif self.type_id == 3: #maximum
            return max(map(lambda x: x.evaluate(), self.sub_packets))
        elif self.type_id == 5: #greater than
            if self.sub_packets[0].evaluate() > self.sub_packets[1].evaluate():
                return 1
            else:
                return 0
        elif self.type_id == 6: #less than
            if self.sub_packets[0].evaluate() < self.sub_packets[1].evaluate():
                return 1
            else:
                return 0
        elif self.type_id == 7: #equal to
            if self.sub_packets[0].evaluate() == self.sub_packets[1].evaluate():
                return 1
            else:
                return 0

def parse_literal_packet(input, version, type_id, start_pos):
    marker_bit = "1"
    value = ""

    while marker_bit != "0":
        marker_bit = input[start_pos]
        value += input[start_pos+1: start_pos+5]
        start_pos += 5

    int_value = binary_to_int(value)

    return LiteralPacket(version, type_id, int_value), start_pos


def parse_operator_packet(bin_input, version, type_id, start_pos):
    packets = []

    length_type_id = bin_input[start_pos]
    # print(f"length_type_id: {length_type_id}")

    if length_type_id == "0":
        length = binary_to_int(bin_input[start_pos + 1: start_pos + 16])
        start_pos += 16

        # print(f"length: {length}")

        end_pos = start_pos + length
        while start_pos < end_pos:
            packet, start_pos = parse(bin_input, start_pos)
            packets.append(packet)

    else:
        num_packets = binary_to_int(bin_input[start_pos + 1: start_pos + 12])
        start_pos += 12

        for i in range(num_packets):
            packet, start_pos = parse(bin_input, start_pos)
            packets.append(packet)

    return OperatorPacket(version, type_id, packets), start_pos


def parse(bin_input, start_pos = 0):
    # while start_pos < len(binary_input):
    version = binary_to_int(bin_input[start_pos:start_pos + 3])
    type_id = binary_to_int(bin_input[start_pos + 3:start_pos + 6])
    if is_operator_packet(type_id):
        operator_packet, start_pos = parse_operator_packet(bin_input, version, type_id, start_pos + 6)
        return operator_packet, start_pos
    else:
        packet, start_pos = parse_literal_packet(bin_input, version, type_id, start_pos + 6)
        return packet, start_pos


if __name__ == "__main__":
    binary_input = hex_to_binary(puzzle_input)
    # binary_input = "00111000000000000110111101000101001010010001001000000000"
    packet, start_pos = parse(binary_input)
    print(packet.sum_of_versions())
    print(packet.evaluate())
    # print(packet)
