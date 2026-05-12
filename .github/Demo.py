# FatherTimeSDKP minimal prototype
# - Units: lightweight Quantity class (SI)
# - Particles: Newtonian particle
# - Integrators: RK4
# - Constraint: single holonomic constraint g(x)=0 via Lagrange multiplier
# - Estimation: simple discrete Kalman filter for position/velocity
#
# Usage: run simulate() at bottom. Adjust parameters as needed.

import numpy as np

# -----------------------
# Units / Quantity (minimal)
# -----------------------
class Quantity:
    def __init__(self, value, unit_scale=1.0):
        # value is numeric, unit_scale maps unit to SI (e.g., km -> 1000)
        self.v = float(value) * float(unit_scale)
    def __add__(self, other):
        return Quantity(self.v + other.v)
    def __sub__(self, other):
        return Quantity(self.v - other.v)
    def __mul__(self, other):
        return Quantity(self.v * (other.v if isinstance(other, Quantity) else other))
    def __truediv__(self, other):
        return Quantity(self.v / (other.v if isinstance(other, Quantity) else other))
    def value(self):
        return self.v
    def __repr__(self):
        return f"{self.v} (SI)"

# Helper constructors
def m(x): return Quantity(x, 1.0)         # meters
def kg(x): return Quantity(x, 1.0)        # kg (value treated as SI)
def s(x): return Quantity(x, 1.0)         # seconds

# For simplicity later we unwrap Quantity with .value()

# -----------------------
# Particle & World
# -----------------------
class Particle:
    def __init__(self, mass, x, v):
        self.m = float(mass)        # kg
        self.x = np.array(x, dtype=float)  # position vector
        self.v = np.array(v, dtype=float)  # velocity vector

class World:
    def __init__(self, gravity=np.array([0.0, -9.81, 0.0])):
        self.particles = []
        self.g = np.array(gravity, dtype=float)
    def add_particle(self, p: Particle):
        self.particles.append(p)

# -----------------------
# Forces example: gravity + custom
# -----------------------
def compute_forces(world):
    # returns list of forces for each particle
    forces = []
    for p in world.particles:
        Fg = p.m * world.g
        forces.append(Fg)
    return forces

# -----------------------
# Holonomic constraint: single scalar g(x)=0
# Example: constrain particle to lie on circle x^2 + y^2 - R^2 = 0 in XY plane
# Solve Lagrange multiplier lambda such that M x'' = F + J^T lambda, with J = dg/dx
# -----------------------
class CircleConstraint:
    def __init__(self, idx, R):
        self.idx = idx  # particle index
        self.R = float(R)
    def g(self, x):  # scalar
        return x[0]**2 + x[1]**2 - self.R**2
    def J(self, x):  # gradient row vector shape (1,3)
        return np.array([2*x[0], 2*x[1], 0.0]).reshape((1,3))
    def desired_accel_term(self, x, v):
        # Using Baumgarte stabilization coefficients (alpha, beta)
        alpha = 10.0
        beta = 10.0
        g = self.g(x)
        g_dot = 2*(x[0]*v[0] + x[1]*v[1])
        # we want: g_ddot + 2 alpha g_dot + beta^2 g = 0
        return - (2*alpha*g_dot + (beta**2)*g)

# -----------------------
# RK4 integrator with constraint enforcement (compute accelerations with lambda)
# For single constraint, solve for scalar lambda per particle
# -----------------------
def accelerations_with_constraint(world, forces, constraint: CircleConstraint):
    # Build accel for unconstrained: a = F/m
    a_unc = [f / p.m for f,p in zip(forces, world.particles)]
    # Apply constraint for particle constraint.idx
    i = constraint.idx
    p = world.particles[i]
    x = p.x
    v = p.v
    J = constraint.J(x)                  # shape (1,3)
    M_inv = 1.0 / p.m                    # scalar for single particle
    # Left-hand: J M^{-1} J^T -> scalar
    lhs = (J * M_inv) @ J.T              # (1,1)
    lhs = float(lhs)
    # Right-hand: - (J M^{-1} F + J_dot v + desired_term)
    # J_dot v term (for this constraint J_dot = 2 v_xy ...)
    # compute J_dot v = d/dt(J) * v = 2 * (v . v) ? We compute using derivative: dJ/dt = 2 v_xy row
    J_dot = np.array([2*v[0], 2*v[1], 0.0]).reshape((1,3))
    rhs = - ( (J * M_inv) @ forces[i].reshape((3,1)) + (J_dot @ v.reshape((3,1))) + constraint.desired_accel_term(x, v) )
    rhs = float(rhs)
    # solve lambda
    if abs(lhs) < 1e-12:
        lam = 0.0
    else:
        lam = rhs / lhs
    # corrective accel = M^{-1} J^T lambda
    a_corr = (M_inv * (J.T.flatten() * lam))
    # return list of accelerations
    accs = a_unc.copy()
    accs[i] = accs[i] + a_corr
    return accs

