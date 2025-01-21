---
title: KiCAD & JLCPCB
prev: /docs/design/laptop_measurements
next: /docs/design/single_board
weight: 2
---

## KiCAD
- Open source
- No license required for usage
- Good enough for adapter which is a relatively simple circuit
- Lacks high end simulation capabilities but those aren't necessary
- Can resort to external calculators (JLCPCB and Sierra circuits) and simulation software (openEMS)

## JLCPCB design constraints
- Location of JLCPCB design constraints
- Varies with type of stackup and number of layers (4 layer has smaller minimum sizes)
- Using a FR4 and 4 layer design with lowest cost options using quote page (different from absolute minimums specified in constraints page)

## Importing design constraints into KiCAD
- Design rules checker custom rules file
- DRC can be triggered manually or is run automatically before generating gerber and drill files

## Generating gerber and drill files
- Provided by JLCPCB
- Verify output through gerber viewer program
- Final verification in JLCPCB online gerber viewer in quote page
