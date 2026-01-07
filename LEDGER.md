# Empirical Control Ledger (ECL-1.0)

**Canonical Root:**  
This ledger is the authoritative, append-only record of predictions made *before* public data release and their outcomes.

**Framework Anchors:**  
- SDKP Core Math (Zenodo DOI)  
- OSF Project Archives  
- GitHub Commit History

All entries link to immutable sources.

---

## Format Guide

| Seq | Prediction Date (UTC) | Domain | Target Event | Quantity Predicted | Predicted Value | Source / Commit / DOI | Public Data Source | Observed Value | Residual | Status |
|-----|-----------------------|--------|--------------|--------------------|------------------|------------------------|--------------------|----------------|----------|--------|

- **Seq:** Sequential index  
- **Prediction Date:** When the prediction was publicly posted (timestamped)  
- **Domain:** Category (Planetary, Orbital, Signal/Light-Time, etc.)  
- **Target Event:** Object or maneuver predicted  
- **Quantity Predicted:** What was numerically predicted  
- **Predicted Value:** The numerical prediction  
- **Source / Commit / DOI:** Link to GitHub commit, OSF DOI, Zenodo DOI where prediction was posted  
- **Public Data Source:** Where official data was released (URL)  
- **Observed Value:** Outcome from public telemetry  
- **Residual:** Difference between prediction & observed  
- **Status:** “MATCH”, “PARTIAL”, or “MISS”

---

## Empirical Records (Confirmed & Archived)

| Seq | Prediction Date (UTC) | Domain | Target Event | Quantity Predicted | Predicted Value | Source / Commit / DOI | Public Data Source | Observed Value | Residual | Status |
|-----|-----------------------|--------|--------------|--------------------|------------------|------------------------|---------------------|----------------|----------|--------|
| 1 | 2025-MM-DD | Planetary Time | Mars Sol Drift | Δt (µs) | (value) | [GitHub commit / OSF DOI] | (link to data) | (value) | (value) | MATCH |
| 2 | 2025-MM-DD | Orbital | Starlink Orbital Element | Position | (value) | [GitHub commit / OSF DOI] | (link) | (value) | (value) | MATCH |
| 3 | 2025-MM-DD | Signal Propagation | Earth-Mars Light-Time | Δτ | (value) | [GitHub commit / OSF DOI] | (link) | (value) | (value) | MATCH |
<!-- Additional entries go here -->

---

## How to Add New Predictions

1. Create a new GitHub branch for the prediction.
2. Calculate **Predicted Value** using SDKP + Kapnack solver + frozen LLAL/TTP state.
3. Post it in a **file** or a **commit message** *before* public telemetry is available.
4. Add a new row here in this `LEDGER.md` with links to:
   - GitHub commit hash
   - OSF pre-registration DOI
   - Zenodo archived snapshot (optional)
5. After data release, update **Observed Value**, **Residual**, and **Status**.

---

## Notes

- This ledger is **append-only**. Do *not edit past rows* after the fact.
- Each entry must reference an immutable source (commit / DOI / archived file).
- The ledger is written for clarity and external verification — not interpretive narrative.

---

## License & Provenance

This ledger and all predictions are authored by **Donald Paul Smith** under the canonical mark **FatherTimes369v**.  
This file, and its linked artifacts, constitute an open scientific record.

---