def rk4_step(world, dt, constraint=None):
    n = len(world.particles)
    # Helper to pack state
    def pack_state(ws):
        xs = np.concatenate([p.x for p in ws.particles])
        vs = np.concatenate([p.v for p in ws.particles])
        return xs, vs
    def unpack_state(ws, xs, vs):
        for i,p in enumerate(ws.particles):
            p.x = xs[3*i:3*i+3].copy()
            p.v = vs[3*i:3*i+3].copy()
    # k1
    forces = compute_forces(world)
    if constraint:
        accs = accelerations_with_constraint(world, forces, constraint)
    else:
        accs = [f / p.m for f,p in zip(forces, world.particles)]
    xs, vs = pack_state(world)
    k1_x = np.concatenate([p.v for p in world.particles])
    k1_v = np.concatenate(accs)
    # k2
    ws2 = World(world.g)
    for i,p in enumerate(world.particles):
        p2 = Particle(p.m, p.x + 0.5*dt*k1_x[3*i:3*i+3], p.v + 0.5*dt*k1_v[3*i:3*i+3])
        ws2.add_particle(p2)
    forces2 = compute_forces(ws2)
    if constraint:
        accs2 = accelerations_with_constraint(ws2, forces2, constraint)
    else:
        accs2 = [f / p.m for f,p in zip(forces2, ws2.particles)]
    k2_x = np.concatenate([p.v for p in ws2.particles])
    k2_v = np.concatenate(accs2)
    # k3
    ws3 = World(world.g)
    for i,p in enumerate(world.particles):
        p3 = Particle(p.m, p.x + 0.5*dt*k2_x[3*i:3*i+3], p.v + 0.5*dt*k2_v[3*i:3*i+3])
        ws3.add_particle(p3)
    forces3 = compute_forces(ws3)
    if constraint:
        accs3 = accelerations_with_constraint(ws3, forces3, constraint)
    else:
        accs3 = [f / p.m for f,p in zip(forces3, ws3.particles)]
    k3_x = np.concatenate([p.v for p in ws3.particles])
    k3_v = np.concatenate(accs3)
    # k4
    ws4 = World(world.g)
    for i,p in enumerate(world.particles):
        p4 = Particle(p.m, p.x + dt*k3_x[3*i:3*i+3], p.v + dt*k3_v[3*i:3*i+3])
        ws4.add_particle(p4)
    forces4 = compute_forces(ws4)
    if constraint:
        accs4 = accelerations_with_constraint(ws4, forces4, constraint)
    else:
        accs4 = [f / p.m for f,p in zip(forces4, ws4.particles)]
    k4_x = np.concatenate([p.v for p in ws4.particles])
    k4_v = np.concatenate(accs4)
    # combine
    xs_new = xs + (dt/6.0)*(k1_x + 2*k2_x + 2*k3_x + k4_x)
    vs_new = vs + (dt/6.0)*(k1_v + 2*k2_v + 2*k3_v + k4_v)
    unpack_state(world, xs_new, vs_new)

# -----------------------
# Simple Kalman filter for 2D particle (pos, vel)
# State: [x, y, vx, vy]^T
# Discrete-time constant-accel model (we'll use dt and assume accel as process noise)
# -----------------------
class KalmanFilter:
    def __init__(self, dt, process_var=1e-2, meas_var=1e-1):
        self.dt = dt
        # state transition
        self.A = np.array([[1,0,dt,0],
                           [0,1,0,dt],
                           [0,0,1,0],
                           [0,0,0,1]], dtype=float)
        # Control none; process noise Q:
        q = process_var
        # simple Q affecting acceleration mapped to state; approximate
        self.Q = q * np.eye(4)
        # Measurement H: measure position only
        self.H = np.array([[1,0,0,0],
                           [0,1,0,0]], dtype=float)
        self.R = meas_var * np.eye(2)
        self.x = np.zeros((4,1))
        self.P = np.eye(4)
    def predict(self):
        self.x = self.A @ self.x
        self.P = self.A @ self.P @ self.A.T + self.Q
    def update(self, z):  # z shape (2,) or (2,1)
        z = np.array(z).reshape((2,1))
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        y = z - (self.H @ self.x)
        self.x = self.x + K @ y
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ self.H) @ self.P

# -----------------------
# Simulation demo
# -----------------------
def simulate():
    # Create world and particle constrained to circle radius R in XY plane
    world = World(gravity=np.array([0.0, 0.0, 0.0]))  # turn off gravity for pure circular motion
    R = 5.0
    # initial on circle at (R,0,0) with tangential velocity for circular motion v = sqrt(k/R)
    mass = 1.0
    x0 = np.array([R, 0.0, 0.0])
    # give initial velocity tangent (0, v, 0)
    speed = 1.0
    v0 = np.array([0.0, speed, 0.0])
    p = Particle(mass, x0.copy(), v0.copy())
    world.add_particle(p)
    constraint = CircleConstraint(idx=0, R=R)
    dt = 0.01
    steps = 2000
    # Kalman filter for estimating x,y,vx,vy from noisy position measurements
    kf = KalmanFilter(dt=dt, process_var=1e-4, meas_var=1e-2)
    # initialize KF near true state
    kf.x = np.array([[x0[0]],[x0[1]],[v0[0]],[v0[1]]])
    traj = []
    est_traj = []
    times = []
    for n in range(steps):
        t = n*dt
        # integrate with constraint
        rk4_step(world, dt, constraint=constraint)
        # ground truth position and velocity
        xt = world.particles[0].x.copy()
        vt = world.particles[0].v.copy()
        # noisy measurement (position only)
        meas_noise = np.random.normal(scale=0.1, size=2)  # 0.1 m noise
        z = xt[:2] + meas_noise
        # Kalman predict/update
        kf.predict()
        kf.update(z)
        traj.append((xt.copy(), vt.copy()))
        est_traj.append(kf.x.flatten().copy())
        times.append(t)
    # Print final states
    print("Final true position:", traj[-1][0])
    print("Final true velocity:", traj[-1][1])
    print("Final KF estimate (x,y,vx,vy):", est_traj[-1])
    # Quick energy check (should be roughly conserved if constraint forces do no work)
    speeds = [np.linalg.norm(v) for (_,v) in traj]
    print("Speed stats: mean, min, max:", np.mean(speeds), np.min(speeds), np.max(speeds))

if __name__ == "__main__":
    simulate()
