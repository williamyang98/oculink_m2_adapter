---
title: Hatched ground plane
prev: /docs/design/transmission_line/skew_requirements
next: /docs/design/transmission_line/flex_connection
weight: 6
params:
  icon: hashtag
---

## Problems with thin flexible PCB
- The base polyimide dielectric core has a thickness of 25um.
- This means that we need extremely thin traces with a solid ground plane if we want to reach our PCIe impedance target.
- Thicker dielectric cores are provided but they increase cost substantially and trace width barely increases.
- Even worse the calculated transmission line trace width is calculated as 0.05mm which is below JLCPCB's manufacturing minimums.

## Hatched ground plane
- Hatched ground plane can allow for wider traces while matching impedance.
- No easy equation to get impedance measurement (fill factor approximation does not model this adequately).
- Design of hatched ground plane must meet manufacturing capabilities of JLCPCB.
- Requires parametric search with simulation software.
- Refer to this section about simulating circuits with [openEMS]({{< abs_url link="docs/design/open_ems/hatched_ground" >}}).

## Determining parameters
There are three major parameters to consider:
1. Trace width.
2. Hatch width.
3. Hatch gap.

Since we need to be above the minimum trace width for JLCPCB to manufacture it, we should select a fixed trace width of 0.1mm.
- This is similar the trace width of 0.13mm for our transmission line on the FR4 substrate for both the M.2 cad and Oculink port board.
- This means we will have an easier time designing a taper geometry when connecting the flex connector to our boards (discussed [here]({{< abs_url link="docs/design/transmission_line/flex_connection" >}})).
- Means we only need to perform a parametric search with two variables (the hatch width and gap) which is less time consuming.

## Additional design considerations
Refer to minimising [intra-pair skew]({{< abs_url link="docs/design/transmission_line/skew_requirements#hatched-ground-plane" >}}) for hatched ground planes and differential pairs.
