#!/usr/bin/env python3
"""Offline palette check: contrast and endpoint CVD simulations, not a vision test."""
from itertools import combinations
from pathlib import Path
import json
from chart_style import THEMES, SERIES, DASHES

# Machado 2010 endpoint matrices as retained in Colour's primary implementation:
# https://github.com/colour-science/colour/blob/develop/colour/blindness/datasets/machado2010.py
# Read 27 October 2026. Simulate in linear sRGB; clip before display encoding.
MATRICES = {
    'protanopia': ((.152286, 1.052583, -.204868), (.114503, .786281, .099216), (-.003882, -.048116, 1.051998)),
    'deuteranopia': ((.367322, .860646, -.227968), (.280085, .672501, .047413), (-.011820, .042940, .968881)),
    'tritanopia': ((1.255528, -.076749, -.178779), (-.078411, .930809, .147602), (.004733, .691367, .303900)),
}


def linear(colour):
    rgb = [int(colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]


def luminance(rgb):
    return sum(v * w for v, w in zip(rgb, (.2126, .7152, .0722)))


def contrast(a, b):
    lo, hi = sorted((luminance(a), luminance(b)))
    return (hi + .05) / (lo + .05)


def simulate(rgb, matrix):
    return [min(1, max(0, sum(v * w for v, w in zip(rgb, row)))) for row in matrix]


def encoded(rgb):
    return '#' + ''.join(f'{round(255 * (12.92*v if v <= .0031308 else 1.055*v**(1/2.4)-.055)):02x}' for v in rgb)


def check():
    report = {}
    for theme, colours in THEMES.items():
        bg = linear(colours['bg'])
        ratios = {k: contrast(linear(v), bg) for k, v in colours.items() if k not in ('bg', 'grid')}
        assert min(ratios.values()) >= 4.5, (theme, ratios)
        simulated = {}
        for name, matrix in MATRICES.items():
            palette = {k: simulate(linear(colours[k]), matrix) for k in SERIES}
            simulated[name] = {k: encoded(v) for k, v in palette.items()}
            # Foreground/background visibility is checked separately from category identity.
            assert min(contrast(v, simulate(bg, matrix)) for v in palette.values()) >= 3
        report[theme] = {'contrast_on_background': {k: round(v, 2) for k, v in ratios.items()},
                         'simulated_categorical_colours': simulated}
    assert len(set(DASHES)) == len(SERIES)
    return report


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
