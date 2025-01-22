---
title: Transmission Line
prev: /docs/design/flex_pcb
next: /docs/design/hatched_ground_plane
weight: 6
params:
  icon: switch-horizontal 
---

## Transmission line structures
Many possible transmission line geometries
- Differential, single ended
- Coplanar ground (relation to common mode signals)
- Ground plane

## Via fence
- Reduce EMI and prevent crosstalk with adjacent lanes
- Limitation on design options set by price and fabrication (minimum via size and annular ring)
- Spacing requirements and equation for spacing for maximum design frequency

- Staggered via fence performance better than regular via fence
- Requries micro vias and buried vias which JLCPCB does not support

## Skin effect
- Copper thickness and surface roughness
- Effect at higher frequencies
- Difficulty modelling this with tools and available simulation software
- Lack of availability without moving to HDI stackup which is more expensive
