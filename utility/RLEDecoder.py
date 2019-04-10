# -------------- RLEDecoder.py  -------------- #
# ----------- dependencies  ---------- #

import os

# ----------- code  ---------- #
# Class used to decode rle pattern files on patterns directory


class RLEDecoder:

    def decode(self, string):
        counter = ""
        out = ""
        for i in string:
            if i.isdigit():
                counter += i
            else:
                if counter:
                    out += (int(counter)*i)
                else:
                    out += i
                counter = ""
        return out

    def decode_pattern(self, file):
        with open(os.path.join("patterns", file), "r") as pattern:
            content = False
            coordinates = False
            map_string = ""
            for line in pattern:
                if "rule" in line: content = True
                if content:
                    if coordinates:
                        map_string += self.decode(line.rstrip('\n'))+'\n'  # coordinates
                    else:
                        dim = [int(s) for s in line.replace(",", "").split(" ") if s.isdigit()]
                        x = dim[0]
                        y = dim[1]
                        coordinates = True

        return x, y, map_string