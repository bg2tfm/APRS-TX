# By BG2TFM

class Ax25Frame:
    def __init__(self, dest_addr, src_addr, info):
        print("Dest: %s-1\nSrc:  %s-9\nMessage: %s" % (dest_addr, src_addr, info))
        # 1- Make address field and shift
        addr_field = self.addr_shift(dest_addr + chr(0x71) + src_addr + chr(0x39))  # list of int
        # Dest SSID:-1(0CRRSSSS, C=1)  Sourc SSID:-9(0CRRSSSS, C=0)

        # 2- Make AX.25 payload
        self.ax25_frame = addr_field          # Address field
        self.ax25_frame.extend([0x03, 0xF0])  # Control field and protocol ID
        for k in info:                          # Infomation field
            self.ax25_frame.append(ord(k))

        print("AX.25 payload len: %d" % len(self.ax25_frame))
        # for k in self.ax25_frame:
        #     print(hex(k)[2:], end=" ")

    def addr_shift(self, addr_field):
        s = []
        for k in addr_field:
            s.append(ord(k) << 1)
        s[-1] = 1     # The last bit of Address Field should be '1'

        return s


if __name__ == '__main__':
    # Make sure each addr takes 6 bytes
    ax25_frm = Ax25Frame("BEACON", "BG2TFM", "!3853.20N/12131.59ELDUT SDR LAB")
