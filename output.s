.globl _main
_main:
	pushq %rbp
	movq %rsp, %rbp
	subq $0, %rsp
	movl $100, %eax
	movq %rbp, %rsp
	popq %rbp
	ret
