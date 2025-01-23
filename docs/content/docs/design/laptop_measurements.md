---
title: Laptop measurements
prev: /docs/design/reference_designs
next: /docs/design/kicad_jlcpcb
weight: 2
params:
  icon: color-swatch
---

## Measurement and modelling
{{< responsive_image key="lenovo_16arp8_dimensions" >}}
{{< responsive_image key="lenovo_16arp8_3d_model" >}}

- Modelling was done from a sparse set of measurements.
- After modelling was done arbitrary measurements of any feature could be done.
- Easier than measuring every possible dimension when needed.

## Planning
- Longer M.2 2280 slot is used for high capacity SSD.
- Shorter M.2 2242 slot is available but in a less convenient location.
- Left speaker can be removed to make room for Oculink port.
- M.2 2242 slot has 1mm of clearance for bottom side passive components.
- **Option 1**: Very narrow 12mm gap between M.2 2280 connector and internal display connector for single board design for side Oculink port.
- **Option 2**: Vertical space underneath M.2 2280 slot for routing with a flex pcb design that has a side Oculink port.
- **Option 3**: Use vertical Oculink adapter and have port on bottom instead of side of laptop.

{{< responsive_image key="nfhk_vertical_m2_to_oculink_adapter" style="width: 75%">}}
