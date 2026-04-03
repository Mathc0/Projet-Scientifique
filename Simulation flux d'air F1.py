import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe
import textwrap

# ─────────────────────────────────────────────
# Données des voitures
# ─────────────────────────────────────────────
VOITURES = {
    1: {
        "nom": "Ferrari SF21",
        "vitesse": 350,
        "angle": 5,
        "surface": 1.5,
        "couleur": "#E8000D",
        "description": (
            "La Ferrari SF21 est la monoplace engagée par la Scuderia Ferrari pour la "
            "saison 2021. Pilotée par Charles Leclerc et Carlos Sainz Jr., elle présente "
            "un museau bas et des ailes optimisées pour maximiser l'appui aérodynamique."
        ),
    },
    2: {
        "nom": "Mercedes W12",
        "vitesse": 360,
        "angle": 4,
        "surface": 1.4,
        "couleur": "#00D2BE",
        "description": (
            "La Mercedes W12, championne du monde 2021, est pilotée par Lewis Hamilton "
            "et Valtteri Bottas. Elle est réputée pour sa fiabilité, son efficacité "
            "aérodynamique et son système hybride ERS sophistiqué."
        ),
    },
    3: {
        "nom": "Red Bull RB16B",
        "vitesse": 355,
        "angle": 6,
        "surface": 1.6,
        "couleur": "#1E41FF",
        "description": (
            "La Red Bull RB16B a remporté le championnat des constructeurs 2021 avec "
            "Max Verstappen et Sergio Pérez. Son moteur Honda et son design innovant "
            "lui confèrent un excellent équilibre entre appui et traînée."
        ),
    },
}

# ─────────────────────────────────────────────
# Fonctions aérodynamiques
# ─────────────────────────────────────────────
rho = 1.225  # kg/m³

def force_trainee(v, angle, S):
    Cd = 0.3 + 0.1 * np.sin(np.radians(angle))
    vs = v / 3.6
    return 0.5 * rho * vs**2 * S * Cd

def force_portance(v, angle, S):
    Cl = 0.2 + 0.05 * np.sin(np.radians(angle))
    vs = v / 3.6
    return 0.5 * rho * vs**2 * S * Cl

# ─────────────────────────────────────────────
# Choix de la voiture
# ─────────────────────────────────────────────
print("\n╔══════════════════════════════════╗")
print("║   Simulation F1 – Flux d'air     ║")
print("╚══════════════════════════════════╝\n")
print("Choisissez une voiture de F1 :")
for k, v in VOITURES.items():
    print(f"  {k}. {v['nom']}")

choix = int(input("\nEntrez le numéro (1, 2 ou 3) : "))
if choix not in VOITURES:
    print("Choix invalide, utilisation de la Ferrari SF21.")
    choix = 1

voiture = VOITURES[choix]
vitesse = voiture["vitesse"]
angle   = voiture["angle"]
surface = voiture["surface"]
couleur = voiture["couleur"]
nom     = voiture["nom"]
desc    = voiture["description"]

Fd = force_trainee(vitesse, angle, surface)
Fl = force_portance(vitesse, angle, surface)

print(f"\n── {nom} ──")
print(f"  Vitesse          : {vitesse} km/h")
print(f"  Angle d'incidence: {angle}°")
print(f"  Surface aéro     : {surface} m²")
print(f"  Force de traînée : {Fd:.1f} N")
print(f"  Force d'appui    : {Fl:.1f} N")

# ─────────────────────────────────────────────
# Figure principale
# ─────────────────────────────────────────────
fig = plt.figure(figsize=(16, 10), facecolor="#0d0d0d")
fig.suptitle(f"Simulation aérodynamique – {nom}",
             color="white", fontsize=15, fontweight="bold", y=0.97)

