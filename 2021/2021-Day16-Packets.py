from dataclasses import dataclass
import math

@dataclass
class Packet:
    type: int
    version: int
    start: int
    length: int = 0
    subpackets: list['Packet'] = None
    value: int = None


class PacketReader:
    def __init__(self, data):
        self.data = data
        self.bitit = self.bits()
        self.bitidx = 0

    def bits(self):
        for c in self.data:
            byte = int(c, base=16)
            for i in reversed(range(4)):
                yield 1 if byte & 1<<i else 0
                self.bitidx += 1

    def get_num(self, nbits):
        result = 0
        while nbits > 0:
            result <<= 1
            result += next(self.bitit)
            nbits -= 1
        return result
    
    def get_literal(self):
        has_more = self.get_num(1)
        result = self.get_num(4)
        bitsread = 5
        while has_more:
            has_more = self.get_num(1)
            result = (result << 4) + self.get_num(4)
            bitsread += 5
        return result, bitsread

    def get_subpackets(self):
        ltid = self.get_num(1)
        bitsread = 1
        result = []
        if ltid == 1:
            pcount = self.get_num(11)
            bitsread += 11
            while pcount > 0:
                packet, nbits = self.get_packet()
                result.append(packet)
                bitsread += nbits
                pcount -= 1
        else:
            plen = self.get_num(15)
            bitsread += 15
            while plen > 0:
                packet, nbits = self.get_packet()
                result.append(packet)
                bitsread += nbits
                plen -= nbits
        return result, bitsread

    def get_packet(self):
        start = self.bitidx
        version = self.get_num(3)
        type = self.get_num(3)
        bitsread = 6
        result = Packet(version = version, type = type, start = start)
        if type == 4:
            literal, nbits = self.get_literal()
            result.value = literal
        else:
            operator, nbits = self.get_subpackets()
            result.subpackets = operator
        bitsread += nbits
        result.length = bitsread
        return result, bitsread
    
    def get_version_sum(self):
        result, _  = self.get_packet()

        def vsum(node: Packet):
            result = node.version
            if node.subpackets is None: return result
            for snode in node.subpackets:
                result += vsum(snode)
            return result
        
        return vsum(result)


    def eval(self):
        result, _  = self.get_packet()

        def peval(node: Packet):
            if node.type == 0:
                return sum(peval(x) for x in node.subpackets)
            elif node.type == 1:
                return math.prod(peval(x) for x in node.subpackets)
            elif node.type == 2:
                return min(peval(x) for x in node.subpackets)
            elif node.type == 3:
                return max(peval(x) for x in node.subpackets)
            elif node.type == 4:
                return node.value
            elif node.type == 5:
                return 1 if peval(node.subpackets[0]) > peval(node.subpackets[1]) else 0
            elif node.type == 6:
                return 1 if peval(node.subpackets[0]) < peval(node.subpackets[1]) else 0
            elif node.type == 7:
                return 1 if peval(node.subpackets[0]) == peval(node.subpackets[1]) else 0
            else:
                print(node.type)

        return peval(result)
    


pr = PacketReader("420D50000B318100415919B24E72D6509AE67F87195A3CCC518CC01197D538C3E00BC9A349A09802D258CC16FC016100660DC4283200087C6485F1C8C015A00A5A5FB19C363F2FD8CE1B1B99DE81D00C9D3002100B58002AB5400D50038008DA2020A9C00F300248065A4016B4C00810028003D9600CA4C0084007B8400A0002AA6F68440274080331D20C4300004323CC32830200D42A85D1BE4F1C1440072E4630F2CCD624206008CC5B3E3AB00580010E8710862F0803D06E10C65000946442A631EC2EC30926A600D2A583653BE2D98BFE3820975787C600A680252AC9354FFE8CD23BE1E180253548D057002429794BD4759794BD4709AEDAFF0530043003511006E24C4685A00087C428811EE7FD8BBC1805D28C73C93262526CB36AC600DCB9649334A23900AA9257963FEF17D8028200DC608A71B80010A8D50C23E9802B37AA40EA801CD96EDA25B39593BB002A33F72D9AD959802525BCD6D36CC00D580010A86D1761F080311AE32C73500224E3BCD6D0AE5600024F92F654E5F6132B49979802129DC6593401591389CA62A4840101C9064A34499E4A1B180276008CDEFA0D37BE834F6F11B13900923E008CF6611BC65BCB2CB46B3A779D4C998A848DED30F0014288010A8451062B980311C21BC7C20042A2846782A400834916CFA5B8013374F6A33973C532F071000B565F47F15A526273BB129B6D9985680680111C728FD339BDBD8F03980230A6C0119774999A09001093E34600A60052B2B1D7EF60C958EBF7B074D7AF4928CD6BA5A40208E002F935E855AE68EE56F3ED271E6B44460084AB55002572F3289B78600A6647D1E5F6871BE5E598099006512207600BCDCBCFD23CE463678100467680D27BAE920804119DBFA96E05F00431269D255DDA528D83A577285B91BCCB4802AB95A5C9B001299793FCD24C5D600BC652523D82D3FCB56EF737F045008E0FCDC7DAE40B64F7F799F3981F2490")
print(pr.eval())


pr = PacketReader("9C0141080250320F1802104A08")
print(pr.eval())
