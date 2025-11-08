.globl __main
__main:
	pushq %rbp
	movq %rsp, %rbp
	subq $8, %rsp
	movl $5, -4(%rbp)
	notl -4(%rbp)
	movl -4(%rbp), %r10d
	movl %r10d, -8(%rbp)
	negl -8(%rbp)
	movl -8(%rbp), %eax
	movq %rbp, %rsp
	popq %rbp
	ret
