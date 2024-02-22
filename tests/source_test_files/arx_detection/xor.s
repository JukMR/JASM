
xor.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <xor>:
   0:	48 8b 04 f7          	mov    (%rdi,%rsi,8),%rax
   4:	48 31 04 d7          	xor    %rax,(%rdi,%rdx,8)
   8:	c3                   	ret
