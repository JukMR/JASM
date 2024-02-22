# Makefile

# Compiler and flags
CC=gcc
CFLAGS=-Wall -O3 -g # -Werror

# Automatically find all .c and .h files in the directory
SRCS=$(wildcard *.c)
HEADERS=$(wildcard *.h)

# Convert the .c filenames to .o
OBJS=$(SRCS:.c=.o)

# Convert the .c filenames to .s for assembly listings
ASMS=$(SRCS:.c=.s)

# Default target to generate the assembly listings for all .c files
all: $(ASMS) $(OBJS)

# Rule to compile .c files to .o files
%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

# Rule to disassemble .o files to .s assembly listings
%.s: %.o
	objdump -d $< > $@

# Prevent Make from automatically deleting any intermediate files
.SECONDARY: $(OBJS)

# Clean the build
clean:
	rm -f $(OBJS) $(ASMS)

.PHONY: all clean
