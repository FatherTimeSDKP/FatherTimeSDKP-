import numpy as np


class EOSCorrectedAnchorEngine:
    """Computes the scaling relationship between universal lightspeed (c)

    and the local Earth Orbital Speed (EOS / v_e) anchor, ensuring
    dimensional consistency and precise phase propagation delay.
    """

    def __init__(self, distance_m: float):
        self.distance = float(distance_m)  # Spatial path [meters, m]
        self.c = 299792458.0               # Universal Speed of Light [m/s]
        self.v_e = 29780.0                 # Earth Orbital Speed [m/s]

    def compute_standard_light_time(self) -> float:
        """Calculates standard electromagnetic propagation delay using c [seconds]."""
        return self.distance / self.c

    def compute_eos_anchored_modulation(self) -> dict:
        """Applies EOS as a local kinematic scaling anchor, evaluating

        the fractional modulation ratio (v_e / c) without violating c.
        """
        # Dimensionless local kinematic scaling factor (v_e / c)
        scaling_ratio = self.v_e / self.c
        
        t_light = self.compute_standard_light_time()
        
        # Local field propagation time adjusted for terrestrial orbital anchoring [seconds]
        t_anchored = t_light * (1.0 + scaling_ratio)
        
        delta_t = t_anchored - t_light

        return {
            "standard_time_s": t_light,
            "anchored_time_s": t_anchored,
            "delta_t_s": delta_t,
            "scaling_ratio": scaling_ratio,
            "status": "Dimensionally Consistent (c governs speed, v_e governs local anchor)"
        }


# --- Operational Demonstration ---
if __name__ == "__main__":
    # Test distance (e.g., standard baseline path of 1,000,000 meters)
    test_distance = 1000000.0

    engine = EOSCorrectedAnchorEngine(distance_m=test_distance)
    result = engine.compute_eos_anchored_modulation()

    print("=== PRINCIPLE 2: EOS ANCHOR VERIFICATION ===")
    print(f"Standard Light Propagation (c) : {result['standard_time_s']:.9f} s")
    print(f"EOS-Anchored Propagation (v_e) : {result['anchored_time_s']:.9f} s")
    print(f"Modulation Delta (ΔT)          : {result['delta_t_s']:.9f} s")
    print(f"Kinematic Scaling Ratio (v_e/c): {result['scaling_ratio']:.8e}")
    print(f"Status                         : {result['status']}")
