import re
from pathlib import Path
import mne

def parse_summary(summary_path):
    """Return {edf_filename: [(start_sec, end_sec), ...]}"""
    text = Path(summary_path).read_text()
    labels = {}
    # har file ka block "File Name:" se shuru hota hai
    for block in re.split(r"(?=File Name:)", text):
        m = re.search(r"File Name:\s*(\S+\.edf)", block)
        if not m:
            continue
        # "Seizure Start Time:" aur "Seizure 1 Start Time:" dono formats handle
        starts = re.findall(r"Seizure\s*\d*\s*Start Time:\s*(\d+)", block)
        ends   = re.findall(r"Seizure\s*\d*\s*End Time:\s*(\d+)", block)
        labels[m.group(1)] = [(int(s), int(e)) for s, e in zip(starts, ends)]
    return labels

def load_edf(path):
    return mne.io.read_raw_edf(path, preload=True, verbose="error")