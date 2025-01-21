---
title: Single Board
prev: /docs/design/kicad_jlcpcb
next: /docs/design/flex_pcb
weight: 3
---

## Advantages of single board
- Only need to solder oculink port and passives
- Can reflow components of opposite sides of the board easily by doing it in parts
- Single kicad schematic required

## Difficulties
- Referring to laptop layout, the lanes have to go through a very narrow section
- Requires moving certain PCIe lanes to other layer which can introduce electrical performance issues
- Board has to bend so that port is at the correct position when screwed into laptop
    - Might result in damage to circuit
    - Probably fine since the flex is tolerable
