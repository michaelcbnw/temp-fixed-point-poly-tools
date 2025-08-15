# Fixed-Point Quadratic Polynomial Analysis
C & Python workflow to generate, compile, run, and analyze a fixed-point quadratic polynomial vs a floating-point reference. Includes visual comparison & statistical error metrics.
This project is designed for cases where temperature is computed from an analog sensor output using a quadratic polynomial. The fixed-point implementation allows running on microcontrollers without floating-point hardware while maintaining accuracy close to the floating-point version.

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

