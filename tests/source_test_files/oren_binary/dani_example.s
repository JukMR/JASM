
dani_example.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <fun>:
   0:	48 8b 05 00 00 00 00 	mov    0x0(%rip),%rax        # 7 <fun+0x7>
   7:	48 8d 14 7f          	lea    (%rdi,%rdi,2),%rdx
   b:	48 8d 44 90 04       	lea    0x4(%rax,%rdx,4),%rax
  10:	c3                   	ret
