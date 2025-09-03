# Fixed-Point Quadratic Polynomial Analysis (Temperature Case)
C & Python workflow to generate, compile, run, and analyze a fixed-point quadratic polynomial for temperature calculation from voltage readings, compared against a floating-point reference. Includes visual comparison & statistical error metrics.

This project is designed for cases where temperature is computed from an analog sensor output using a quadratic polynomial. The fixed-point implementation allows running on microcontrollers without floating-point hardware while maintaining accuracy close to the floating-point version.

---

## Files
- `gen.py`: Generates `temp_calc.c/.h` from configurable temperature polynomial coefficients & fixed-point scale.
- `temp_calc.c`: Fixed-point (`temp_calc_q`) & floating-point (`temperature_from_voltage_float`) implementations.
- `temp_calc.h`: Function prototypes & fixed-point macros.
- `test.c`: Runs both implementations over a voltage range, outputs temperatures to CSV.
- `viz.py`: Plots results, calculates Mean Squared Error (MSE), performs paired t-test.
- `Makefile`: Automates generation, build, run, and plotting.

---

## Changing the Coefficients
You can easily modify `gen.py` to use different temperature calibration coefficients or fixed-point scale:

```python
# Define the coefficients and the fixed-point scale.
# You can easily change these variables to generate new code.
# The script will automatically calculate the fixed-point constants.
Q_FRAC   = 24
A_FLOAT  = 2.347383e-5
B_FLOAT  = 1.274251e-2
C_FLOAT  = -154.375
```

After changing values, just run:
```bash
make
```
to regenerate and compile the code.

---

## Usage
```bash
make        # generate & compile
make run    # produce test.csv with temperature data
make plot   # plot & analyze temperature results
make clean  # remove generated files
```

---

## Requirements
- `gcc`, `python3`
- Python libs:
```bash
pip install pandas matplotlib numpy scipy
```

---

## Output
- **Plot**: Fixed-point vs floating-point temperature curves
- **Stats**: Mean Squared Error + paired t-test
