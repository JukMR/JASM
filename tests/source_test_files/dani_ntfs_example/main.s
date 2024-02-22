
main.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <fun>:
   0:	31 c0                	xor    %eax,%eax
   2:	80 3f 4e             	cmpb   $0x4e,(%rdi)
   5:	74 09                	je     10 <fun+0x10>
   7:	c3                   	ret
   8:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
   f:	00 
  10:	80 7f 01 54          	cmpb   $0x54,0x1(%rdi)
  14:	75 f1                	jne    7 <fun+0x7>
  16:	80 7f 02 46          	cmpb   $0x46,0x2(%rdi)
  1a:	75 eb                	jne    7 <fun+0x7>
  1c:	31 c0                	xor    %eax,%eax
  1e:	80 7f 03 53          	cmpb   $0x53,0x3(%rdi)
  22:	0f 94 c0             	sete   %al
  25:	c3                   	ret
