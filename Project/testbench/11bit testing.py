def mdac_stage(vi):
    """
    2.5-bit MDAC stage:
      - 根据输入 vi 决定重构值 s ∈ {-3…+3}
      - 计算 DAC = s * 0.225
      - 计算残值 vo = 4 * (vi - DAC)
      - 返回 vo 和 3-bit code = s+3 (范围 0…6)

    阈值:
      vi < -0.562       → s = -3
    -0.562 ≤ vi < -0.337 → s = -2
    -0.337 ≤ vi < -0.112 → s = -1
    -0.112 ≤ vi <  0.112 → s =  0
     0.112 ≤ vi <  0.337 → s =  1
     0.337 ≤ vi <  0.562 → s =  2
       vi ≥ 0.562       → s =  3
    """
    LSB = 0.225

    if vi < -0.562:
        s = -3
    elif vi < -0.337:
        s = -2
    elif vi < -0.112:
        s = -1
    elif vi <  0.112:
        s =  0
    elif vi <  0.337:
        s =  1
    elif vi <  0.562:
        s =  2
    else:
        s =  3

    dac = s * LSB
    vo  = 4 * (vi - dac)
    code_3bit = s + 3
    return vo, code_3bit, dac


def flash_stage(vi):
    """
    最后一级 Flash ADC：
      - 同样的阈值决策
      - 不产生残值，直接返回 code_3bit = s+3
    """
    if vi < -0.562:
        s = -3
    elif vi < -0.337:
        s = -2
    elif vi < -0.112:
        s = -1
    elif vi <  0.112:
        s =  0
    elif vi <  0.337:
        s =  1
    elif vi <  0.562:
        s =  2
    else:
        s =  3

    return s + 3


def combine_vertical(codes):
    """
    直列二进位加法合成最终 11-bit 结果。
    """
    bits = [((c>>2)&1, (c>>1)&1, c&1) for c in codes]
    columns = [
        [bits[0][0]],
        [bits[0][1]],
        [bits[0][2], bits[1][0]],
        [bits[1][1]],
        [bits[1][2], bits[2][0]],
        [bits[2][1]],
        [bits[2][2], bits[3][0]],
        [bits[3][1]],
        [bits[3][2], bits[4][0]],
        [bits[4][1]],
        [bits[4][2]],
    ]
    result = [0]*len(columns)
    carry = 0
    for i in range(len(columns)-1, -1, -1):
        s = carry + sum(columns[i])
        result[i] = s & 1
        carry    = s >> 1
    if carry:
        result.insert(0, carry)
    return ''.join(str(b) for b in result)


def main():
    vin = float(input("Vin: "))

    print("\nstage output：")
    hdr = f"{'Stg':>3} {'Vin':>8} {'Vo':>8} {'DAC':>8} {'Code':>6}"
    print(hdr)
    print("-"*len(hdr))

    codes = []
    current = vin

    # 前 4 级 MDAC
    for st in range(1,5):
        vo, code, dac = mdac_stage(current)
        print(f"{st:3d} {current:8.4f} {vo:8.4f} {dac:8.4f} {format(code,'03b'):>6}")
        codes.append(code)
        current = vo

    # 第 5 级 Flash
    code_f = flash_stage(current)
    print(f"{5:3d} {current:8.4f} {'----':>8} {'----':>8} {format(code_f,'03b'):>6}")
    codes.append(code_f)

    final = combine_vertical(codes)
    print("\n 11-bit output：")
    print(final)


if __name__ == "__main__":
    main()



