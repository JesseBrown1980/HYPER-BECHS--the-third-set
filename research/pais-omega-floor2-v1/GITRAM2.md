# Pais Omega Floor Two: GitRAM lane

Floor two, unlocked by operator OP-JESSE 2026-07-15 ("continue to floor two with the
bigger language set"). Contract: `FLOOR2-CONTRACT.hbp` here and
https://github.com/JesseBrown1980/GitRAM/blob/main/docs/FLOOR2-CONTRACT.md

This lane distributes 34 floor-two bodies + one control across isolated GitHub Actions
containers. Each body trains through the unchanged Cartesian schedule (8 reversible
representation lanes x 10 forward/reverse predictor lanes x 10 persistent epochs = 800
cells) — the only changed variable is the alphabet: **BEHCS-1024 (10-bit glyphs), 4x
floor one's byte alphabet**, binding the existing 64 -> 256 -> 1024 ladder.

Inputs are the SEALED floor-one bodies of run 29415341620 (omega `cb8f8e7e...40d2e`),
never the raw PDFs:

- bodies 01-27 (base): the cube's `BEST-TRAINED-CHAIN.poc1`, SHA-matched to the
  floor-one leafrefs and restored byte-exact through the floor-one decoder carried
  inside this trainer ("old decodes new") before any cell trains;
- bodies 28-33 (apex +X/-X/+Y/-Y/+Z/-Z): the 27 final-epoch payloads concatenated in
  the receipted axis order;
- body 34 (Omega junction): timing-free junction rows only (source/archive/chain SHAs;
  leaf hashes and the floor-one omega are excluded from training bytes — LIRIS
  timing-contamination flag, 2026-07-15);
- control: body 01's input at BEHCS-64 (6-bit) — the falsification arm; prediction
  under the contract is that its gain collapses versus the 1024 arm.

LIRIS leaf-preimage law implemented: `elapsed_ms` never enters a leaf hash (it rides a
TIMING row sealed after the leaf), so floor-two leaves and the floor-two Omega are
seat-convergent. The fan-in flattens nested checkpoint layouts and asserts 35/35
BODY_RESUME — it verifies and seals, it does not retrain (the floor-one resume lesson).

Higher floors, live promotion, compression-record claims, and patent-physics
validation remain held.