# ─────────────────────────────────────────────
# 1. Schéma F1 + flux d'air  (grand sous-plot)
# ─────────────────────────────────────────────
ax_schema = fig.add_axes([0.02, 0.32, 0.60, 0.60])
ax_schema.set_facecolor("#0d1117")
ax_schema.set_xlim(0, 10)
ax_schema.set_ylim(0, 6)
ax_schema.set_aspect("equal")
ax_schema.axis("off")
ax_schema.set_title("Flux d'air et forces aérodynamiques",
                    color="white", fontsize=11, pad=8)

# ── Sol ──
ax_schema.axhline(y=1.15, color="#444", linewidth=1.2, zorder=1)

# ── Ombrage sol ──
ax_schema.fill_between([0, 10], [0, 0], [1.15, 1.15],
                        color="#111", zorder=0)

# ────────────────────────────────────────────
# Dessin de la F1 (formes géométriques)
# ────────────────────────────────────────────
car_col   = couleur
dark      = "#1a1a1a"
mid_gray  = "#2a2a2a"
wheel_col = "#1a1a1a"

# -- Châssis principal --
chassis = mpatches.FancyBboxPatch(
    (2.5, 1.9), 5.0, 0.90,
    boxstyle="round,pad=0.18",
    facecolor=dark, edgecolor="#555", linewidth=0.8, zorder=5
)
ax_schema.add_patch(chassis)

# -- Flancs / sidepods --
left_pod = mpatches.FancyBboxPatch(
    (3.0, 1.85), 1.8, 0.55,
    boxstyle="round,pad=0.1",
    facecolor=mid_gray, edgecolor="#444", linewidth=0.6, zorder=4
)
right_pod = mpatches.FancyBboxPatch(
    (5.2, 1.85), 1.8, 0.55,
    boxstyle="round,pad=0.1",
    facecolor=mid_gray, edgecolor="#444", linewidth=0.6, zorder=4
)
ax_schema.add_patch(left_pod)
ax_schema.add_patch(right_pod)

# -- Bande couleur équipe --
bande = mpatches.FancyBboxPatch(
    (2.6, 2.55), 4.8, 0.20,
    boxstyle="round,pad=0.05",
    facecolor=car_col, edgecolor="none", linewidth=0, zorder=6, alpha=0.85
)
ax_schema.add_patch(bande)

# -- Nez (nose cone) --
nose_x = [2.5, 1.85, 1.7, 1.85, 2.5]
nose_y = [2.75, 2.6, 2.45, 2.35, 2.55]
ax_schema.fill(nose_x, nose_y, color=dark, zorder=5)
ax_schema.plot(nose_x, nose_y, color="#555", linewidth=0.6, zorder=6)

# -- Aileron avant --
front_wing_x = [1.55, 0.85, 0.85, 1.55]
front_wing_y = [2.58, 2.53, 2.46, 2.40]
ax_schema.fill(front_wing_x, front_wing_y, color=dark, zorder=5)
ax_schema.plot(front_wing_x + [front_wing_x[0]],
               front_wing_y + [front_wing_y[0]],
               color="#555", linewidth=0.6, zorder=6)
# Flap couleur
flap_x = [0.87, 1.53, 1.52, 0.87]
flap_y = [2.53, 2.57, 2.48, 2.44]
ax_schema.fill(flap_x, flap_y, color=car_col, alpha=0.7, zorder=7)

# -- Aileron arrière --
rear_col = dark
rear_wing = mpatches.Rectangle((7.5, 3.1), 1.0, 0.18,
                                 facecolor=rear_col, edgecolor="#555",
                                 linewidth=0.7, zorder=5)
ax_schema.add_patch(rear_wing)
# Flap secondaire
rear_flap = mpatches.Rectangle((7.52, 2.92), 0.96, 0.12,
                                 facecolor=mid_gray, edgecolor="#444",
                                 linewidth=0.5, zorder=5)
ax_schema.add_patch(rear_flap)
# Mâts
ax_schema.plot([7.9, 7.9], [2.8, 3.1], color="#444", linewidth=2, zorder=5)
ax_schema.plot([8.1, 8.1], [2.8, 3.1], color="#444", linewidth=2, zorder=5)
# Endplates
ax_schema.plot([7.5, 7.5], [2.9, 3.28], color="#555", linewidth=1.5, zorder=5)
ax_schema.plot([8.5, 8.5], [2.9, 3.28], color="#555", linewidth=1.5, zorder=5)

