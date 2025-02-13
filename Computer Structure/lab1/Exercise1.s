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

#####################################################################

cos:
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
    
cos_checkif0:
	# A simple check to avoid the loop for the most basic condition
    fmv.w.x fs0 zero # save a 0 in fs0
    feq.s s0 fa0 fs0 # check if given value is 0
    li s1 1 # save a 1
    fcvt.s.wu fs0 s1 # load a 1 into fs0
    beq s0 s1 end_sin # go to end if given value (x) is 0
    
    fcvt.s.wu fs0 zero # save a 0 in fs0 (it will be later used as the total of the sum)
	fcvt.s.wu fs1 s1 # load a 1 in fs1 (later used as sign)
    fmv.s fs2 fa0 # save "x" in fs2
    li s0 0 # save "count" in s0 (initially 0)
    li s2 2 # load a 2 in s1
    li s4 0x3a83126f # load 0.001 (temporal)
    fmv.w.x fs5 s4 # load error in fs5
    
cos_loop:
    mul s3 s0 s2 # s3 = 2*n (count)
    
    mv a0 s3 # load 2n
    fmv.s fa0 fs2 # load "x" from fs2 into fa0.
    jal ra exponential # call to exp(x, 2n)
    fmv.s fs3 fa0 # save "result" in fs3
    
    mv a0 s3 # load 2n
    jal ra factorial # call to factorial(2n)
    
    fdiv.s fs3 fs3 fa0 # fs3 = result / factorial
    
    fabs.s fs4 fs3 # absolute value of result (fs3) in fs4
    flt.s s4 fs4 fs5 # save in s4 if abs(result) < error
    beq s4 s1 end_cos # if result < error, jump to end (if 1 == 1(s1))
    
add_term_cos:
	fmul.s fs3 fs3 fs1 # assignation of sign <-> term*(-1)^n
    fadd.s fs0 fs0 fs3 # fs0 = total + this_term
    add s0 s0 s1 # add 1 to count
    fneg.s fs1, fs1 # change sign of the term for next iteration
    j cos_loop # repeat
    
end_cos:
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
    
###################################################################

E:
	# no parameters
	addi sp sp -32 # allocate memory
    sw ra 0(sp)	# push
    sw s0 4(sp) # push
    sw s1 8(sp) # push
    sw s2 12(sp) # push
    fsw fs0 16(sp) # push
    fsw fs1 20(sp) # push
    fsw fs2 24(sp) # push
    fsw fs3 28(sp) # push
    
    mv s0 zero # s0 = 0 (used as count)
    fcvt.s.wu fs0 zero # fs0 = 0 (total of the sum)
    li s1 1 # load 1 in s1
    fcvt.s.wu fs1 s1 # fs1 = 1
    li s2 0x3a83126f # load 0.001 (temporal)
    fmv.w.x fs2 s2 # load error in fs2
    
e_loop:
	mv a0 s0
    jal ra factorial # factorial of count
    
    fdiv.s fs3 fs1 fa0 # fs3 = 1/factorial(n)
    
    flt.s s2 fs3 fs2 # save in s2 if 1/factorial < error
    beq s2 s1 end_e # if result < error, jump to end
	
    fadd.s fs0 fs0 fs3 # total = total + 1/factorial
    add s0 s0 s1 # add 1 to count
    j e_loop # repeat
    
end_e:
	fmv.s fa0 fs0 # load "total" into return address
    
    flw fs3 28(sp) # pop
	flw fs2 24(sp) # pop
    flw fs1 20(sp) # pop
    flw fs0 16(sp) # pop
    lw s2 12(sp) # pop
    lw s1 8(sp) # pop
    lw s0 4(sp) # pop
	lw ra 0(sp)	# pop
    addi sp sp 32 # restore memory
    jr ra # return

###################################################################################

tg:
	addi sp sp -20 # allocate memory
    sw ra 0(sp) # push
    sw s0 4(sp) # push
    fsw fs0 8(sp) # push
    fsw fs1 12(sp) # push
    fsw fs2 16(sp) # push
    
checkif_pihalf_tg:
    # in order to find if the value given is +pi/2 or -pi/2, we have to substract them and check if the difference is less than the error.
    # if this condition is met, it means that x == pi/2 under our error consideration, therefore cos(x) = 0 and tg(x) is +Inf
    # we also have to check +-3/2 * pi, so we will first compare pi/2 and then this value
    # we only consider this value since its the only value of x in the given interval of evaluation (-2pi , +2pi) that results in cos(x) = 0
    
    li s0 0x3fc90ff9 # load pi/2 in hexadecimal floating point (temporal)
    fmv.w.x fs0 s0 # load pi/2 into float (fs0)
	li s0 0x3a83126f # load error in hexadecimal floating point (0.001) (temporal)
    fmv.w.x fs1 s0 # load error into float (fs1)  
    fabs.s fs2 fa0 # load absolute value of x (tg(x))
    
    fsub.s fs0 fs0 fs2 # fs0 = pi/2 - value of x
    fabs.s fs0 fs0 # abs(fs0)
    flt.s s0 fs1 fs0 # check if value(fs0) > error
    beq s0 zero return_inf_tg # if the value is smaller than the error, s0 will contain a 0 (x = pi/2) and we jump to return_inf_tg.
    
checkif_3pi2_tg: 
    li s0 0x4096cbd1 # load pi * 3/2 in hexadecimal floating point (temporal)
    fmv.w.x fs0 s0 # load pi/2 into float (fs0)
    
	fsub.s fs0 fs0 fs2 # fs0 = pi/2 - value of x
    fabs.s fs0 fs0 # abs(fs0)
    flt.s s0 fs0 fs1 # check if value(fs0) < error
    beq s0 zero tg_operations # if the value is greater than the error, s0 will contain a 0 (x != 3/2 * pi) and we jump to the operations.
    
return_inf_tg:
	li s0 0x7f800000 # hexadecimal for +infinity in floating point
    fmv.w.x fs0 s0 # load into fs0 (used at the end as return value)
    j end_tg # jump to end
    
tg_operations:
	fmv.s fs2 fa0 # load value of x into fs2 to save it
    jal ra sin # execute sin(x)
    
    fmv.s fs1 fa0 # save value of sin(x) in fs1
    fmv.s fa0 fs2 # load value of x
    jal ra cos # execute cos(x)
    
    fdiv.s fs0 fs1 fa0 # fs0 = tg(x) = sin(x) / cos(x)

end_tg:
    fmv.s fa0 fs0 # load tg(x) value into return register
    
    flw fs2 16(sp) # pop
    flw fs1 12(sp) # pop
    flw fs0 8(sp) # pop
    lw s0 4(sp) # pop
    lw ra 0(sp) # pop
    addi sp sp 20 # free memory
    jr ra # return
