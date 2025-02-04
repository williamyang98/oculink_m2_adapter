# Introduction
- Simulates variants of hatched ground plane for flexible PCB design.
- Refer to ```kicad/oculink_m2_flex_connector/flex_pcb``` for the final design.

# Instructions
1. Create hatched ground plane simulation variants.
```bash
python ./generate_hatches.py
```

2. Simulate hatched ground plane variants.
```bash
python ../run_simulations.py
```

3. Search for optimum hatch plane configuration.
```bash
python ../find_optimum_diffpair.py
```

# Layout
| Filepath | Description |
| --- | --- |
| ```variants_simulation/base``` | Original simulation files |
| ```variants_simulation/variants.csv``` | Stores list of variants |
| ```variants_simulation/variants/*/images/*_debug.png``` | Stores debug images of hatch ground plane variant |
| ```variants_optimum_diffpair``` | Stores S-parameter and Smith chart plots of hatch ground plane variants |
