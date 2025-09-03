import os

# Define the coefficients and the fixed-point scale.
# You can easily change these variables to generate new code.
# The script will automatically calculate the fixed-point constants.
Q_FRAC = 23
A_FLOAT = 2.347383e-5
B_FLOAT = 1.274251e-2
C_FLOAT = -154.375
TH_LOW_LIMIT_INT8_T = 814
TH_HIGH_LIMIT_INT8_T = 3200


def generate_fixed_point_constants(q_frac, a_float, b_float, c_float):
    """
    Calculates the fixed-point constants from floating-point numbers.
    The result is rounded to the nearest integer.
    """
    q_one = 1 << q_frac
    a_q = int(round(a_float * q_one))
    b_q = int(round(b_float * q_one))
    c_q = int(round(c_float * q_one))
    return q_one, a_q, b_q, c_q

def generate_c_file_content(q_frac, a_float, b_float, c_float, a_q, b_q, c_q):
    """
    Generates the content for the C source file.
    This includes the necessary includes, macros, constants, and functions.
    The fixed-point math has been carefully optimized for ARM Cortex-M0+
    using 64-bit intermediate types to prevent overflow.
    """
    # The comments are formatted to match the user's example style.
    c_content = f"""#include "temp_calc.h"
#include <stdint.h>

/* ---------- coefficients (Q{32-q_frac-1}.{q_frac}) ----------
   A =  {a_float} * 2^{q_frac}  ≈      {a_q}
   B =  {b_float} * 2^{q_frac}  ≈   {b_q}
   C = {c_float} * 2^{q_frac}  ≈ {c_q}
--------------------------------------------*/
static const int32_t A_Q = {a_q};
static const int32_t B_Q = {b_q};
static const int64_t C_Q = {c_q};

#define TH_LOW_LIMIT_INT8_T {TH_LOW_LIMIT_INT8_T}
#define TH_HIGH_LIMIT_INT8_T {TH_HIGH_LIMIT_INT8_T}

/* ---------- fixed-point helpers ---------- */
static inline int32_t q_to_int(int32_t q)
{{
    return (q + (Q_ONE >> 1)) >> Q_FRAC; /* round-to-nearest */
}}

/* ---------- fixed-point quadratic (Corrected) ----------
 * Calculates Y = A*x^2 + B*x + C where coefficients are in Q_FRAC format.
 * Intermediate calculations use int64_t to prevent overflow on Cortex-M0+.
 * The final result is in Q_FRAC format.
 */
int32_t temp_calc_q(int32_t mv)
{{
    // mv is an integer (Qx.0).
    // The coefficients A_Q, B_Q, C_Q are Qy.Q_FRAC.
    
    // Perform multiplications. The results will have extra fractional bits.
    int64_t ax2_term = ((int64_t)A_Q * mv * mv);
    int64_t bx_term = (int64_t)B_Q * mv;
    
    // C_Q is already in Q_FRAC format.
    
    // Sum the terms and perform the final shift to Q_FRAC format.
    return (int32_t)(ax2_term + bx_term + C_Q);
}}

int32_t temp_calc_int(int32_t mv)
{{
    if(mv >= TH_HIGH_LIMIT_INT8_T) return q_to_int(temp_calc_q(TH_HIGH_LIMIT_INT8_T));
    else if (mv <= TH_LOW_LIMIT_INT8_T) return q_to_int(temp_calc_q(TH_LOW_LIMIT_INT8_T));
    else  return q_to_int(temp_calc_q(mv));
}}

/* ---------- floating-point quadratic ---------- */
float temperature_from_voltage_float(float mv)
{{
    return ({A_FLOAT} * mv * mv) + ({B_FLOAT} * mv) + {C_FLOAT};
}}
"""
    return c_content

def generate_h_file_content(q_frac, a_float, b_float, c_float):
    """
    Generates the content for the C header file.
    """
    h_content = f"""#ifndef TEMP_CALC_H
#define TEMP_CALC_H

#include <stdint.h>

/* ---------- fixed-point scale ---------- */
#define Q_FRAC      {q_frac}
#define Q_ONE       (1 << Q_FRAC)

int32_t temp_calc_q(int32_t mv);
int32_t temp_calc_int(int32_t mv);
float temperature_from_voltage_float(float mv);

#endif /* TEMP_CALC_H */
"""
    return h_content

def main():
    q_one, a_q, b_q, c_q = generate_fixed_point_constants(Q_FRAC, A_FLOAT, B_FLOAT, C_FLOAT)

    c_file_content = generate_c_file_content(Q_FRAC, A_FLOAT, B_FLOAT, C_FLOAT, a_q, b_q, c_q)
    h_file_content = generate_h_file_content(Q_FRAC, A_FLOAT, B_FLOAT, C_FLOAT)

    print("Generating temp_calc.c and temp_calc.h...")

    with open("temp_calc.c", "w", encoding='utf-8') as f:
        f.write(c_file_content)
    
    with open("temp_calc.h", "w", encoding='utf-8') as f:
        f.write(h_file_content)

    print("Done! Files saved in the current directory.")

if __name__ == "__main__":
    main()
