#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include "temp_calc.h"

int main(void)
{
    // Corrected CSV header to match viz.py
    puts("mv,ref_float,q_fixed_point_float,q_fixed_point_int");

    for (int32_t mv = 1000; mv <= 3000; mv += 10) {
        int32_t t_q = temp_calc_q(mv);
        float   t_f = (float)t_q / (1 << Q_FRAC); // Use Q_FRAC macro from temp_calc.h
        int32_t t_i = temp_calc_int(mv);
        float   ref = temperature_from_voltage_float((float)mv);

        // Corrected printf to output all three calculated values
        printf("%" PRId32 ",%.6f,%.6f,%" PRId32 "\n",
                mv, ref, t_f, t_i);
    }
    return 0;
}
