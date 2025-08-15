# Fixed-Point Quadratic Polynomial Analysis
C & Python workflow to generate, compile, run, and analyze a fixed-point quadratic polynomial vs a floating-point reference. Includes visual comparison & statistical error metrics.

## Files
- `gen.py`: Generates `temp_calc.c/.h` from coefficients & scale.
- `temp_calc.c`: Fixed-point (`temp_calc_q`) & float (`temperature_from_voltage_float`) implementations.
- `temp_calc.h`: Prototypes & fixed-point macros.
- `test.c`: Runs both implementations, outputs CSV.
- `viz.py`: Plots results, calculates MSE, performs t-test.
- `Makefile`: Automates generation, build, run, and plotting.

## Usage
```bash
make        # generate & compile
make run    # produce test.csv
make plot   # plot & analyze
make clean  # remove generated files
```

## Requirements
- `gcc`, `python`
- Python libs: `pip install pandas matplotlib numpy scipy`

## Output
- Plot: fixed-point vs floating-point outputs
- Stats: MSE + paired t-test
