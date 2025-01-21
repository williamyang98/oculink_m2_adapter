---
title: Conclusion
prev: /docs/results/synthetic_benchmarks
next: /gallery
weight: 6
---

## Custom adapter
- Can be designed and achieve PCIe 3.0 speeds reliably
- Unlikely to achieve PCIe 4.0 due to aformentioned issues
- Time consuming to construct
- Difficult to manufacture requiring multiple attempts
- Potential risk of shorting if assembly was done poorly
- If form factor is extremely unusual or limited this might be an option you should consider

## Aliexpress adapter
- Otherwise purchasing a PCIe 4.0 adapter from aliexpress with bendable cables is a better option 
- More performance
- Cheaper overall when considering parts and equipment
- Sourcing oculink port and SMD components has a hefty shipping fee from most electronic suppliers
- Aliexpress has very low to non existent shipping fees
- Adapter has controlled impedance cables in many lengths which are bendable and thus can be adapted to a variety of enclosures

## Lessons learnt
- Interesting exercise in practical high frequency transmission line design
- Research was relatively straight forward due to public schematics from AdtLink and datasheets
- Design was time consuming especially for the flex pcb which required a manually routed hatched ground plane due to KiCAD limitations
    - Altium or more mature software might have better hatched ground plane design tools
    - In order to route bends in hatched ground plane it was easier to make the entire hatch manually with trace segments
    - Distort the hatch at bend to maintain as much symmetry
    - Using default hatched ground plane implementation would have resulted in extreme inter-pair skew and terrible performance
- Manufacturing was time consuming due to microsoldering, improper reflow, and hand testing of adapter
    - Unless stencil application is ideal there will be dry joints or bridges
    - Difficult or impossible to visually inspect since half of the oculink pads are underneath the port
- Due to use of passive components, the most informative part of this project was high frequency transmission line design
    - PCIe redriver ICs are not cheap and are not usually sold in low quantities
    - Optimised passive adapter is the most cost effective option
    - Microsoldering of flex pcb could achieve near zero pitch error with aid of magnifying glass but is limited to dexterity and patience
    - Aliexpress adapter uses special micro coaxial cables which will perform better than flex pcb with hatched ground plane or direct routing over lossy FR4 over distances longer than 10cm
- Design of hatch ground plane is not solvable using equations
    - Requires simulation tools
    - openEMS is a free option but is uses the CPU only and only leverages SSE extensions which are a decade old
    - Open source github repo that handles preprocessing of gerber files, setup of openEMS simulation, and analysis of results to produce impedance graphs over frequency
    - Ansys does not have a easy (or at least not something that is easy to look up) way of importing gerber files for simulation
    - Ansys is GPU accelerated but only with CUDA, which is okay if you have an Nvidia gpu but not if you have an Intel or AMD gpu
    - Ansys will sometimes give an error without an explanation

## Requirements to reach PCIe 4.0
- Final performance of adapter reached minimum target of PCIe 3.0 but failed the more ambitious PCIe 4.0

To reach PCIe 4.0 it would probably require:
- Lower loss dielectric materials
- Better simulation of via jumps in transmission line to match impedance and prevent reflections
- Better design of flex pcb hatched ground plane to hit impedance target or avoid it altogether with single board design
- Increase transmission line trace width to mitigate impact of skin effect at higher frequencies (most effective)
- Use thicker copper layers (only effective at lower frequencies)
- Use smoother copper finish since surface roughness results in higher impedance due to skin effect (very effective)
    - Unknown if this can be done cheaply without moving to a more expensive HDI stackup
- Replace flex pcb with micro coax (doesn't seem easy to do since it would require alot of microsoldering of extremely fine traces)

## Future plans
- In flex pcb design the oculink port board can be swapped out with another type of connector
- Potential candidates are
    - Mini cool edge IO (MCIO) - Better official number of insertion cycles
    - Far far future there may be electrical to optical solution for PCIe like with PCIe 7.0 (unlikely to be available at consumer prices)
    - Improved oculink connector that is rated for higher insertion cycles
- Wait for Thunderbolt 5 with 128Gbp/s of bandwidth
    - Thunderbolt 4 with 64Gbp/s of bandwidth should be comparable to PCIe 4.0 x 4 but there is overhead somewhere which results in much worse performance
    - Requires a very recent CPU to have support for Thunderbolt 4
    - Thunderbolt eGPU docks are very expensive
    - Oculink solution has cheaper cables and eGPU docks compared to thunderbolt 3 and 4 solutions
    - USB 4 64Gbp/s has similar overhead problems to thunderbolt



