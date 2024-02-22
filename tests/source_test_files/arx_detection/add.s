
add.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <add>:
   0:	48 8b 04 d7          	mov    (%rdi,%rdx,8),%rax
   4:	48 01 04 f7          	add    %rax,(%rdi,%rsi,8)
   8:	c3                   	ret
