
moonbounce.bin:     file format pei-x86-64


Disassembly of section .text:

00000001800002c0 <.text>:
   18015781b:	c3                   	ret
   18015781c:	c6 00 48             	movb   $0x48,(%rax)
   18015781f:	c7 40 01 89 5c 24 08 	movl   $0x8245c89,0x1(%rax)
   180157826:	48 8b 44 24 08       	mov    0x8(%rsp),%rax
   18015782b:	9c                   	pushf
   18015782c:	53                   	push   %rbx
   18015782d:	51                   	push   %rcx
   18015782e:	52                   	push   %rdx
   18015782f:	41 50                	push   %r8
   180157831:	41 51                	push   %r9
   180157833:	56                   	push   %rsi
   180157834:	57                   	push   %rdi
   180157835:	31 c9                	xor    %ecx,%ecx
   180157837:	ff c1                	inc    %ecx
   180157839:	81 f9 78 88 15 00    	cmp    $0x158878,%ecx
   18015783f:	7f 32                	jg     0x180157873
   180157841:	67 81 3c 08 41 55 48 	cmpl   $0xcb485541,(%eax,%ecx,1)
   180157848:	cb
   180157849:	75 ec                	jne    0x180157837
	...
