# Extended FatherTimeSDKP prototype
# - Multiple particles (each can have a CircleConstraint)
# - RK4 integrator with per-particle constraints
# - Kalman filters (one per particle) for position/velocity estimation
# - Matplotlib visualization of true vs estimated trajectories

import numpy as np
import matplotlib.pyplot as plt

# -----------------------
# Particle & World
# -----------------------
class Particle:
    def __init__(self, mass, x, v):
        self.m = float(mass)
        self.x = np.array(x, dtype=float)
        self.v = np.array(v, dtype=float)

class World:
    def __init__(self, gravity=np.array([0.0, -9.81, 0.0])):
        self.particles = []
        self.g = np.array(gravity, dtype=float)
    def add_particle(self, p: Particle):
        self.particles.append(p)

# -----------------------
# Forces: simple (gravity)
# -----------------------
def compute_forces(world):
    return [p.m * world.g for p in world.particles]

# -----------------------
# Circle constraint (per-particle)
# -----------------------
class CircleConstraint:
    def __init__(self, idx, R):
        self.idx = idx
        self.R = float(R)
    def g(self, x):
        return x[0]**2 + x[1]**2 - self.R**2
    def J(self, x):
        return np.array([2*x[0], 2*x[1], 0.0]).reshape((1,3))
    def J_dot(self, v):
        return np.array([2*v[0], 2*v[1], 0.0]).reshape((1,3))
    def desired_accel_term(self, x, v):
        alpha = 10.0; beta = 10.0
        g = self.g(x)
        g_dot = 2*(x[0]*v[0] + x[1]*v[1])
        return - (2*alpha*g_dot + (beta**2)*g)

# -----------------------
# Compute accelerations with multiple independent constraints
# (Assume constraints affect different particles; solve scalar lambda per constraint)
# -----------------------
def accelerations_with_constraints(world, forces, constraints):
    n = len(world.particles)
    a_unc = [f / p.m for f,p in zip(forces, world.particles)]
    a = a_unc.copy()
    for c in constraints:
        i = c.idx
        p = world.particles[i]
        x = p.x; v = p.v
        J = c.J(x)                    # (1,3)
        M_inv = 1.0 / p.m
        lhs = float((J * M_inv) @ J.T)
        rhs = - ( float((J * M_inv) @ forces[i].reshape((3,1))) + float(c.J_dot(v) @ v.reshape((3,1))) + c.desired_accel_term(x, v) )
        lam = 0.0 if abs(lhs) < 1e-12 else rhs / lhs
        a_corr = (M_inv * (J.T.flatten() * lam))
        a[i] = a[i] + a_corr
    return a

# -----------------------
# RK4 integrator (supports multiple constraints)
# -----------------------
def rk4_step(world, dt, constraints=None):
    n = len(world.particles)
    def pack(ws):
        xs = np.concatenate([p.x for p in ws.particles])
        vs = np.concatenate([p.v for p in ws.particles])
        return xs, vs
    def unpack(ws, xs, vs):
        for i,p in enumerate(ws.particles):
            p.x = xs[3*i:3*i+3].copy()
            p.v = vs[3*i:3*i+3].copy()
    forces1 = compute_forces(world)
    if constraints:
        a1 = accelerations_with_constraints(world, forces1, constraints)
    else:
        a1 = [f / p.m for f,p in zip(forces1, world.particles)]
    xs, vs = pack(world)
    k1_x = np.concatenate([p.v for p in world.particles])
    k1_v = np.concatenate(a1)
    # k2
    ws2 = World(world.g)
    for i,p in enumerate(world.particles):
        p2 = Particle(p.m, p.x + 0.5*dt*k1_x[3*i:3*i+3], p.v + 0.5*dt*k1_v[3*i:3*i+3])
        ws2.add_particle(p2)
    forces2 = compute_forces(ws2)
    if constraints:
        # need to map constraints to new world by copying same constraint objects but index equivalent
        a2 = accelerations_with_constraints(ws2, forces2, constraints)
    else:
        a2 = [f / p.m for f,p in zip(forces2, ws2.particles)]
    k2_x = np.concatenate([p.v for p in ws2.particles])
    k2_v = np.concatenate(a2)
    # k3
    ws3 = World(world.g)
    for i,p in enumerate(world.particles):
        p3 = Particle(p.m, p.x + 0.5*dt*k2_x[3*i:3*i+3], p.v + 0.5*dt*k2_v[3*i:3*i+3])
        ws3.add_particle(p3)
    forces3 = compute_forces(ws3)
    if constraints:
        a3 = accelerations_with_constraints(ws3, forces3, constraints)
    else:
        a3 = [f / p.m for f,p in zip(forces3, ws3.particles)]
    k3_x = np.concatenate([p.v for p in ws3.particles])
    k3_v = np.concatenate(a3)
    # k4
    ws4 = World(world.g)
    for i,p in enumerate(world.particles):
        p4 = Particle(p.m, p.x + dt*k3_x[3*i:3*i+3], p.v + dt*k3_v[3*i:3*i+3])
        ws4.add_particle(p4)
    forces4 = compute_forces(ws4)
    if constraints:
        a4 = accelerations_with_constraints(ws4, forces4, constraints)
    else:
        a4 = [f / p.m for f,p in zip(forces4, ws4.particles)]
    k4_x = np.concatenate([p.v for p in ws4.particles])
    k4_v = np.concatenate(a4)
    xs_new = xs + (dt/6.0)*(k1_x + 2*k2_x + 2*k3_x + k4_x)
    vs_new = vs + (dt/6.0)*(k1_v + 2*k2_v + 2*k3_v + k4_v)
    unpack(world, xs_new, vs_new)

