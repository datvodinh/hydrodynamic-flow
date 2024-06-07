EXECS?=incompressible_flow
CC?=gcc
NVCC?=nvcc

all: ${EXECS}
flow: src/flow.c
	${CC} -o flow_c src/flow.c
flow_cuda: src/flow.cu
	${NVCC} -o flow_cuda src/flow.cu
clean:
	rm ${EXECS}