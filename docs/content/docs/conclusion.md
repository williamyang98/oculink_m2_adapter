---
title: Conclusion
prev: /docs/results/discussion
weight: 5
---

## DIY or Buy?
### DIY
<table>
  <thead>
    <tr>
      <th style="width: 50%">Advantages</th>
      <th style="width: 50%">Disadvantages</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="vertical-align: text-top">
        <ul>
          <li>Can reach PCIe 3.0 speeds</li>
          <li>Can be designed to fit in any enclosure</li>
          <li>Cheaper per-unit cost</li>
          <li>Can be modified with different connector (MCIO)</li>
        </ul>
      </td>
      <td style="vertical-align: text-top">
        <ul>
          <li>Cannot reach PCIe 4.0 speeds</li>
          <li>Significant performance loss in synthetic benchmarks</li>
          <li>Expensive to manufacture when considering minimum order quantity of PCBs and components and soldering equipment</li>
          <li>Time consuming to manufacture especially including electrical testing</li>
          <li>Unclear if design needs overhaul to reach PCIe 4.0 without having equipment to test circuit at PCIe 4.0 speeds</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

### Buy
<table>
  <thead>
    <tr>
      <th style="width: 50%">Advantages</th>
      <th style="width: 50%">Disadvantages</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="vertical-align: text-top">
        <ul>
          <li>Can reach PCIe 4.0 speeds</li>
          <li>Beats PCIe 3.0 adapters in synthetic benchmarks</li>
          <li>Flexible micro-coax can be bent to fit most scenarios</li>
          <li>Cost is low considering performance and quality of adapter</li>
        </ul>
      </td>
      <td style="vertical-align: text-top">
        <ul>
          <li>Minimum length of adapter is 12cm which might make it too long even with bending</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

### Conclusion
{{< responsive_image key="aliexpress_m2_oculink_pcie4_extension" style="width: 50%" >}}

- **Buying** the Aliexpress M.2 Oculink PCIe 4.0 adapter is the much more sensible option. 
- It works out of the box and requires minimal bending to fit into your enclosure.
- Also comes in a variety of lengths: ```[15cm, 20cm, 25cm, 30cm, 40cm]```.

## Future plans
- Check mini cool edge IO (MCIO) connector: 
    - Has a better official number of insertion cycles.
    - Cables are designed officially for PCIe 4.0 speeds.
- Fix performance problems and see if PCIe 4.0 speeds can be reached.
    - Redesign hatch plane and taper in flexible PCB design.
    - Use a low loss dielectric to reduce dielectric losses at PCIe 4.0 speeds.
    - Use smooth copper foil to reduce skin effect losses.
- Determine if there is a method to cheaply verify performance at PCIe 4.0 speeds.
    - High frequency oscilloscopes (>20GHz) required for PCIe testing are extremely expensive.
    - Most low cost (<$1000) and low frequency (<200MHz) oscilloscopes are not useful for validating PCIe peformance.
