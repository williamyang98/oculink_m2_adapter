---
title: Calculations
prev: /docs/design/transmission_line/flex_connection
next: /docs/design/open_ems/
weight: 8
params:
  icon: calculator
---

## JLCPCB data
### Soldermask
| Location    | Thickness (mil)    | Thickness (mm) |
| ---         | ---                |    ---         |
| Laminate    | 1.2                | 0.03048        |
| Traces      | 0.6                | 0.01524        |

Dielectric constant = 3.8

### Core dielectric
Dielectric constant = 4.6

- [JLCPCB impedance control stackup information](https://jlcpcb.com/impedance?_t=1727251667361)
- [JLCPCB impedance calculator guide](https://jlcpcb.com/help/article/User-Guide-to-the-JLCPCB-Impedance-Calculator)

### JLC04081H-3313 Stackup
#### Name breakdown
| Part  | Meaning                   |
| ---   | ---                       |
| 04    | 4 layer                   |
| 08    | 8mm thickness             |
| 1     | 1oz outer copper          |
| H     | half (0.5oz) inner copper |
| 3313  | 3133 prepreg              |

#### Stackup information
| Layer          | Material Type | Thickness (mm) |
| ---            | ---           | ---            |
| Trace          | Copper        | 0.035          |
| Prepreg        | 3313x1        | 0.0994         |
| Inner Layer    | Copper        | 0.0152         |
| Core           | Core          | 0.45           |
| Inner Layer    | Copper        | 0.0152         |
| Prepreg        | 3313x1        | 0.0994         |
| Trace          | Copper        | 0.035          |

### Core material properties
Nan Ya Plastics NP-155F (4 to 8 layers)

| Core Thickness (mm)   | εr   |
| ---                   | ---  |
| 0.08                  | 3.99 |
| 0.10                  | 4.36 |
| 0.13                  | 4.17 |
| 0.15                  | 4.36 |
| 0.20                  | 4.36 |
| 0.25                  | 4.23 |
| 0.30                  | 4.41 |
| 0.35                  | 4.36 |
| 0.40                  | 4.36 |
| 0.45                  | 4.36 |
| 0.50                  | 4.48 |
| 0.55                  | 4.41 |
| 0.60                  | 4.36 |
| 0.65                  | 4.36 |
| 0.70                  | 4.53 |
| > 0.70                | 4.43 |

### Prepreg
#### Source 1
| Prepreg Type  |  Resin Content |  Nominal Thickness (mil) | εr   |
| ---           | ---            | ---                      | ---  |
| 7628          | 49%            | 8.6                      | 4.4  |
| 3313 (2313)   | 57%            | 4.2                      | 4.1  |
| 1080          | 67%            | 3.3                      | 3.91 |
| 2116          | 54%            | 4.9                      | 4.16 |

#### Source 2
| Prepreg type  | Dielectric constant   |
| ---           | --------------------- |
| 7628          | 4.6                   |
| 3313          | 4.05                  |
| 2116          | 4.25                  |


### Impedance calculator results
[JLCPCB impedance calculator](https://jlcpcb.com/pcb-impedance-calculator)

| Parameter             | Value |
| ---                   | ---   |
| Layers                | 4     |
| Thickness             | 0.8mm |
| Inner copper weight   | 0.5oz |
| Outer copper weight   | 1.0oz |
| Stackup               | JLC04081H-3313 |

**NOTE**: Core is 0.5mm instead of expected 0.45mm which might reduce accuracy of calculations.

#### Trace thicknesses
| Impedance (Ω) | Type                                      | Config    | Trace width (mm)  | Trace spacing (mm)    | Distance coplanar (mm)    |
| ---           | ---                                       | ---       | ---               | ---                   | ---                       |
| 85            | Coplanar differential pair with ground    | L1-L2     | 0.1549            | 0.15                  | 0.15                      |
| 85            | Coplanar differential pair with ground    | L2-L3-L4  | 0.1334            | 0.15                  | 0.15                      |
| 42.5          | Coplanar single ended with ground         | L1-L2     | 0.1971            | N/A                   | 0.15                      |
| 42.5          | Coplanar single ended with ground         | L2-L3-L4  | 0.1679            | N/A                   | 0.15                      |

## Sierra circuits calculations
[Sierra circuits impedance calculator](https://impedance.app.protoexpress.com/)

### Prepreg dielectric material property
Rigid - FR408HR - Prepreg
| Parameter | Value |
| --- | --- |
| Dielectric thickness | 4.2? |
| Construction | 1x3313-59% |
| Resin content | 59% |

| Frequency (GHz) | Dielectric constant | Dissipation factor |
| ---             | ---                 | ---                |
| 1               | 3.58                | 0.009              |
| 2               | 3.57                | 0.009              |
| 5               | 3.55                | 0.010              |
| 10              | 3.54                | 0.010              |
| 20              | 3.54                | 0.010              |

### Coplanar stripline differential pair with ground plane
[Impedance calculator](https://impedance.app.protoexpress.com/?appid=CPSLDPIMPCAL)

| Parameter                     | Value     |
| ---                           | ---       |
| Configuration                 | L2-L3-L4  |
| L2-L3 dielectric height (mm)  | 0.0994    |
| L2-L3 dielectric constant     | 3.55      |
| L3-L4 dielectric height (mm)  | 0.45      |
| L3-L4 dielectric constant     | 4.4       |
| L3 Trace thickness (mm)       | 0.01524   |
| L3 Trace separation (mm)      | 0.15      |
| Conductor spacing (mm)        | 0.15      |
| Conductor width (mm)          | 0.6       |
| Dielectric covering tracks    | L2-L3     |

| Input parameter   | Input value   | Output parameter  | Output value  |
| ---               | ---           | ---               | ---           |
| Zdiff (Ω)         | 85            | Trace width (mm)  | 0.1372        |
| Trace width (mm)  | 0.1334        | Zdiff (Ω)         | 85.88         |

### Coplanar soldermask coated microstrip differential pair with ground plane
[Impedance calculator](https://impedance.app.protoexpress.com/?appid=CPCTDPIMPCAL)

| Parameter                         | Value     |
| ---                               | ---       |
| Configuration                     | L1-L2     |
| L1-L2 dielectric height (mm)      | 0.0994    |
| L1-L2 dielectric constant         | 3.55      |
| Soldermask substrate height (mm)  | 0.03048   |
| Soldermask trace height (mm)      | 0.01524   |
| Soldermask dielectric constant    | 3.8       |
| Trace thickness (mm)              | 0.035     |
| Trace separation (mm)             | 0.15      |
| Conductor spacing (mm)            | 0.15      |
| Conductor width (mm)              | 0.6       |

| Input parameter   | Input value   | Output parameter  | Output value  |
| ---               | ---           | ---               | ---           |
| Zdiff (Ω)         | 85            | Trace width (mm)  | 0.1676        |
| Trace width (mm)  | 0.1549        | Zdiff (Ω)         | 88.18         |

### Coplanar stripline single ended with ground plane
[Impedance calculator](https://impedance.app.protoexpress.com/?appid=CPSLSEIMPCAL)

| Parameter                     | Value     |
| ---                           | ---       |
| Configuration                 | L2-L3-L4  |
| L2-L3 dielectric height (mm)  | 0.0994    |
| L2-L3 dielectric constant     | 3.55      |
| L3-L4 dielectric height (mm)  | 0.45      |
| L3-L4 dielectric constant     | 4.4       |
| L3 Trace thickness (mm)       | 0.01524   |
| Conductor spacing (mm)        | 0.15      |
| Conductor width (mm)          | 0.6       |
| Dielectric covering tracks    | L2-L3     |

| Input parameter   | Input value   | Output parameter  | Output value  |
| ---               | ---           | ---               | ---           |
| Zdiff (Ω)         | 42.5          | Trace width (mm)  | 0.174         |
| Trace width (mm)  | 0.1679        | Zdiff (Ω)         | 43.27         |

### Coplanar soldermask coated microstrip singled ended with ground plane
[Impedance calculator](https://impedance.app.protoexpress.com/?appid=CPCTSEIMPCAL)

| Parameter                         | Value     |
| ---                               | ---       |
| Configuration                     | L1-L2     |
| L1-L2 dielectric height (mm)      | 0.0994    |
| L1-L2 dielectric constant         | 3.55      |
| Soldermask substrate height (mm)  | 0.03048   |
| Soldermask trace height (mm)      | 0.01524   |
| Soldermask dielectric constant    | 3.8       |
| Trace thickness (mm)              | 0.035     |
| Conductor spacing (mm)            | 0.15      |
| Conductor width (mm)              | 0.6       |

| Input parameter   | Input value   | Output parameter  | Output value  |
| ---               | ---           | ---               | ---           |
| Zdiff (Ω)         | 42.5          | Trace width (mm)  | 0.2           |
| Trace width (mm)  | 0.1971        | Zdiff (Ω)         | 44.5          |
