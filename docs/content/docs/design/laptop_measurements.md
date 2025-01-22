---
title: Laptop Measurements
prev: /docs/design/reference_designs
next: /docs/design/kicad_jlcpcb
weight: 2
params:
  icon: color-swatch
---

## Laptop measurements
- M.2 card must have enough clearance for passive components such as capacitors, diodes if they are on the bottom side
- Location of port must be in a location where traces can be routed

## Routing challenges
- Other M.2 slot is in the way of direct connection between port location and M.2 slot
- Using smaller M.2 slot for larger SSD choices at the cost of more complex and longer routing

## Stackup
- Fixed thickness of 0.8mm to meet M.2 finger connector requirement
- To ease with stackup 4 layers is chosen
- JLCPCB has very little pricing increase when moving from 2 layers to 4 layers
- Allows for movement of traces to additional layers allowing for easier physical layout if bottleneck is found

