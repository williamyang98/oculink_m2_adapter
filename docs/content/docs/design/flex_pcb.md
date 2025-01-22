---
title: Flex PCB
prev: /docs/design/single_board
next: /docs/design/transmission_line
weight: 5
params:
  icon: bookmark
---

## Advantages of flex pcb
- Instead of routing through narrow section can route through wider area underneath M.2 SSD
- Flex pcb is designed to flex which means no bending of solid PCB stackup required
- Wider space means we don't need to jump as many PCIe lanes
    - Possible better electrial performance since vias introduce impedance discontinuities and signal reflections
    - Maximum of 1 via jump in flex pcb design compared to 2 to 3 in single board design
- Instead of routing over FR4 which has a high dielectric loss we are routing over polyethylene flex pcb core which has a lower dielectric loss potentially
- If port position needs to be adjusted, ordering a new flex pcb is much cheaper
- Opens possibility of fixed m.2 card and customisable flex pcb and port board design

## Disadvantage of flex pcb
- Might not have a lower dielectric loss as given by JLCPCB specification so advantage might be nullified
- Thinner dielectric means we need to move from solid to hatched ground plane which introduces design challenges

## Stackup
- Very thin dielectric core
- Means very difficult to attain correct impedance without making traces extremely thin with a solid ground plane
- Thicker dielectric cores are provided but they increase cost substantially and trace width is still too thin to manufacture

## Hatched ground plane
- Hatched ground plane can allow for wider traces while matching impedance
- No easy equation to get impedance measurement (fill factor approximation does not model this adequately)
- Requires parametric search with simulation software
- Design of hatched ground plane must meet manufacturing capabilities of JLCPCB

