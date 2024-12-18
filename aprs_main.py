import time
import pyaudio
import numpy as np
from matplotlib import pyplot as plt

import ax25_frame as ax25
import hdlc_frame as hdlc
import phy_layer as phy

DRAW_ON = 0
au_fs = int(48e3)
dest = "BEACON"
src = "BG2TFM"
msg = "!3853.10N/12131.45E`Python code via FM radio"


def over_sampling(sig: str, n=40):
    s = []
    for k in sig:
        s.append(int(k, 10))

    return np.repeat(s, n)


if __name__ == "__main__":
    hdlc_frm = hdlc.HdlcFrame(ax25.Ax25Frame(dest, src, msg))
    phy_dat = phy.PhyLayer(hdlc_frm, au_fs)
    au_sig = np.array(phy_dat.afsk_sig, dtype=np.float32)

    # Drive the soundcard
    p = pyaudio.PyAudio()
    ss = p.open(format=pyaudio.paFloat32, channels=1, rate=au_fs, output=True)
    ss.write(au_sig.tobytes())
    time.sleep(0.5)
    ss.close
    p.terminate()

    if DRAW_ON:
        nrzi = over_sampling(phy_dat.nrzi_bs, 40)

        plt.plot(au_sig)
        plt.plot(2*(nrzi-0.5), 'r')
        plt.xlim([6000, 8000])
        plt.ylim([-2, 2])
        plt.grid()
        plt.show()
