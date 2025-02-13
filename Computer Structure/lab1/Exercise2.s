.data

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


############################################################################################################

exponential:
	# 2 parameters, fa0 (base) and a0 (exponent)
    beq a0 zero exponential_zero # base case where exp = 0
    fmv.s ft0 fa0 # move to temporal float register the base
    li t0 1 # load 1
    
loop_exponential:
    bge t0 a0 exponential_end # if t0>a0 jump to end (counter is greater or equal than the exponent we need)
    fmul.s ft0 ft0 fa0 # ft0 = ft0 * fa0
    addi t0 t0 1 # increase counter by one
    j loop_exponential # repeat
    
exponential_zero:
	li t0 1 # load 1
    fcvt.s.wu fa0 t0 # move to float register of return (by conversion)
    jr ra # return
    
exponential_end:
    fmv.s fa0 ft0 # move to float register of return
    jr ra # return

##############################################################################################

sin:
	# one parameter, x being sin(x) = sin(fa0)
	addi sp sp -48 # allocate memory
    sw ra 0(sp)	# push
    sw s0 4(sp) # push
    sw s1 8(sp) # push
    sw s2 12(sp) # push
    sw s3 16(sp) # push
    sw s4 20(sp) # push
    fsw fs0 24(sp) # push
    fsw fs1 28(sp) # push
    fsw fs2 32(sp) # push
    fsw fs3 36(sp) # push
    fsw fs4 40(sp) # push
    fsw fs5 44(sp) # push
    
sin_checkif0:
    fcvt.s.wu fs0 zero # save a 0 in fs0 (it will be later used as the total of the sum)
    feq.s s0 fa0 fs0 # check if given value is 0
    li s1 1 # save a 1
    beq s0 s1 end_sin # go to end if given value (x) is 0
    
sin_initialization:
	fcvt.s.wu fs1 s1 # load a 1 in fs1 (later used as sign)
    fmv.s fs2 fa0 # save "x" in fs2
    li s0 0 # save "count" in s0 (initially 0)
    li s2 2 # load a 2 in s1
    li s4 0x3a83126f # load 0.001 (temporal)
    fmv.w.x fs5 s4 # load error in fs5
    
sin_loop:
    mul s3 s0 s2 # s3 = 2*n (count)
    add s3 s3 s1 # add 1 (s3 = 2n+1)
    
    mv a0 s3 # load 2n+1
    fmv.s fa0 fs2 # load "x" from fs2 into fa0.
    jal ra exponential # call to exp(x, 2n+1)
    fmv.s fs3 fa0 # save "result" in fs3
    
    mv a0 s3 # load 2n+1
    jal ra factorial # call to factorial(2n+1)
    
    fdiv.s fs3 fs3 fa0 # fs3 = result / factorial
    
    fabs.s fs4 fs3 # absolute value of result (fs3) in fs4
    flt.s s4 fs4 fs5 # save in s4 if abs(result) < error
    beq s4 s1 end_sin # if result < error, jump to end (if 1 == 1(s1))
    
add_term_sin:
	fmul.s fs3 fs3 fs1 # assignation of sign <-> term*(-1)^n
    fadd.s fs0 fs0 fs3 # fs0 = total + this_term
    add s0 s0 s1 # add 1 to count
    fneg.s fs1, fs1 # change sign of the term for next iteration
    j sin_loop # repeat
    
end_sin:
	fmv.s fa0 fs0 # load result into the return address
    flw fs5 44(sp) # pop
    flw fs4 40(sp) # pop
    flw fs3 36(sp) # pop
    flw fs2 32(sp) # pop
    flw fs1 28(sp) # pop
    flw fs0 24(sp) # pop
    lw s4 20(sp) # pop
    lw s3 16(sp) # pop
    lw s2 12(sp) # pop
    lw s1 8(sp) # pop
    lw s0 4(sp) # pop
	lw ra 0(sp) # pop
    addi sp sp 48 # free stack
    jr ra # return

############################################################################################################################################

SinMatrix:
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
    flw fa0 0(s0) # load term of the A matrix into fa0
    jal ra sin # execute sin of the term
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