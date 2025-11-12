.globl _main
_main:
	pushq %rbp
	movq %rsp, %rbp
	subq $20, %rsp
	movl $12, %r11d
	subl $3, %r11d
	movl %r11d, -4(%rbp)
	movl $9, -8(%rbp)
	movl -4(%rbp), %eax
	cdq
	idivl -8(%rbp)
	movl $1, %r11d
	imull $5, %r11d
	movl %r11d, -12(%rbp)
	movl %eax, %r11d
	addl -12(%rbp), %r11d
	movl %r11d, -16(%rbp)
	movl -16(%rbp), %r10d
	movl %r10d, -20(%rbp)
	movl $24, %eax
	cdq
	idivl -20(%rbp)
	movl %edx, %eax
	movq %rbp, %rsp
	popq %rbp
	ret