# -- Cockpit --
cockpit = mpatches.Ellipse((5.0, 2.87), 1.0, 0.38,
                             facecolor="#111", edgecolor="#333",
                             linewidth=0.8, zorder=8)
ax_schema.add_patch(cockpit)
# Casque pilote
helmet = mpatches.Ellipse((5.05, 2.93), 0.52, 0.38,
                            facecolor=car_col, edgecolor="none",
                            alpha=0.85, zorder=9)
ax_schema.add_patch(helmet)
visor = mpatches.Ellipse((5.15, 2.95), 0.26, 0.18,
                           facecolor="#85B7EB", edgecolor="none",
                           alpha=0.6, zorder=10)
ax_schema.add_patch(visor)

# -- Roues --
for cx, cy in [(2.1, 1.55), (7.8, 1.55)]:
    outer = plt.Circle((cx, cy), 0.42, color=wheel_col, zorder=6)
    rim   = plt.Circle((cx, cy), 0.22, color="#2a2a2a", zorder=7)
    hub   = plt.Circle((cx, cy), 0.08, color="#555", zorder=8)
    ax_schema.add_patch(outer)
    ax_schema.add_patch(rim)
    ax_schema.add_patch(hub)

# -- Diffuseur arrière --
diff_x = [7.5, 8.5, 8.6, 7.4]
diff_y = [1.9, 1.9, 1.6, 1.6]
ax_schema.fill(diff_x, diff_y, color="#222", zorder=4)
ax_schema.plot(diff_x + [diff_x[0]], diff_y + [diff_y[0]],
               color="#444", linewidth=0.7, zorder=5)

# ────────────────────────────────────────────
# Flux d'air animés (lignes de courant statiques)
# ────────────────────────────────────────────
BLUE  = "#378ADD"
GREEN = "#639922"
AMBER = "#BA7517"
RED   = "#E24B4A"

arrow_kw = dict(arrowstyle="-|>", mutation_scale=8, lw=0)

def streamline(ax, xs, ys, color, lw=1.0, alpha=0.8, n_arrows=3):
    """Trace un filet d'air avec des petites flèches."""
    ax.plot(xs, ys, color=color, lw=lw, alpha=alpha, zorder=3)
    # flèches régulièrement espacées
    n = len(xs)
    step = n // (n_arrows + 1)
    for i in range(step, n - step, step):
        dx = xs[min(i+1, n-1)] - xs[i-1]
        dy = ys[min(i+1, n-1)] - ys[i-1]
        ax.annotate("", xy=(xs[i]+dx*0.01, ys[i]+dy*0.01),
                    xytext=(xs[i]-dx*0.01, ys[i]-dy*0.01),
                    arrowprops=dict(**arrow_kw, color=color),
                    zorder=4)

t = np.linspace(0, 1, 120)

# ── Flux entrants (gauche) ──
for y0 in [4.2, 3.8, 3.4, 3.0, 2.6, 2.2, 1.9]:
    xs = np.linspace(0.0, 1.6, 60)
    ys = np.full(60, y0)
    streamline(ax_schema, list(xs), list(ys), BLUE, lw=1.0, alpha=0.55, n_arrows=2)

# ── Flux extrados (sur la carrosserie) ──
# Ligne supérieure : déviation vers le haut + accélération
for dy_offset in [0.0, 0.12, 0.25]:
    xs = np.concatenate([
        np.linspace(1.6, 2.5, 30),
        np.linspace(2.5, 7.5, 70),
        np.linspace(7.5, 9.5, 20),
    ])
    ys_in   = np.linspace(3.0 + dy_offset, 3.05 + dy_offset, 30)
    ys_over = np.linspace(3.1 + dy_offset, 3.1 + dy_offset, 70) + \
              0.18 * np.sin(np.linspace(0, np.pi, 70))
    ys_out  = np.linspace(3.1 + dy_offset, 3.0 + dy_offset, 20)
    ys = np.concatenate([ys_in, ys_over, ys_out])
    streamline(ax_schema, list(xs), list(ys), GREEN, lw=1.1, alpha=0.75, n_arrows=3)

