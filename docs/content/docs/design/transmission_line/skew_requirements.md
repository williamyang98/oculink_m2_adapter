---
title: Skew requirements
prev: /docs/design/transmission_line/structures
next: /docs/design/transmission_line/via_fence_jumps
weight: 2
params:
  icon: switch-horizontal
---

The PCIe standard specifies several requirements for differential pair skew.

## Intra-pair skew (within lane)
Intra-pair skew must be less than 5 mils (0.127mm) which is rather small margin of error.
- This is usually caused by bends in the transmission line lengthening on side of the pair.
- Can be avoided by keeping bends short so local skew error is below 5 mils.
- If skew error is too large than it should be immediately corrected near the bend by adding kinks in the shorter side of the differential pair.

For hatched ground planes in a flexible pcb design improper routing or design can produce large intra-pair skews.
- Further discussion located [here](/docs/design/transmission_line/hatched_ground_plane)

## Inter-pair skew (between lanes)
Inter-pair skew is usually not specified but has a lower bound of 1ns for PCIe 4.0.
- Assuming a propagation speed of 0.6c, the inter-pair skew is around 20cm.
- Since this is such a large value the inter-pair skew requirement is difficult to violate. 
- The reason for this is because the PCIe standard states that transceivers have to do symbol synchronisation.
- Usually done with a buffer which usually can store around 20 symbols for each lane.
- For PCIe 4.0 at a transfer rate of 16GT/s, 20 symbols have a duration of 1.25ns.
