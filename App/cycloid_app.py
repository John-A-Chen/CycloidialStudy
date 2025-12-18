# cycloid_app.py
# Single-file Streamlit cycloidal drive helper:
# - preview rotor profile + rollers + output holes
# - export SolidWorks parametric equations + parameter list + CSV points
#
# Maths/export style follows the widely used SolidWorks parametric curve form:
# X = (R*cos(t))-(Rr*cos(t+psi))-(E*cos(N*t))
# Y = (-R*sin(t))+(Rr*sin(t+psi))+(E*sin(N*t))
# psi = atan( sin((1-N)*t) / ((R/(E*N)) - cos((1-N)*t)) )
#
# NOTE: SolidWorks can choke if t range is exactly 0..2*pi. Use 2*pi - eps.

import math
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


# ----------------------------
# SECTION A: Parameters + Maths
# ----------------------------

@dataclass
class Params:
    # Core rotor inputs (mm)
    R: float      # rotor radius (roller pitch circle radius)
    Rr: float     # roller radius (pin radius)
    E: float      # eccentricity
    N: int        # number of rollers

    # Output holes (mm)
    out_pin_circle_R: float
    out_pin_count: int
    out_pin_diam: float
    hole_clearance: float

    # Disc options
    dual_disc: bool
    disc2_phase_deg: float  # normally 180

    # Sampling
    samples: int
    eps: float  # radians


def gear_ratio_N_to_Nminus1(N: int) -> float:
    # Common single-disc cycloidal reducer: lobes = N-1 gives ratio ~ (N-1):1 (architecture dependent)
    # Keep this as an indicative display only.
    if N <= 1:
        return float("nan")
    return (N - 1) / 1.0