# ── Flux sous carrosserie – effet venturi ──
for dy_offset in [0.0, 0.08]:
    xs = np.concatenate([
        np.linspace(1.6, 2.5, 20),
        np.linspace(2.5, 7.5, 80),
        np.linspace(7.5, 9.5, 20),
    ])
    ys_in  = np.linspace(1.75 + dy_offset, 1.75 + dy_offset, 20)
    ys_mid = np.linspace(1.75 + dy_offset, 1.75 + dy_offset, 80) - \
             0.15 * np.sin(np.linspace(0, np.pi, 80))
    ys_out = np.linspace(1.75 + dy_offset, 1.75 + dy_offset, 20)
    ys = np.concatenate([ys_in, ys_mid, ys_out])
    streamline(ax_schema, list(xs), list(ys), AMBER, lw=1.2, alpha=0.8, n_arrows=3)

# ── Sillage turbulent (arrière) ──
np.random.seed(42)
for i in range(6):
    base_y  = 2.0 + i * 0.22
    xs_turb = np.linspace(8.55, 9.9, 60)
    noise   = np.cumsum(np.random.randn(60) * 0.012)
    ys_turb = base_y + noise
    ax_schema.plot(xs_turb, ys_turb, color=RED, lw=0.9,
                   alpha=0.65, linestyle="--", zorder=3)

# ────────────────────────────────────────────
# Vecteurs de forces
# ────────────────────────────────────────────
cx, cy = 5.0, 2.5  # centre de la voiture

# Traînée → flèche vers la gauche
fd_scale = 0.5 + (Fd / 3500) * 1.2
ax_schema.annotate("",
    xy=(cx - fd_scale, cy + 0.3),
    xytext=(cx, cy + 0.3),
    arrowprops=dict(arrowstyle="-|>", color=RED,
                    lw=2.5, mutation_scale=14),
    zorder=12
)
ax_schema.text(cx - fd_scale - 0.05, cy + 0.45,
               f"Fd = {Fd:.0f} N", color=RED,
               fontsize=8.5, fontweight="bold", ha="right", zorder=13)

# Downforce → flèche vers le bas
fl_scale = 0.3 + (Fl / 1800) * 0.8
ax_schema.annotate("",
    xy=(cx + 0.8, cy - fl_scale),
    xytext=(cx + 0.8, cy + 0.05),
    arrowprops=dict(arrowstyle="-|>", color=GREEN,
                    lw=2.5, mutation_scale=14),
    zorder=12
)
ax_schema.text(cx + 0.9, cy - fl_scale / 2,
               f"Fl = {Fl:.0f} N", color=GREEN,
               fontsize=8.5, fontweight="bold", ha="left", zorder=13)

# ── Point de stagnation ──
ax_schema.plot(1.72, 2.45, "o", color="#FAC775", markersize=7, zorder=14)
ax_schema.annotate("Point de\nstagnation",
                   xy=(1.72, 2.45), xytext=(0.6, 1.55),
                   color="#FAC775", fontsize=7.5,
                   arrowprops=dict(arrowstyle="-", color="#FAC775",
                                   lw=0.8, linestyle="dashed"),
                   zorder=14)

# ── Légende ──
legend_items = [
    mpatches.Patch(color=BLUE,  label="Écoulement entrant"),
    mpatches.Patch(color=GREEN, label="Extrados (dépression)"),
    mpatches.Patch(color=AMBER, label="Effet de sol (venturi)"),
    mpatches.Patch(color=RED,   label="Sillage turbulent"),
]
ax_schema.legend(handles=legend_items, loc="upper right",
                  fontsize=7.5, facecolor="#1a1a1a",
                  edgecolor="#444", labelcolor="white",
                  framealpha=0.9)

