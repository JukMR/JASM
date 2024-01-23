# Add a phony target for all the commands

.PHONY: all make generate_objdump clean

all: clean make generate_objdump

make:
	gcc -g -c -O3 dani_example.c

generate_objdump:
	objdump -d -m att dani_example.o > dani_example.s


clean:
	rm -f *.o