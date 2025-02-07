---
title: Flex connection
prev: /docs/design/transmission_line/hatched_ground_plane
next: /docs/design/transmission_line/calculations
weight: 7
params:
  icon: hashtag
---

## Type of connection
### Flexible flat/printed cable connector
{{< responsive_image key="molex_ffc_fpc_connector" >}}
<table>
  <thead>
    <tr>
      <th style="width: 50%">Advantages</th>
      <th style="width: 50%">Disadvantages</th>
    </tr>
  </thead>
  <tbody style="vertical-align: top">
    <tr>
      <td>
        <ul>
          <li>Flexible connector can be replaced without resoldering the connector.</li>
          <li>Allows for easier installation and removal without danger of damaging flexible connector.</li>
        </ul>
      </td>
      <td>
        <ul>
          <li>Requires designing transmission line to gracefully transition to the connector without a large impedance discontinuity.</li>
          <li>Higher insertion loss compared to soldered connection since contact surface isn't perfect and there will be stubs from the internal connectors. This could hamper high frequency performance.</li>
          <li>Maximum usable frequency before insertion loss is more than 3dB is usually below 20GHz. This is the recommended design frequency for a good eye opening for PCIe 3.0 which has a fundemental frequency of 4GHz.</li>
          <li>Requires reflow soldering the connector which is extremely difficult for a fine pitch connector (0.2mm) without risk of bridging.</li>
          <li>Connectors add a few extra dollars of cost to the bill of materials</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

- {{< pdf_link key="molex_ffc_fpc_datasheet" >}}

### Soldered connection
<table>
  <thead>
    <tr>
      <th style="width: 50%">Advantages</th>
      <th style="width: 50%">Disadvantages</th>
    </tr>
  </thead>
  <tbody style="vertical-align: top">
    <tr>
      <td>
        <ul>
          <li>Allows for more control over the design of the transmission line structure</li>
          <li>Lower insertion loss since connection is soldered. This means no stubs caused by extra internal connector pins or non-ideal/non-uniform contact surface.</li>
          <li>Connector SMD pads can be designed specifically to avoid discontinuities in impedance caused by trace length mismatch, loss of coplanar ground traces or ground plane.</li>
        </ul>
      </td>
      <td>
        <ul>
          <li>Low tolerance for z-height error on pad connections requires soldering the connector very flat to the SMD pads. This may require pressure during the reflow process</li>
          <li>Requires hand positioning of flexible connector onto pads which is extremely difficult since the traces are only 0.1mm. Any pitch error will result in possible bridging or degraded signal integrity</li>
          <li>Flexible pcb is not removable and is permanently connected to the boards. This might make installation or removal more difficult if connector is in a suboptimal location.</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

### Final choice
The **soldered connection** allows closer control over the design of the tranmission line and avoids the downsides of a FFC connector. This should allow us to avoid or mitigate the signal integrity issues that will arise from the use of a FFC connector.

## Structure of transmission line
{{< responsive_image key="sierra_express_coplanar_ground_plane_via_fence_transmission_line" >}}

The following are useful equations to describe the impedance of the transmission line in relation to it's geometry. These will be useful in determining which parameters to adjust if we want to meet our PCIe impedance target. This comes at the cost of lower modularity but is this is an acceptable compromise for higher guarantees of high frequency signal performance.

### Characteristic impedance
Rough equation for a simple transmission line is given by:

{{< mathjax body >}}
Z_0 = \sqrt{\frac{L}{C}}
{{< /mathjax >}}

This is still useful when discussing changes in impedance for a variety of transmission line structures if we discuss them in terms of differing trace inductances and capacitances.

{{< website_link key="university_san_diego_characteristic_impedance" >}}

### Parallel plate capacitors
The capacitance between a simple two plate system is given by:
{{< mathjax body >}}C = \frac{\epsilon_0 A}{d}{{< /mathjax >}}

{{< responsive_image key="parallel_plate_capacitor" >}}

### Wire over plane
The inductance of a wire over a plane can be approximated as:
{{< mathjax body >}}L = \frac{\mu_0 \mu_r d}{2 \pi} cosh^{-1}{\frac{h}{2r}} {{< /mathjax >}}

{{< responsive_image key="wire_plane_inductance" >}}

## Stackup height differences
{{< responsive_image key="jlcpcb_stackup_diagram" >}}

Transitioning our transmission line from an FR4 stackup to a flexible PCB stackup causes the height of the dielectric in the transmission line to significantly decrease.
- Therefore signal trace to ground plane capacitance increases which causes impedance to decrease.
- Mismatch in impedance causes signal reflections and reduced integrity.

### Hatched ground plane
If the transmission line signal traces have the same width, using a suitably designed hatched ground plane will increase the impedance to meet our impedance target. 
- See [designing hatched ground plane](/docs/design/transmission_line/hatched_ground_plane) for more details.
- See [simulating hatched ground plane](/docs/design/open_ems/hatched_ground) for more details.

## Vertical transmission line connection
{{< responsive_image key="jlcpcb_stackup_connection" >}}
Transition from FR4 stackup to flexible PCB involves a vertical solder connection which produces an impedance discontinuity.

- The coplanar ground traces experience some discontinuity when it meets the solder connection due to an increase in the conductor height.
    - Results in an increase in edge coupling area.
    - This increases capacitance and decreases impedance.
- The E-fields between the signal traces and ground planes have to switch layers.
    - Broadside coupling means stronger E-fields and more energy being carried compared to the coplanar ground traces which use edge coupling.
    - Capacitive coupling is greater through a broadside connection since the traces are 0.1mm wide, compared to the edge side coupling which occurs over a 0.012mm or 0.035mm
    - This was verified through an [open EMS simulation]({{< abs_url link="/docs/design/open_ems/" >}}).

### Tapered connection
{{< responsive_image key="flex_pcb_transmission_line_taper" >}}

A taper is a gradual change in the geometry of a transmission line that attempts to maintain consistent impedance value across a geometric transition.
- We use a linear taper to transition the E-field broadside coupling from the ground plane on the M.2 card to the ground plane on the flexible PCB.
- A linear taper is not necessarily the best however it is very simple to design.
    - {{< website_link key="altium_rf_trace_taper" >}}
    - Other taper designs have complex non-linear equations describing their shape which is difficult to import/design using KiCAD.
    - Linear taper just requires the polyline tool in KiCAD.

### Parametric optimisation of taper
To verify the performance of the taper [openEMS]({{< abs_url link="/docs/design/open_ems/taper" >}}) was used.
- Simulated stackup with flex PCB connected to FR4 transmission line as a 3 layer board.
    - Layers were: ```[FR4 ground, signal traces, flex PCB ground]```.
    - The soldered signal traces were approximated as an ideal single trace on a single layer.
    - This was done so that only the E-field transition between the ground planes was relevant for our parametric search.
    - Might not be ideal from a simulation accuracy standpoint as the geometry of the solder connection might impact the impedance match. However representing the solder connection in our simulation setup was difficult so this approximation/assumption was used.
- Parametric search was done on the length, width, and amount of overlap of the linear taper.
- Shape of taper was modified separately on the FR4 stack up and flexible PCB stackup.
- Possible that simulation was not accurate since mesh size is limited and linear taper requires very small simulation grid size to accurately capture the pointy part.

