
rotate.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <rotateLeft32>:
   0:	89 f8                	mov    %edi,%eax
   2:	89 f1                	mov    %esi,%ecx
   4:	d3 c0                	rol    %cl,%eax
   6:	c3                   	ret
