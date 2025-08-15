#!/usr/bin/env python3
"""
viz.py – Visual sanity-check of the fixed-point quadratic
         against the float reference.

Input file: test.csv produced by

    ./test.exe > test.csv

Columns expected:
    mv,ref_float,q_fixed_point_float,q_fixed_point_int
"""

import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np
from scipy import stats

CSV = 'test.csv'

def main():
    try:
        # Read the CSV with corrected column names
        df = pd.read_csv(CSV, header=0, names=['mv', 'ref_float', 'q_fixed_point_float', 'q_fixed_point_int'])
    except FileNotFoundError:
        print(f'Error: {CSV} not found. Run "./test.exe > {CSV}" first.')
        sys.exit(1)

    # Compute absolute error in °C
    df['err_abs'] = (df['ref_float'] - df['q_fixed_point_float']).abs()

    # Calculate and print Mean Squared Error (MSE)
    mse = np.mean((df['ref_float'] - df['q_fixed_point_float'])**2)
    print(f'Mean Squared Error (MSE): {mse:.6f}')

    # Perform statistical inference (t-test)
    # This tests the null hypothesis that the mean of the difference
    # between the two samples is equal to 0.
    t_stat, p_value = stats.ttest_rel(df['ref_float'], df['q_fixed_point_float'])
    print(f'Paired t-test results:')
    print(f'  t-statistic: {t_stat:.4f}')
    print(f'  p-value: {p_value:.6f}')
    if p_value < 0.05:
        print('  The difference between the float and fixed-point results is statistically significant.')
    else:
        print('  The difference between the float and fixed-point results is not statistically significant.')

    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot curves
    ax.plot(df['mv'], df['ref_float'],
            label='Float reference', color='tab:blue')
    ax.plot(df['mv'], df['q_fixed_point_float'],
            label='Q fixed-point', color='tab:orange', ls='--')

    # Optional: show rounded integer °C as dots
    ax.scatter(df['mv'], df['q_fixed_point_int'],
               label='Q rounded (°C)', color='tab:green', s=12)

    # cosmetics
    ax.set_xlabel('Input (mV)')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Quadratic polynomial: float vs fixed-point')
    ax.legend()
    ax.grid(True, ls=':')

    # print worst-case error
    worst = df['err_abs'].max()
    print(f'Worst absolute error: {worst:.4f} °C')

    plt.tight_layout()
    plt.show()
    # plt.savefig('viz.png', dpi=150)
    # print('Saved viz.png')

if __name__ == '__main__':
    main()
