import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def calculate_manipulability(J):
    """
    Oblicza miarę manipulacyjności Yoshikawy oraz parametry elipsoidy manipulacyjności.
    """
    # 1. SVD Jacobiana: J = U * Sigma * V^T
    U, S, Vh = np.linalg.svd(J)
    
    # 2. Wskaźnik Yoshikawy: w = det(J*J^T)^(1/2) = iloczyn wartości osobliwych
    w = np.prod(S)
    
    # 3. Elipsoida manipulacyjności:
    # Osie elipsoidy to kolumny U przeskalowane przez wartości osobliwe S
    # W 2D: major axis = S[0]*U[:,0], minor axis = S[1]*U[:,1]
    angle = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
    width = 2 * S[0]
    height = 2 * S[1]
    
    return w, width, height, angle

def forward_kinematics_2d(q, l1, l2):
    """
    Kinematyka prosta dla robota planarnego 2-DOF.
    """
    x = l1 * np.cos(q[0]) + l2 * np.cos(q[0] + q[1])
    y = l1 * np.sin(q[0]) + l2 * np.sin(q[0] + q[1])
    return np.array([x, y])

def jacobian_2d(q, l1, l2):
    """
    Analityczny Jacobian dla robota planarnego 2-DOF.
    """
    # Pochodne cząstkowe po q1, q2
    j11 = -l1 * np.sin(q[0]) - l2 * np.sin(q[0] + q[1])
    j12 = -l2 * np.sin(q[0] + q[1])
    j21 =  l1 * np.cos(q[0]) + l2 * np.cos(q[0] + q[1])
    j22 =  l2 * np.cos(q[0] + q[1])
    return np.array([[j11, j12], [j21, j22]])

def numerical_integration_trapezoid(v_history, dt):
    """
    Numeryczne całkowanie prędkości metodą trapezów.
    """
    x = 0.0
    # Zakładamy start od 0
    for i in range(len(v_history) - 1):
        x += (v_history[i] + v_history[i + 1]) / 2.0 * dt
    return x

# --- PARAMETRY ROBOTA ---
l1, l2 = 5.0, 3.0  # Długości ramion [m]

# --- SYMULACJA RUCHU (DYNAMIKA/NUMERYKA) ---
# Generujemy profil prędkości (trapezoidal velocity profile)
dt = 0.02
t = np.arange(0, 2.0, dt)
v_profile = np.piecewise(t, [t < 0.5, (t >= 0.5) & (t < 1.5), t >= 1.5],
                         [lambda x: 2*x, 1.0, lambda x: 1.0 - 2*(x-1.5)])

# Całkowanie numeryczne pozycji (Metoda Trapezów z Części 3)
#pos_numeric = []
#for i in range(len(t)):
#    fragment = v_profile[:i+1]
#    pozycja  = numerical_integration_trapezoid(fragment, dt)
#    pos_numeric.append(pozycja)
#pos_numeric = [0.0]
#for i in range(len(t) - 1):
#    delta = (v_profile[i] + v_profile[i+1]) / 2.0 * dt
#    pos_numeric.append(pos_numeric[-1] + delta)
pos_numeric = [numerical_integration_trapezoid(v_profile[:i+1], dt) for i in range(len(t))]
q_traj = [] # Trajektoria w złączach (uproszczona: q1=pos, q2=const)
for p in pos_numeric:
    q_traj.append([p, np.radians(45)]) # Ruch tylko barkiem, łokieć zgięty 45st

q_traj = np.array(q_traj)

# --- ANALIZA W KAŻDYM KROKU (ALGEBRA/GEOMETRIA) ---
manipulabilities = []
end_effector_positions = []
ellipses = []

# Wybieramy kilka punktów do wizualizacji elipsoid
#indices_to_plot = set([10, 25, 50, 75, 100, 125, 150, 175, 190])
n = len(t)
num_ellipses = 5
indices_to_plot = set(np.linspace(0, n-1, num_ellipses, dtype = int))

for i in range(len(t)):
    q = q_traj[i]
    
    # 1. Kinematyka (Geometria Analityczna - Część 5)
    pos = forward_kinematics_2d(q, l1, l2)
    end_effector_positions.append(pos)
    
    # 2. Jacobian (Rachunek Różniczkowy - Część 2)
    J = jacobian_2d(q, l1, l2)
    
    # 3. Manipulacyjność (Algebra Liniowa - SVD - Część 1)
    w, width, height, angle = calculate_manipulability(J)
    manipulabilities.append(w)
    
    if i in indices_to_plot:
        ellipses.append((pos, width, height, angle))

end_effector_positions = np.array(end_effector_positions)

# --- WIZUALIZACJA ---
fig, ax = plt.subplots(figsize=(10, 8))

# Ścieżka końcówki
ax.plot(end_effector_positions[:, 0], end_effector_positions[:, 1], 'b-', label='Trajectory (Numerical Integration)', linewidth=2)

# Rysowanie elipsoid manipulacyjności (Statystyka/Algebra - SVD przypomina kowariancję)
for pos, w, h, ang in ellipses:
    ell = Ellipse(xy=pos, width=w*0.4, height=h*0.4, angle=ang, color='r', alpha=0.3)
    ax.add_patch(ell)
    ax.plot(pos[0], pos[1], 'ro', markersize=3)

# Rysowanie robota w ostatniej pozycji
last_q = q_traj[-1]
p0 = [0, 0]
p1 = [l1*np.cos(last_q[0]), l1*np.sin(last_q[0])]
p2 = end_effector_positions[-1]
ax.plot([p0[0], p1[0], p2[0]], [p0[1], p1[1], p2[1]], 'k-o', linewidth=3, label='Robot Arm (Final Pose)')

# Opisy
ax.set_title('Robot Arm Dynamics: Integration, Kinematics & Manipulability (SVD)')
ax.set_xlabel('X [m]')
ax.set_ylabel('Y [m]')
ax.legend()
ax.axis('equal')
ax.grid(True)

plt.tight_layout()
plt.show()
print("Obliczenia zakończone. Generuję wykres...")