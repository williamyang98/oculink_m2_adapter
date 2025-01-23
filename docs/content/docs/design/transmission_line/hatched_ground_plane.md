---
title: Hatched ground plane
prev: /docs/design/transmission_line/via_fence_jumps
next: /docs/manufacturing
weight: 4
params:
  icon: hashtag
---

## Stackup
- Very thin dielectric core
- Means very difficult to attain correct impedance without making traces extremely thin with a solid ground plane
- Thicker dielectric cores are provided but they increase cost substantially and trace width is still too thin to manufacture



## Hatched ground plane
- Hatched ground plane can allow for wider traces while matching impedance
- No easy equation to get impedance measurement (fill factor approximation does not model this adequately)
- Requires parametric search with simulation software
- Design of hatched ground plane must meet manufacturing capabilities of JLCPCB

## openEMS simulation
- Many ways to set up simulation
    - Fixed trace width, vary hatch geometry
    - Fixed hatch geometry, vary trace width
    - Select fixed trace width since that is easier to transition to from an existing known trace width on parent boards
- Parametric search by varying hatch width and gap
    - Routing of differential traces over hatch ground plane must be symmetrical otherwise inter-pair skew will result in bad performance
    - Termination of hatched ground plane to SMD pads requires taper to avoid impedance discontinuity and reflections
- Limits in resolution and speed of openEMS due to CPU based design (GPU acceleration not available)
- Ansys supports CUDA acceleration but is difficult to use with exported gerber files
- OpenEMS can be used with a python toolchain to process and setup openEMS harness with gerber files and drill files

## Results
- Table of results
- Graph of impedance
