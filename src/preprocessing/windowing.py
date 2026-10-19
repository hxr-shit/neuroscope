import numpy as np

def make_windows(raw, seizures, win_sec=4, l_freq=0.5, h_freq=40.0):
    """raw -> (X: [n_win, n_ch, n_samples], y: [n_win])"""
    raw = raw.copy().filter(l_freq, h_freq, verbose="error")
    fs = int(raw.info["sfreq"])
    data = raw.get_data()
    L = win_sec * fs
    n = data.shape[1] // L
    X = data[:, : n * L].reshape(data.shape[0], n, L).transpose(1, 0, 2)

    starts = np.arange(n) * win_sec
    ends = starts + win_sec
    y = np.zeros(n, dtype=int)
    for s, e in seizures:
        y[(starts < e) & (ends > s)] = 1      # koi bhi overlap = seizure window
    return X.astype(np.float32), y