# --- Windows + MinGW / MSYS2 makefile -----------------------------
# You can use this makefile on Linux/macOS by changing the TARGET.

CC      = gcc
CFLAGS  = -Wall -Wextra -O2
TARGET  = test.exe
CSV     = test.csv
GEN_PY  = gen.py
VIZ_PY  = viz.py
C_SRC   = test.c temp_calc.c
H_HDR   = temp_calc.h

.PHONY: all clean run plot

# The default target. Builds the executable.
all: $(TARGET)

# The rule to build the executable.
# It depends on all C source files and the header file.
# The `temp_calc.c` and `temp_calc.h` files are intermediate.
$(TARGET): $(C_SRC) $(H_HDR)
	$(CC) $(CFLAGS) -o $@ $(C_SRC)

# This rule tells make that the generated C files depend on the Python script.
# This ensures make will run the generator before compiling the C code.
$(C_SRC) $(H_HDR): $(GEN_PY)
	python $(GEN_PY)

# Runs the compiled program and redirects the output to the CSV file.
# It depends on the executable being built.
run: $(TARGET)
	./$(TARGET) > $(CSV)
	@echo "CSV written to $(CSV)"

# Plots the data from the CSV file using the Python viz script.
# It depends on the CSV file being created first.
plot: $(CSV)
	python $(VIZ_PY)

# The 'clean' rule is executed explicitly to remove only the generated files.
clean:
	rm -f $(TARGET) $(CSV) temp_plot.png temp_calc.c temp_calc.h
