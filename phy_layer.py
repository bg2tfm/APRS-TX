import numpy as np
import ax25_frame as ax25
import hdlc_frame as hdlc


class PhyLayer:
    def __init__(self, hdlc: hdlc.HdlcFrame, fs):
        self.br = 1200
        self.fs = fs
        self.nrzi_bs = self.nrzi_encode('0'*100 + hdlc.hdlc_bits)
        self.afsk_sig = self.afsk_mod(self.nrzi_bs)

    def nrzi_encode(self, bs: str):
        nrzi = ['0']
        bs = list(bs)

        for i in range(len(bs)):
            if bs[i] == '0':
                nrzi.append('0' if nrzi[i] == '1' else '1')
            else:
                nrzi.append(nrzi[i])

        nrzi = "".join(nrzi[1:])
        print("Encoding to NRZI: %d" % len(nrzi))

        return nrzi

    def afsk_mod(self, bs: str):
        print("AFSK modulated with Fs=%d." % self.fs)
        bs = list(bs)
        s = []
        phase = 0

        n_pt = int(self.fs/self.br)
        tt = np.linspace(0, 1/self.br, n_pt)

        for k in bs:
            f0 = (1200 if k == '0' else 2200)
            s.extend(np.cos(2*np.pi*f0*tt+phase))

            # Phase tracking, to make the phase continuous
            phase = (phase + (1+1/n_pt)*(2*np.pi*f0/self.br)) % (2*np.pi)

        return s


if __name__ == '__main__':
    ax25_frm = ax25.Ax25Frame("BEACON", "BG2TFM", "!3853.10N/12131.45E`Python code by D.M.")
    hdlc_frm = hdlc.HdlcFrame(ax25_frm)
    afsk_sig = PhyLayer(hdlc_frm, 48e3)
