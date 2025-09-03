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

    # Create a figure with two subplots stacked vertically
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    # Plot curves on the top subplot (ax1)
    ax1.plot(df['mv'], df['ref_float'],
             label='Float reference', color='tab:blue')
    ax1.plot(df['mv'], df['q_fixed_point_float'],
             label='Q fixed-point', color='tab:orange', ls='--')
    ax1.scatter(df['mv'], df['q_fixed_point_int'],
                label='Q rounded (°C)', color='tab:green', s=12)

    # Cosmetics for the top subplot
    ax1.set_ylabel('Temperature (°C)')
    ax1.set_title('Quadratic polynomial: float vs fixed-point')
    ax1.legend()
    ax1.grid(True, ls=':')

    # Plot the absolute error on the bottom subplot (ax2)
    ax2.plot(df['mv'], df['err_abs'],
             label='Absolute Error', color='tab:red')

    # Cosmetics for the bottom subplot
    ax2.set_xlabel('Input (mV)')
    ax2.set_ylabel('Absolute Error (°C)')
    ax2.set_title('Absolute Error')
    ax2.grid(True, ls=':')
    ax2.legend()
    ax2.set_ylim(bottom=0)  # Ensure the error plot starts at zero

    # Print worst-case error
    worst = df['err_abs'].max()
    print(f'Worst absolute error: {worst:.4f} °C')

    plt.tight_layout()
    plt.show()
    # plt.savefig('viz.png', dpi=150)
    # print('Saved viz.png')

if __name__ == '__main__':
    main()
