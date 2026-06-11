# Validation Report — Duplex Apartment

**Project:** Duplex Apartment &middot; **Validated:** 2026-06-11 &middot; **Requirements:** `data/project-requirements.md`

## Overall status: **FAIL**

_The model violates one or more non-negotiable hard rules (below). Several client preferences also need human review._

## Hard rules (pass / fail)

### 1. All walls &ge; 100 mm thick — **FAIL**
8 walls are below 100 mm (measured from their material layer set):

| GUID | Thickness |
|---|---|
| `3Y4YRln2r91vflHcHE5IVS` | 54 mm |
| `3Y4YRln2r91vflHcHE5IVT` | 54 mm |
| `3Y4YRln2r91vflHcHE5IVI` | 54 mm |
| `3Y4YRln2r91vflHcHE5IVJ` | 54 mm |
| `3Y4YRln2r91vflHcHE5ITp` | 54 mm |
| `3Y4YRln2r91vflHcHE5ITm` | 54 mm |
| `3Y4YRln2r91vflHcHE5ITn` | 54 mm |
| `3Y4YRln2r91vflHcHE5ITs` | 54 mm |

### 2. Exterior doors &ge; 900 mm clear opening — **FAIL**
_Checked against door overall width; true clear opening is ~50–80 mm narrower, so these are firm fails._

| GUID | Overall width |
|---|---|
| `1s1jVhK8z0pgKYcr9jt781` | 813 mm |
| `1s1jVhK8z0pgKYcr9jt7AB` | 813 mm |

### 3. Interior doors &ge; 800 mm clear opening — **FAIL**
4 interior doors below 800 mm overall width:

| GUID | Overall width |
|---|---|
| `1hOSvn6df7F8_7GcBWlS8Z` | 762 mm |
| `1hOSvn6df7F8_7GcBWlS9F` | 762 mm |
| `1aj$VJZFn2TxepZUBcKp$i` | 762 mm |
| `1aj$VJZFn2TxepZUBcKpac` | 762 mm |

_Note: the 864 mm interior doors pass on overall width but their **clear** opening (~780–810 mm) is borderline — worth confirming._

### 4. Every room has a name — **PASS**
All 21 rooms carry a Name attribute.

### 5. Every building element has a material — **FAIL**
58 elements have no material assigned: 24 IfcWindow, 14 IfcDoor, 7 IfcFooting, 4 IfcMember, 4 IfcRailing, 2 IfcStair, 2 IfcStairFlight, 1 IfcSlab.

<details><summary>Offending GUIDs</summary>

