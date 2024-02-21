
main.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <xor>:
   0:	48 8b 04 f7          	mov    (%rdi,%rsi,8),%rax
   4:	48 31 04 d7          	xor    %rax,(%rdi,%rdx,8)
   8:	c3                   	ret
   9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000000010 <add>:
  10:	48 8b 04 d7          	mov    (%rdi,%rdx,8),%rax
  14:	48 01 04 f7          	add    %rax,(%rdi,%rsi,8)
  18:	c3                   	ret
  19:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000000020 <fun>:
  20:	48 89 d1             	mov    %rdx,%rcx
  23:	48 8d 14 f7          	lea    (%rdi,%rsi,8),%rdx
  27:	48 8b 02             	mov    (%rdx),%rax
  2a:	48 03 04 cf          	add    (%rdi,%rcx,8),%rax
  2e:	48 89 02             	mov    %rax,(%rdx)
  31:	4a 8d 14 c7          	lea    (%rdi,%r8,8),%rdx
  35:	48 33 02             	xor    (%rdx),%rax
  38:	48 89 02             	mov    %rax,(%rdx)
  3b:	c1 c0 10             	rol    $0x10,%eax
  3e:	c3                   	ret
