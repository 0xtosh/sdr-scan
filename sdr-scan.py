import time
from rtlsdr import RtlSdr
import keyboard
from datetime import datetime
import numpy as np
from scipy.io.wavfile import write

# requires:
# - rtl2830 usb dongle
# - pip3 install pyrtlsdr keyboard scipy numpy

def read_frequencies(file_name):
    with open(file_name, 'r') as f:
        return [float(line.strip()) for line in f.readlines()]

def scan_frequencies(sdr, frequencies):
    for freq in frequencies:
        sdr.center_freq = freq * 1e6  # tune to frequency (in Hz)
        print(f'Tuned to {freq} MHz')

        # read some samples
        samples = sdr.read_samples(256*1024)

        # save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'recording_{freq}MHz_{timestamp}'
        np.save(filename + '.npy', samples)

        # convert to wav
        write(filename + '.wav', int(sdr.sample_rate), np.real(samples).astype(np.int16))

        time.sleep(120)
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            print('Exiting...')
            break

def main():
    sdr = RtlSdr()

    try:
        frequencies = read_frequencies('freqs.txt')  # list of frequencies in Mhz format e.g. 135.3900
        while True:
            scan_frequencies(sdr, frequencies)
    finally:
        sdr.close()

if __name__ == '__main__':
    main()

