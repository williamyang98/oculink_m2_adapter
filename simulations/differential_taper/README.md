# Introduction
- Simulates variants of ground taper for differential trace with ground plane transition.
- Refer to schematics in ```kicad/oculink_m2_flex_connector/``` for the final design of taper.

# Instructions
1. Create taper simulation variants.
```bash
python ./generate_tapers.py
```

2. Simulate taper variants.
```bash
python ../run_simulations.py
```

3. Search for optimum taper configuration.
```bash
python ../find_optimum_diffpair.py
```

# Layout
| Filepath | Description |
| --- | --- |
| ```variants_simulation/base``` | Original simulation files |
| ```variants_simulation/variants.csv``` | Stores list of variants |
| ```variants_simulation/variants/*/images/*_debug.png``` | Stores debug images of taper variant |
| ```variants_optimum_diffpair``` | Stores S-parameter and Smith chart plots of taper variants |
