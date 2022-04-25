import numpy as np
import re


class CEIL:
    '''
        Interpreter of Chess Environment Interpretation Language (CEIL)

        Version: 0.1.0
    '''

    def parse(self, input: str, shape: tuple[2]) -> np.ndarray:
        cb = np.zeros(shape)
        cur_r, cur_c = -1, -1

        for row in input.strip().split('@'):
            cur_c = -1
            cur_r = cur_r + 1
            if cur_r >= shape[0]:
                break

            for cell in row.strip().split('&'):
                cell_s = cell.strip()
                cur_c = cur_c + 1
                if cur_c >= shape[1]:
                    break

                if len(cell_s) == 0:
                    continue

                if cell_s[0] == 'x' or cell_s[0] == 'X':
                    cur_c = cur_c + int(cell_s[1:]) - 1
                    continue

                cb[cur_r, cur_c] = int(cell_s)

        return cb

    def __remove_redundant(self, s: str) -> str:
        for i in range(len(s) - 1, -1, -1):
            if not re.match(r'[@&0]', s[i]):
                break

        return s[:i+1]

    def __optimize_code(self, gen_code: str) -> str:
        # Remove redundant suffix
        gen_code = self.__remove_redundant(gen_code)

        tmp_gs = ''
        for item in gen_code.split('@'):
            tmp_gs = tmp_gs + self.__remove_redundant(item) + '@'

        gen_code = tmp_gs[:-1]

        # Repeated empty cells detection
        tmp_gs = ''
        repr_start = -1

        for i, ch in enumerate(gen_code):
            if repr_start < 0:
                if ch == '&':
                    repr_start = i
            else:
                if ch != '&':
                    repr_c = i - repr_start - 1
                    repr_start = -1
                    if repr_c > 1:
                        tmp_gs = f"{tmp_gs}&x{repr_c}&"
                    elif repr_c > 0:
                        tmp_gs = tmp_gs + '&&'
                    else:
                        tmp_gs = tmp_gs + '&'

            if ch != '&':
                tmp_gs = tmp_gs + ch

        gen_code = tmp_gs
        del tmp_gs

        return gen_code

    def generate(self, cb: np.ndarray) -> str:
        gs = ''

        for row in cb:
            for cell in row:
                c = str(int(cell))
                gs = gs + (c if c != '0' else '') + "&"

            gs = gs.removesuffix('&') + "@"

        return self.__optimize_code(gs)


def main():
    c = CEIL()
    arr = c.parse("1&x6&5@2&&5@3&6&4&2&x3&1", (8, 8))
    print(arr)
    print(c.generate(arr))


if __name__ == '__main__':
    main()