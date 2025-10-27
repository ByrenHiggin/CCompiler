	.globl _main
_main:
	pushq %rbp
	movq %rsp, %rbp
	subq $8, %rsp
	Neg $3 -> tmp.WL2No4Dv
	Not tmp.WL2No4Dv -> tmp.iE7YkGoJ
	mov	tmp.iE7YkGoJ, %eax
	
	movq %rbp, %rsp
	popq %rbp
	ret