# ─────────────────────────────────────────────
# 2. Graphique forces vs vitesse
# ─────────────────────────────────────────────
ax_forces = fig.add_axes([0.66, 0.55, 0.32, 0.37])
ax_forces.set_facecolor("#0d1117")

vitesses_range = np.linspace(100, 400, 200)
Fd_vals = [force_trainee(v, angle, surface) for v in vitesses_range]
Fl_vals = [force_portance(v, angle, surface) for v in vitesses_range]

ax_forces.plot(vitesses_range, Fd_vals, color=RED,   lw=2,   label="Traînée (Fd)")
ax_forces.plot(vitesses_range, Fl_vals, color=GREEN, lw=2,   label="Appui (Fl)")
ax_forces.axvline(x=vitesse, color="white", lw=0.8, linestyle="--", alpha=0.5)
ax_forces.scatter([vitesse], [Fd], color=RED,   s=55, zorder=5)
ax_forces.scatter([vitesse], [Fl], color=GREEN, s=55, zorder=5)

ax_forces.set_xlabel("Vitesse (km/h)", color="#aaa", fontsize=8)
ax_forces.set_ylabel("Force (N)",      color="#aaa", fontsize=8)
ax_forces.set_title("Forces en fonction de la vitesse",
                    color="white", fontsize=9, pad=6)
ax_forces.tick_params(colors="#888", labelsize=7.5)
ax_forces.spines[:].set_color("#333")
ax_forces.legend(fontsize=8, facecolor="#1a1a1a",
                  edgecolor="#444", labelcolor="white")
ax_forces.grid(True, color="#1f1f1f", linewidth=0.5)

# ─────────────────────────────────────────────
# 3. Barres de forces à vitesse fixe
# ─────────────────────────────────────────────
ax_bars = fig.add_axes([0.66, 0.10, 0.32, 0.37])
ax_bars.set_facecolor("#0d1117")

bars = ax_bars.bar(["Traînée (Fd)", "Appui (Fl)"],
                    [Fd, Fl],
                    color=[RED, GREEN],
                    width=0.45, zorder=3)
for bar, val in zip(bars, [Fd, Fl]):
    ax_bars.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 20,
                 f"{val:.0f} N",
                 ha="center", color="white", fontsize=9, fontweight="bold")

ax_bars.set_ylabel("Force (N)", color="#aaa", fontsize=8)
ax_bars.set_title(f"Forces à {vitesse} km/h",
                  color="white", fontsize=9, pad=6)
ax_bars.tick_params(colors="#888", labelsize=8)
ax_bars.spines[:].set_color("#333")
ax_bars.grid(True, axis="y", color="#1f1f1f", linewidth=0.5)
ax_bars.set_facecolor("#0d1117")

# ─────────────────────────────────────────────
# 4. Description de la voiture
# ─────────────────────────────────────────────
ax_desc = fig.add_axes([0.02, 0.04, 0.60, 0.22])
ax_desc.set_facecolor("#101820")
ax_desc.axis("off")
ax_desc.add_patch(mpatches.FancyBboxPatch(
    (0, 0), 1, 1,
    boxstyle="round,pad=0.02",
    transform=ax_desc.transAxes,
    facecolor="#101820", edgecolor="#333", linewidth=0.8
))

ax_desc.text(0.02, 0.88, nom,
             transform=ax_desc.transAxes,
             color=car_col, fontsize=11, fontweight="bold")

wrapped = textwrap.fill(desc, width=110)
ax_desc.text(0.02, 0.65, wrapped,
             transform=ax_desc.transAxes,
             color="#ccc", fontsize=8.5, va="top",
             linespacing=1.6)

params_str = (
    f"Vitesse : {vitesse} km/h   |   "
    f"Angle d'incidence : {angle}°   |   "
    f"Surface aéro : {surface} m²   |   "
    f"Fd = {Fd:.1f} N   |   Fl = {Fl:.1f} N"
)
ax_desc.text(0.02, 0.12, params_str,
             transform=ax_desc.transAxes,
             color="#888", fontsize=8, va="bottom")

plt.show()
