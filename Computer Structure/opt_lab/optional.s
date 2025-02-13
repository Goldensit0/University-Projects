.data
	A: .word 1,2,3,4 # values for matrix A
	B: .word 0,0,0,0 # values for matrix B
	N: .word 2 # Number of rows
	M: .word 2 # Number of columns
    
.text
main:
	addi sp, sp -12
	sw ra, 0(sp)
	sw s0, 4(sp)
	sw s1, 8 (sp)
	
	la a0, A
	la a1, B
	la t0, N
	lw a2, 0(t0)
	la t0, M
	lw a3, 0(t0)
	
	# the function is executed for the first time
	rdcycle s0
	jal ra factorialMatrix
	rdcycle s1
	sub s1 s1 s0
	
	# print the number of cycles (s1)
	
	# the function is executed a second time
	la a0, A
	la a1, B
	la t0, N
	lw a2, 0(t0)
	la t0, M
	lw a3, 0(t0)
	
	rdcycle s0
	jal ra factorialMatrix
	rdcycle s1
	sub s1 s1 s0
	
	# print the number of cycles (s1)
	
	lw ra, 0(sp)
	lw s0, 4(sp)
	lw s1, 8 (sp)
	addi sp, sp 12
	
	jr ra

.text

factorial:
	# one parameter, a0 (the factorial term)
    # first, special case where factorial of 0 is called
	li t0 1 # total
	fcvt.s.wu ft0 t0 # convert 1 to float
	beq a0 zero end_factorial # factorial of zero equals 1
    
    # if not, we run the whole function
    fmv.s ft1 ft0 # load 1 to ft1
    fmv.s ft2 ft0 # load 1 to ft2
    
loop_factorial:
	bge t0 a0 end_factorial # if last multiplied number equals the one of the factorial, we break the loop
	addi t0 t0 1 # increase the counter
    fadd.s ft2 ft2 ft1 # ft2 = ft2 + 1 (increase the term)
    fmul.s ft0 ft0 ft2 # ft0 = ft0 * ft2 (n * n+1)
    
	j loop_factorial # repeat
    
end_factorial:
	fmv.s fa0 ft0 # return value -> fa0 = ft0
	jr ra # return
	
	
	
factorialMatrix:
	# The function recieves 4 parameters: a0 = addressA ; a1 = addressB ; a2 = rows ; a3 = columns
    addi sp sp -16 # allocate memory
    sw ra 0(sp) # push
    sw s0 4(sp) # push
    sw s1 8(sp) # push
    sw s2 12(sp) # push
    
    mv s0 a0 # store value of A address to manipulate it
    mv s1 a1 # store value of B address to manipulate it
    mul s2 a2 a3 # get the total number of terms of the matrix by multipliying (and store it in s2, will be used as a count)

loop_SinMatrix:
    ble s2 zero end_SinMatrix # if count <= zero -> jump to end_SinMatrix
    lw a0 0(s0) # load term of the A matrix into a0
    jal ra factorial # execute sin of the term
    fsw fa0 0(s1) # save result of the sin(term)
    addi s0 s0 4 # move to the next term
    addi s1 s1 4 # move to the next term
    addi s2 s2 -1 # decrease counter
    j loop_SinMatrix # repeat

end_SinMatrix:
	lw s2 12(sp) # pop
    lw s1 8(sp) # pop
    lw s0 4(sp) # pop
    lw ra 0(sp) # pop
    addi sp sp 16 # free memory

	jr ra # return