def cycloid_profile_xy(t: np.ndarray, R: float, Rr: float, E: float, N: int, phase_rad: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    """
    Rotor profile point generation using the same structure as the Younis app equations.
    Uses atan2 for numerical stability in Python. For SolidWorks export we’ll output atan(sin/denom).

    If you want to emulate the "fit check" from Younis preview, add +E to X to offset the disc.
    Here we keep it centred at origin and let you overlay rollers separately.
    """
    tt = t + phase_rad
    a = (1 - N) * tt
    denom = (R / (E * N)) - np.cos(a)
    psi = np.arctan2(np.sin(a), denom)

    x = (R * np.cos(tt)) - (Rr * np.cos(tt + psi)) - (E * np.cos(N * tt))
    y = (-R * np.sin(tt)) + (Rr * np.sin(tt + psi)) + (E * np.sin(N * tt))
    return x, y


def roller_centres(R: float, N: int) -> np.ndarray:
    """Centres of rollers on pitch circle radius R."""
    ang = np.linspace(0, 2*np.pi, N, endpoint=False)
    return np.column_stack((R*np.cos(ang), R*np.sin(ang)))


def output_hole_centres(out_pin_circle_R: float, out_pin_count: int) -> np.ndarray:
    ang = np.linspace(0, 2*np.pi, out_pin_count, endpoint=False)
    return np.column_stack((out_pin_circle_R*np.cos(ang), out_pin_circle_R*np.sin(ang)))


# ----------------------------
# SECTION B: Exporters
# ----------------------------

def solidworks_equations_text(p: Params) -> str:
    # Keep it maximally compatible: SolidWorks supports atan(), sin(), cos().
    # Use the classic “psi” definition (atan of fraction).
    # Provide a recommended t range 0 .. 2*pi - eps.
    N = p.N

    psi = (
        f"atan( sin((1-{N})*t) / ((R/(E*{N})) - cos((1-{N})*t)) )"
    )
    x_eq = f"X = (R*cos(t)) - (Rr*cos(t + {psi})) - (E*cos({N}*t))"
    y_eq = f"Y = (-R*sin(t)) + (Rr*sin(t + {psi})) + (E*sin({N}*t))"

    t0 = 0.0
    t1 = (2.0 * math.pi) - p.eps

    lines = []
    lines.append("SolidWorks Equation Driven Curve (Parametric)")
    lines.append("Units: mm for R, Rr, E. Parameter t is radians.")
    lines.append("")
    lines.append("Define these variables in SolidWorks Equations:")
    lines.append(f"R  = {p.R}")
    lines.append(f"Rr = {p.Rr}")
    lines.append(f"E  = {p.E}")
    lines.append(f"N  = {p.N}")
    lines.append("")
    lines.append("Paste into the Equation Driven Curve dialog:")
    lines.append(x_eq)
    lines.append(y_eq)
    lines.append("")
    lines.append(f"Recommended t range: {t0} to {t1} (avoid exactly 2*pi)")
    if p.dual_disc:
        phase = math.radians(p.disc2_phase_deg)
        lines.append("")
        lines.append("Optional: Disc 2 (phase shifted)")
        lines.append(f"Use t2 = t + {phase}  (or add {phase} everywhere t appears)")
    return "\n".join(lines)


def parameters_text(p: Params) -> str:
    lobes = p.N - 1
    ratio_hint = gear_ratio_N_to_Nminus1(p.N)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append(f"Generated: {ts}")
    lines.append("")
    lines.append("Core rotor parameters (mm unless stated):")
    lines.append(f"N (rollers)            = {p.N}")
    lines.append(f"Lobes (N-1)             = {lobes}")
    lines.append(f"R  (roller PCD radius)  = {p.R}")
    lines.append(f"Rr (roller radius)      = {p.Rr}")
    lines.append(f"E  (eccentricity)       = {p.E}")
    lines.append(f"Ratio hint (~N-1)        = {ratio_hint:g}")
    lines.append("")
    lines.append("Output holes:")
    lines.append(f"Output pin circle radius = {p.out_pin_circle_R}")
    lines.append(f"Output pin count         = {p.out_pin_count}")
    lines.append(f"Output pin diameter      = {p.out_pin_diam}")
    lines.append(f"Hole clearance           = {p.hole_clearance}")
    lines.append("")
    lines.append("Sampling:")
    lines.append(f"samples                  = {p.samples}")
    lines.append(f"eps (rad)                = {p.eps}")
    if p.dual_disc:
        lines.append("")
        lines.append("Dual disc:")
        lines.append(f"disc2 phase (deg)        = {p.disc2_phase_deg}")
    return "\n".join(lines)


def csv_points(x: np.ndarray, y: np.ndarray) -> str:
    out = ["x_mm,y_mm"]
    for xi, yi in zip(x, y):
        out.append(f"{xi:.6f},{yi:.6f}")
    return "\n".join(out)


# ----------------------------
# SECTION C: Streamlit UI
# ----------------------------

st.set_page_config(page_title="Cycloidal Drive App", layout="wide")
st.title("Cycloidal Drive App (single-file)")

with st.sidebar:
    st.header("Rotor inputs (mm)")
    N = st.number_input("Number of rollers (N)", min_value=3, value=10, step=1)
    R = st.number_input("Roller pitch circle radius (R)", min_value=0.1, value=20.0, step=0.5, format="%.3f")
    Rr = st.number_input("Roller radius (Rr)", min_value=0.1, value=3.0, step=0.1, format="%.3f")
    E = st.number_input("Eccentricity (E)", min_value=0.001, value=1.1, step=0.05, format="%.4f")

    st.divider()
    st.header("Output holes")
    out_pin_circle_R = st.number_input("Output pin circle radius", min_value=0.1, value=10.0, step=0.5, format="%.3f")
    out_pin_count = st.number_input("Output pin count", min_value=3, value=4, step=1)
    out_pin_diam = st.number_input("Output pin diameter", min_value=0.1, value=8.0, step=0.5, format="%.3f")
    hole_clearance = st.number_input("Hole clearance (+diameter)", min_value=0.0, value=0.2, step=0.05, format="%.3f")

    st.divider()
    st.header("Disc options")
    dual_disc = st.checkbox("Dual disc (show disc 2)", value=False)
    disc2_phase_deg = st.number_input("Disc 2 phase (deg)", min_value=0.0, max_value=360.0, value=180.0, step=1.0)

    st.divider()
    st.header("Sampling / SolidWorks stability")
    samples = st.slider("Samples (preview + CSV)", min_value=200, max_value=6000, value=1200, step=100)
    eps = st.number_input("Epsilon (rad) for 2π", min_value=1e-6, value=9e-4, step=1e-4, format="%.6f")

p = Params(
    R=float(R),
    Rr=float(Rr),
    E=float(E),
    N=int(N),
    out_pin_circle_R=float(out_pin_circle_R),
    out_pin_count=int(out_pin_count),
    out_pin_diam=float(out_pin_diam),
    hole_clearance=float(hole_clearance),
    dual_disc=bool(dual_disc),
    disc2_phase_deg=float(disc2_phase_deg),
    samples=int(samples),
    eps=float(eps),
)

# Sanity checks
warnings = []
if p.E <= 0:
    warnings.append("E must be > 0.")
if p.E > (p.R / p.N):
    warnings.append("E is larger than R/N. This often causes ugly/self-intersecting profiles. Not always invalid, but check fit.")
if p.R <= p.Rr:
    warnings.append("R should usually be larger than Rr (roller circle radius vs roller radius).")
if warnings:
    for w in warnings:
        st.warning(w)

# Generate profile points
t = np.linspace(0.0, (2.0 * math.pi) - p.eps, p.samples, endpoint=True)
x1, y1 = cycloid_profile_xy(t, p.R, p.Rr, p.E, p.N, phase_rad=0.0)

phase2 = math.radians(p.disc2_phase_deg)
if p.dual_disc:
    x2, y2 = cycloid_profile_xy(t, p.R, p.Rr, p.E, p.N, phase_rad=phase2)
else:
    x2, y2 = None, None

# Build plot
fig = plt.figure(figsize=(7, 7))
ax = plt.gca()

# Rotor curve(s)
ax.plot(x1, y1, linewidth=2, label="Rotor (disc 1)")
if p.dual_disc:
    ax.plot(x2, y2, linewidth=2, linestyle="--", label="Rotor (disc 2)")

# Rollers
centres = roller_centres(p.R, p.N)
th = np.linspace(0, 2*np.pi, 120)
for i, (cx, cy) in enumerate(centres):
    rx = cx + p.Rr*np.cos(th)
    ry = cy + p.Rr*np.sin(th)
    if i == 0:
        ax.plot(rx, ry, linewidth=1.5, label="Rollers")
    else:
        ax.plot(rx, ry, linewidth=1.5)

# Output holes (as circles)
hole_R = (p.out_pin_diam + p.hole_clearance) / 2.0
out_centres = output_hole_centres(p.out_pin_circle_R, p.out_pin_count)
for i, (cx, cy) in enumerate(out_centres):
    hx = cx + hole_R*np.cos(th)
    hy = cy + hole_R*np.sin(th)
    if i == 0:
        ax.plot(hx, hy, linewidth=1.5, label="Output holes")
    else:
        ax.plot(hx, hy, linewidth=1.5)

ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("x (mm)")
ax.set_ylabel("y (mm)")
ax.grid(True, linewidth=0.5)
ax.legend(loc="upper right")

st.pyplot(fig, clear_figure=True)

# Exports
st.subheader("Exports")

eq_txt = solidworks_equations_text(p)
st.text_area("SolidWorks equations (copy/paste)", value=eq_txt, height=220)

par_txt = parameters_text(p)
st.text_area("Parameter summary", value=par_txt, height=220)

# CSVs (disc 1 always; disc 2 optional)
csv1 = csv_points(x1, y1)
st.download_button(
    "Download Disc 1 points (CSV)",
    data=csv1.encode("utf-8"),
    file_name=f"disc1_points_N{p.N}_R{p.R}_Rr{p.Rr}_E{p.E}.csv",
    mime="text/csv",
)

if p.dual_disc:
    csv2 = csv_points(x2, y2)
    st.download_button(
        "Download Disc 2 points (CSV)",
        data=csv2.encode("utf-8"),
        file_name=f"disc2_points_N{p.N}_R{p.R}_Rr{p.Rr}_E{p.E}_phase{p.disc2_phase_deg}.csv",
        mime="text/csv",
    )

st.download_button(
    "Download SolidWorks equations (TXT)",
    data=eq_txt.encode("utf-8"),
    file_name=f"solidworks_equations_N{p.N}_R{p.R}_Rr{p.Rr}_E{p.E}.txt",
    mime="text/plain",
)

st.download_button(
    "Download parameters (TXT)",
    data=par_txt.encode("utf-8"),
    file_name=f"parameters_N{p.N}_R{p.R}_Rr{p.Rr}_E{p.E}.txt",
    mime="text/plain",
)

st.caption("If SolidWorks rejects the curve: increase epsilon (eps) slightly (e.g., 0.001–0.01) or reduce sample density.")
