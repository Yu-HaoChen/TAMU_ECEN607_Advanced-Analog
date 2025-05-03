import numpy as np
import matplotlib.pyplot as plt

#==========================================================
# 1) 2.5 bit (綠色): 無容忍度, Z 形鋸齒，使用虛線
#==========================================================
def plot_2p5bit_no_tolerance_zshape(style='g--', label=None):
    boundaries = [-1.0, -5/8, -3/8, -1/8, 1/8, 3/8, 5/8, 1.0]
    n_sub = len(boundaries) - 1  # 7 段

    for i in range(n_sub):
        x_left = boundaries[i]
        x_right = boundaries[i+1]

        # 該段: y 從 -1 線性上升到 +1
        xs_line = np.linspace(x_left, x_right, 50)
        ys_line = -1 + (xs_line - x_left) * 2.0 / (x_right - x_left)  # -1 → +1

        if i == 0 and label is not None:
            plt.plot(xs_line, ys_line, style, label=label)
        else:
            plt.plot(xs_line, ys_line, style)

        # 在段末（非最後一段）做垂直跳變：從 +1 跳到 -1
        if i < n_sub - 1:
            plt.plot([x_right, x_right], [1, -1], style)


#==========================================================
# 2) 2.5 bit (藍色): 帶容忍度, Z 形鋸齒，使用實線
#==========================================================
def plot_2p5bit_with_tolerance_zshape(style='b-', label=None):
    boundaries = [-1.0, -5/8, -3/8, -1/8, 1/8, 3/8, 5/8, 1.0]
    n_sub = len(boundaries) - 1  # 7 段

    # 設計：
    #  - 第一段：從 -1 上升到 +0.5
    #  - 中間段 (第2~6)：從 -0.5 上升到 +0.5，段末垂直跳到 -0.5
    #  - 最後一段：從 -0.5 上升到 +1
    for i in range(n_sub):
        x_left  = boundaries[i]
        x_right = boundaries[i+1]
        if i == 0:
            y_start, y_end = -1.0, +0.5
        elif i < n_sub - 1:
            y_start, y_end = -0.5, +0.5
        else:
            y_start, y_end = -0.5, +1.0

        xs_line = np.linspace(x_left, x_right, 50)
        ys_line = y_start + (xs_line - x_left) * (y_end - y_start) / (x_right - x_left)

        if i == 0 and label is not None:
            plt.plot(xs_line, ys_line, style, label=label)
        else:
            plt.plot(xs_line, ys_line, style)

        # 非最後一段：在段末垂直跳變到 -0.5
        if i < n_sub - 1:
            plt.plot([x_right, x_right], [y_end, -0.5], style)


#==========================================================
# 3) 3 bit (紅色): 無容忍度, Z 形鋸齒 (等距 8 段)，使用點線
#==========================================================
def plot_3bit_no_tolerance_zshape(style='r:', label=None):
    boundaries = [-1.0, -0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0]
    n_sub = len(boundaries) - 1  # 8 段

    for i in range(n_sub):
        x_left  = boundaries[i]
        x_right = boundaries[i+1]

        xs_line = np.linspace(x_left, x_right, 50)
        ys_line = -1 + (xs_line - x_left) * 2 / (x_right - x_left)  # -1→+1

        if i == 0 and label is not None:
            plt.plot(xs_line, ys_line, style, label=label)
        else:
            plt.plot(xs_line, ys_line, style)

        if i < n_sub - 1:
            plt.plot([x_right, x_right], [1, -1], style)


#==========================================================
# 主程式
#==========================================================
def main():
    plt.figure(figsize=(8,6))

    # 繪製三條曲線
    plot_2p5bit_no_tolerance_zshape(style='g--', 
                                    label='2.5 bits (no tolerance)')
    plot_2p5bit_with_tolerance_zshape(style='b-', 
                                      label='2.5 bits (±1/8 Vref tolerance)')
    plot_3bit_no_tolerance_zshape(style='r:', 
                                  label='3 bits')

    #-----------------------------
    # 同時標出 2.5-bit & 3-bit 的 x 軸刻度
    #-----------------------------
    x_ticks_2p5 = [-1, -5/8, -3/8, -1/8, 0, 1/8, 3/8, 5/8, 1]
    x_labels_2p5 = ["-1", "-5/8", "-3/8", "-1/8", "0", "1/8", "3/8", "5/8", "1"]

    x_ticks_3 = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]
    x_labels_3 = ["-1", "-3/4", "-1/2", "-1/4", "0", "1/4", "1/2", "3/4", "1"]

    # 合併並排序，確保不重複
    x_ticks_all = sorted(set(x_ticks_2p5 + x_ticks_3))

    # 建立「刻度 → 標籤」的對應字典
    label_map = {}
    for t, lab in zip(x_ticks_2p5, x_labels_2p5):
        label_map[t] = lab
    for t, lab in zip(x_ticks_3, x_labels_3):
        label_map[t] = lab

    # 根據排序後的刻度產生對應的標籤
    x_labels_all = [label_map[t] for t in x_ticks_all]

    # 套用到 x 軸
    plt.xticks(x_ticks_all, x_labels_all)

    # 其餘繪圖設定
    plt.axhline(0, color='k', linewidth=0.5)
    plt.axvline(0, color='k', linewidth=0.5)
    plt.xlim(-1, 1)
    plt.ylim(-1.05, 1.05)
    plt.xlabel('Input Voltage (Vi)')
    plt.ylabel('Residue Output (Vo)')
    plt.title('Comparison: 2.5-bit & 3-bit MDAC Residue (Z-shape)')
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.show()

if __name__ == '__main__':
    main()





