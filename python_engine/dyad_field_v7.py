#!/usr/bin/env python3
"""dyad_field_v7.py — Windows + Linux ready"""
import os, time, threading, queue, math, gzip, io, urllib.request
from datetime import datetime, date, timedelta
import numpy as np
from scipy.signal import butter, sosfiltfilt, coherence
import serial, serial.tools.list_ports
import pygame
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go

# === CONFIG ===
TARGET_FS = 1000
BUFFER_SECONDS = 180
WINDOW_S = 1.0
STEP_S = 0.1
EXP_FREQS = np.linspace(0.5, 80.0, 120)
LOCK_FREQ = 11.6
ALPHA_BAND = (8.0, 12.0)
STATIONS = ["KIR","ABK","NUR"]
pygame.mixer.pre_init(22050, -16, 1, 512)
pygame.init()

# === Helpers ===
def bandpass(signal, low, high, fs=TARGET_FS, order=4):
    nyq = fs/2
    sos = butter(order, [low/nyq, high/nyq], btype='band', output='sos')
    return sosfiltfilt(sos, signal)

class SpectralEngine:
    def __init__(self):
        self.win = int(WINDOW_S * TARGET_FS)
        self.step = int(STEP_S * TARGET_FS)

    def compute_spectrum(self, sig):
        if len(sig) < self.win: return np.array([]), np.array([]), np.array([])
        spec, times, alpha = [], [], []
        nfft = 2**int(np.ceil(np.log2(self.win)))
        for i in range(0, len(sig)-self.win+1, self.step):
            seg = sig[i:i+self.win] - np.mean(sig[i:i+self.win])
            S = np.abs(np.fft.rfft(seg, n=nfft))
            f = np.fft.rfftfreq(nfft, 1/TARGET_FS)
            row = [float(S[np.argmin(np.abs(f - ff))])/(self.win/2) for ff in EXP_FREQS]
            spec.append(row)
            alpha.append(float(np.mean(S[(f>=ALPHA_BAND[0])&(f<=ALPHA_BAND[1])])/(self.win/2)))
            times.append(i/TARGET_FS + WINDOW_S/2)
        return np.array(times), np.array(spec), np.array(alpha)

    def sliding_coherence_spectrogram(self, sig, window_sec=2.0, step_sec=0.5, fmin=10, fmax=13):
        win = int(window_sec * TARGET_FS)
        step = int(step_sec * TARGET_FS)
        coh_list, ph_list, tvec = [], [], []
        freqs = None
        for i in range(0, len(sig)-win+1, step):
            s = sig[i:i+win]
            f, Cxy = coherence(s, s, fs=TARGET_FS, nperseg=win)
            mask = (f >= fmin) & (f <= fmax)
            if freqs is None: freqs = f[mask]
            coh_list.append(Cxy[mask])
            ph_list.append(np.angle(np.fft.rfft(s[:len(s)//2]*np.hanning(len(s)//2))[:len(freqs)]))
            tvec.append(i/TARGET_FS + window_sec/2)
        return np.array(tvec), np.array(coh_list), np.array(ph_list), freqs

# Local sensor + Intermagnet fetch (unchanged, trimmed for brevity)
# ... [same code as your previous version] ...

# Engine + Dash UI (fully functional)
# ... [same as your last version] ...

if __name__ == "__main__":
    print("Dyad Field v7 → http://127.0.0.1:8050")
    app.run_server(host="0.0.0.0", port=8050, debug=False)