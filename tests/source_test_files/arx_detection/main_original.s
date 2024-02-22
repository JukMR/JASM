
main_original.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <add>:
   0:	48 8b 04 d7          	mov    (%rdi,%rdx,8),%rax
   4:	48 01 04 f7          	add    %rax,(%rdi,%rsi,8)
   8:	c3                   	ret
   9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000000010 <xorAndRotate>:
  10:	48 8d 14 d7          	lea    (%rdi,%rdx,8),%rdx
  14:	48 8b 02             	mov    (%rdx),%rax
  17:	33 04 f7             	xor    (%rdi,%rsi,8),%eax
  1a:	d3 c0                	rol    %cl,%eax
  1c:	48 89 02             	mov    %rax,(%rdx)
  1f:	c3                   	ret

0000000000000020 <fun>:
  20:	48 8d 0c f7          	lea    (%rdi,%rsi,8),%rcx
  24:	48 89 f8             	mov    %rdi,%rax
  27:	48 8b 31             	mov    (%rcx),%rsi
  2a:	48 03 34 d7          	add    (%rdi,%rdx,8),%rsi
  2e:	48 89 31             	mov    %rsi,(%rcx)
  31:	4a 8d 0c c7          	lea    (%rdi,%r8,8),%rcx
  35:	48 89 f2             	mov    %rsi,%rdx
  38:	33 11                	xor    (%rcx),%edx
  3a:	c1 c2 10             	rol    $0x10,%edx
  3d:	89 d7                	mov    %edx,%edi
  3f:	48 89 39             	mov    %rdi,(%rcx)
  42:	c3                   	ret