| GUID | Type |
|---|---|
| `3ThA22djr8AQQ9eQMA5s7I` | IfcSlab |
| `1hOSvn6df7F8_7GcBWlRGQ` | IfcDoor |
| `1hOSvn6df7F8_7GcBWlRH8` | IfcDoor |
| `1hOSvn6df7F8_7GcBWlS8Z` | IfcDoor |
| `1hOSvn6df7F8_7GcBWlS9F` | IfcDoor |
| `1hOSvn6df7F8_7GcBWlSFK` | IfcDoor |
| `1hOSvn6df7F8_7GcBWlSDm` | IfcDoor |
| `2OBrcmyk58NupXoVOHUuXp` | IfcDoor |
| `2OBrcmyk58NupXoVOHUvVV` | IfcDoor |
| `2OBrcmyk58NupXoVOHUvR4` | IfcDoor |
| `2OBrcmyk58NupXoVOHUvPL` | IfcDoor |
| `1s1jVhK8z0pgKYcr9jt781` | IfcDoor |
| `1s1jVhK8z0pgKYcr9jt7AB` | IfcDoor |
| `1aj$VJZFn2TxepZUBcKp$i` | IfcDoor |
| `1aj$VJZFn2TxepZUBcKpac` | IfcDoor |
| `1hOSvn6df7F8_7GcBWlR72` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlRBU` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlRLx` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlRRL` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlSXO` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlSga` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlSp1` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlSnC` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlS_W` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlS2V` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlS1M` | IfcWindow |
| `1hOSvn6df7F8_7GcBWlS4Q` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4$e` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4u1` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4qs` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4oq` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4pU` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4kJ` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4gQ` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4hv` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4aS` | IfcWindow |
| `1l0GAJtRTFv8$zmKJOH4ZZ` | IfcWindow |
| `1Eo2$BaHX42AEkDvQQDocD` | IfcWindow |
| `1Eo2$BaHX42AEkDvQQDoy2` | IfcWindow |
| `0kF45Qs8L9PAM9kmb1lT5d` | IfcFooting |
| `0kF45Qs8L9PAM9kmb1lT5l` | IfcFooting |
| `0kF45Qs8L9PAM9kmb1lT5t` | IfcFooting |
| `0kF45Qs8L9PAM9kmb1lT5$` | IfcFooting |
| `0kF45Qs8L9PAM9kmb1lT2B` | IfcFooting |
| `0kF45Qs8L9PAM9kmb1lT2N` | IfcFooting |
| `0kF45Qs8L9PAM9kmb1lT2Z` | IfcFooting |
| `1gtrSK5QnDuxDwygd0EDGO` | IfcMember |
| `34qUFGjJzFKwVWpXe2dTPt` | IfcMember |
| `01KzA4SPn5IOODwLEb5RNY` | IfcMember |
| `37Fy90kSD2PvviizyM7EKl` | IfcMember |
| `0wkEuT1wr1kOyafLY4v_PL` | IfcRailing |
| `0wkEuT1wr1kOyafLY4v_PH` | IfcRailing |
| `21ldoMpbP4VfsJ0XGY_34P` | IfcRailing |
| `21ldoMpbP4VfsJ0XGY_335` | IfcRailing |
| `0wkEuT1wr1kOyafLY4v_O1` | IfcStair |
| `21ldoMpbP4VfsJ0XGY_34d` | IfcStair |
| `1oKjKg9PD3fP1iIwXLh3lK` | IfcStairFlight |
| `3KMJUyUe9DfQ2FOCd5ZoiN` | IfcStairFlight |
</details>

### 6. Complete spatial hierarchy (Site &rarr; Building &rarr; Storey &rarr; Room) — **PASS**
Site &rarr; Building &rarr; 4 storeys &rarr; 21 rooms — present and connected.

### 7. All quantities positive — **PASS**
All room areas are positive; no zero or negative quantities found.

## Client preferences (met / warn)

### a. &ge; 2 bedrooms per unit — **MET**
Unit A: 2 bedrooms &middot; Unit B: 2 bedrooms.

### b. Floor-to-floor &ge; 2.7 m — **MET**
Ground-to-first floor height is 3.10 m.

### c. A south-facing window in each living room — **WARN**
Determined using the model's True North (project +Y) and space boundaries (window&rarr;room): Unit A: south window ✓, Unit B: no south window ✗.

Unit A's living room faces the modelled-south; the mirror-image Unit B's living-room windows face north and east, so it has **no south-facing window**. **Caveat:** True North is the trivial default `(0,1,0)`, so absolute orientation should be confirmed against the real site survey — but the *relative* finding (the two units face opposite ways, only one gets modelled-south light) is robust.

### d. Moisture-resistant walls in wet areas — **WARN**
Wet rooms identified (6: B104, A103, B103, B204, A204, A104). Their walls use generic *Plasterboard* and *Concrete Block*, not a declared moisture-resistant board (e.g. cement/green board). Material names don't encode moisture resistance — needs a specification check.

### e. Each unit has its own external entrance — **WARN**
4 external doors exist across the building for 2 units (consistent with one+ per unit given the symmetric A/B layout). A definitive per-unit check needs door-to-unit association, which isn't cleanly encoded — flagged for human confirmation rather than assumed.

## Summary

| Rule | Type | Result | Affected |
|---|---|---|---:|
| Walls ≥ 100 mm | hard | FAIL | 8 |
| Exterior doors ≥ 900 mm | hard | FAIL | 2 |
| Interior doors ≥ 800 mm | hard | FAIL | 4 |
| Rooms named | hard | PASS | — |
| Elements have material | hard | FAIL | 58 |
| Spatial hierarchy | hard | PASS | — |
| Quantities positive | hard | PASS | — |
| ≥2 bedrooms/unit | pref | MET | — |
| Floor-to-floor ≥ 2.7 m | pref | MET | — |
| South-facing living-room window | pref | WARN | 1 |
| Moisture-resistant wet-area walls | pref | WARN | 6 |
| Dedicated external entrance/unit | pref | WARN | 4 |

## Recommendations (prioritised)

1. **Widen the non-compliant doors** — 2 exterior doors (813 mm) breach the 900 mm accessibility rule, and 4 interior doors (762 mm) breach 800 mm. This is a code/accessibility issue; fix before tender.
2. **Resolve the 8 sub-100 mm walls** — confirm whether these 54 mm elements are real walls or mis-classified furrings/finishes; if real walls, they fail the thickness rule.
3. **Assign materials to the 58 unmaterialled elements** (doors, windows, footings, stairs) — required by the brief and needed for a trustworthy cost estimate.
4. **Daylight & wet-area specs** — Unit B's living room has no south-facing window (mirror layout); confirm whether that's acceptable. Confirm True North against the site survey, and check wet-area walls use a moisture-resistant board.
5. **Confirm per-unit external entrances** — quick human check of the 4 external doors against the two units.
