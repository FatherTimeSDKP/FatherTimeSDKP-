def time_dilation_factor(v_eos):
    c = 3e8  # Speed of light, m/s
    return 1 / (1 - (v_eos / c)**2)**0.5  # Simplified Lorentz factor
print(f"Time dilation at v_EOS={7.8e3}: {time_dilation_factor(7.8e3):.6f}")
