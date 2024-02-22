
main.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <s20_quarterround>:
   0:	8b 01                	mov    (%rcx),%eax
   2:	03 07                	add    (%rdi),%eax
   4:	c1 c0 07             	rol    $0x7,%eax
   7:	33 06                	xor    (%rsi),%eax
   9:	89 06                	mov    %eax,(%rsi)
   b:	03 07                	add    (%rdi),%eax
   d:	c1 c0 09             	rol    $0x9,%eax
  10:	33 02                	xor    (%rdx),%eax
  12:	89 02                	mov    %eax,(%rdx)
  14:	03 06                	add    (%rsi),%eax
  16:	c1 c0 0d             	rol    $0xd,%eax
  19:	33 01                	xor    (%rcx),%eax
  1b:	89 01                	mov    %eax,(%rcx)
  1d:	03 02                	add    (%rdx),%eax
  1f:	c1 c8 0e             	ror    $0xe,%eax
  22:	31 07                	xor    %eax,(%rdi)
  24:	c3                   	ret