# -----------------------
# Kalman filter (per-particle 2D pos+vel)
# -----------------------
class KalmanFilter:
    def __init__(self, dt, process_var=1e-3, meas_var=1e-2):
        self.dt = dt
        self.A = np.array([[1,0,dt,0],
                           [0,1,0,dt],
                           [0,0,1,0],
                           [0,0,0,1]], dtype=float)
        self.Q = process_var * np.eye(4)
        self.H = np.array([[1,0,0,0],
                           [0,1,0,0]], dtype=float)
        self.R = meas_var * np.eye(2)
        self.x = np.zeros((4,1))
        self.P = np.eye(4)
    def predict(self):
        self.x = self.A @ self.x
        self.P = self.A @ self.P @ self.A.T + self.Q
    def update(self, z):
        z = np.array(z).reshape((2,1))
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        y = z - (self.H @ self.x)
        self.x = self.x + K @ y
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ self.H) @ self.P

# -----------------------
# Demo: N particles each constrained to their own circle
# -----------------------
def simulate_multi(N=3, dt=0.01, steps=2000):
    world = World(gravity=np.array([0.0, 0.0, 0.0]))
    constraints = []
    kfs = []
    traj = [[] for _ in range(N)]
    est = [[] for _ in range(N)]
    radii = np.linspace(3.0, 6.0, N)
    # initialize particles around circle with tangential speed for approximate circular motion
    for i in range(N):
        R = radii[i]
        theta = 2.0 * np.pi * i / N
        x0 = np.array([R*np.cos(theta), R*np.sin(theta), 0.0])
        # tangential direction rotated +90 degrees
        tangent = np.array([-np.sin(theta), np.cos(theta), 0.0])
        speed = 1.0  # choose modest speed
        v0 = speed * tangent
        p = Particle(1.0, x0.copy(), v0.copy())
        world.add_particle(p)
        constraints.append(CircleConstraint(idx=i, R=R))
        kf = KalmanFilter(dt=dt, process_var=1e-4, meas_var=5e-3)
        kf.x = np.array([[x0[0]],[x0[1]],[v0[0]],[v0[1]]])
        kfs.append(kf)
    # simulate
    for n in range(steps):
        rk4_step(world, dt, constraints=constraints)
        for i,p in enumerate(world.particles):
            xt = p.x.copy()
            vt = p.v.copy()
            # measurement with noise
            z = xt[:2] + np.random.normal(scale=0.05, size=2)
            kfs[i].predict()
            kfs[i].update(z)
            traj[i].append(xt.copy())
            est[i].append(kfs[i].x.flatten().copy())
    # convert to arrays
    traj = [np.array(tr) for tr in traj]
    est = [np.array(e) for e in est]
    return traj, est

# -----------------------
# Visualization
# -----------------------
def plot_traj(traj, est, show=True):
    N = len(traj)
    plt.figure(figsize=(8,8))
    colors = plt.cm.viridis(np.linspace(0,1,N))
    for i in range(N):
        pts = traj[i]
        est_pts = est[i]
        plt.plot(pts[:,0], pts[:,1], color=colors[i], lw=1.5, label=f'Particle {i} true')
        plt.plot(est_pts[:,0], est_pts[:,1], '--', color=colors[i], lw=1.0, label=f'Particle {i} est')
        plt.scatter(pts[0,0], pts[0,1], color=colors[i], marker='o')  # start
    plt.axis('equal')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('True vs Estimated Trajectories')
    plt.legend(fontsize='small')
    if show:
        plt.show()

# -----------------------
# Run demo
# -----------------------
if __name__ == "__main__":
    traj, est = simulate_multi(N=4, dt=0.01, steps=3000)
    plot_traj(traj, est)
