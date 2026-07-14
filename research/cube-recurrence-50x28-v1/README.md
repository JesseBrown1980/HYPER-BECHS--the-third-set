# Cube recurrence 50×28

This directory executes the next large recurrence floor requested by the operator:

```text
30 first-set Asolaria/Hutter cubes
20 Wolfram open-math cubes

for every eligible cube:
  8 reversible representation paths
  10 black/white Fischer prediction viewpoints
  10 exact persistent White-Room recurrence passes
```

Total requested perspective rows:

```text
50 × 28 = 1,400
```

Read [`PLAN.md`](PLAN.md) for the complete experiment contract. The source runner and aggregate
registry are:

- [`cube_recurrence_50x28.py`](cube_recurrence_50x28.py)
- [`aggregate_cube_recurrence.py`](aggregate_cube_recurrence.py)
- [`.github/workflows/cube-recurrence-50x28.yml`](../../.github/workflows/cube-recurrence-50x28.yml)

Ring A and Ring C are reconstructive and require byte-identical restore. Ring B is a prediction
measurement surface and is not represented as a complete compressed archive.
