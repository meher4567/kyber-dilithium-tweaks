CC=gcc
CFLAGS=-Wall -Wextra -O2

all:
	@echo "Specify a target in kyber/ or dilithium/ to build."

clean:
	find . -type f -name '*.o' -delete
	find . -type f -name '*.out' -delete
	find . -type f -name '*.exe' -delete 