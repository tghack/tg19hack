	.file	"asmqr.c"
	.text
	.globl	x
	.data
	.align 32
	.type	x, @object
	.size	x, 132
x:
	.long	67
	.long	51
	.long	78
	.long	68
	.long	65
	.long	61
	.long	54
	.long	53
	.long	55
	.long	69
	.long	79
	.long	72
	.long	73
	.long	76
	.long	57
	.long	58
	.long	66
	.long	13
	.long	40
	.long	60
	.long	77
	.long	70
	.long	75
	.long	59
	.long	63
	.long	62
	.long	5
	.long	27
	.long	71
	.long	81
	.long	56
	.long	64
	.long	74
	.globl	y
	.align 4
	.type	y, @object
	.size	y, 4
y:
	.long	35
	.globl	z
	.align 32
	.type	z, @object
	.size	z, 140
z:
	.long	18
	.long	27
	.long	26
	.long	17
	.long	10
	.long	9
	.long	21
	.long	1
	.long	8
	.long	0
	.long	30
	.long	14
	.long	28
	.long	1
	.long	7
	.long	16
	.long	30
	.long	1
	.long	7
	.long	28
	.long	28
	.long	14
	.long	4
	.long	6
	.long	31
	.long	20
	.long	1
	.long	5
	.long	28
	.long	1
	.long	8
	.long	0
	.long	0
	.long	31
	.long	29
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movl	$0, -4(%rbp)
	jmp	.L2
.L3:
	movl	-4(%rbp), %eax
	cltq
	leaq	0(,%rax,4), %rdx
	leaq	z(%rip), %rax
	movl	(%rdx,%rax), %eax
	cltq
	leaq	0(,%rax,4), %rdx
	leaq	x(%rip), %rax
	movl	(%rdx,%rax), %eax
	addl	$44, %eax
	movl	%eax, %edi
	call	putchar@PLT
	addl	$1, -4(%rbp)
.L2:
	movl	y(%rip), %eax
	cmpl	%eax, -4(%rbp)
	jl	.L3
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (GNU) 8.2.1 20181127"
	.section	.note.GNU-stack,"",@progbits
