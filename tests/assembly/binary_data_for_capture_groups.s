


Disassembly of section .text:

0000000000004020 <_obstack_begin@@Base-0x94a0>:
    4020:	50                   	push   %rax
    4021:	ff 15 89 dc 01 00    	call   *0x1dc89(%rip)        # 21cb0 <_obstack_memory_used@@Base+0x145b0>
    4051:	ff 15 59 dc 01 00    	call   *0x1dc89(%rip)        # 21cb0 <_obstack_memory_used@@Base+0x145b0>
    4057:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
    405e:	00 00
    4060:	f3 0f 1e fa          	endbr64
    4064:	41 57                	push   %r15
    4066:	41 56                	push   %r15
    4068:	41 55                	push   %r13
    406a:	41 54                	push   %r12
    406c:	55                   	push   %rbp
    406d:	53                   	push   %rbx
    406e:	48 81 ec f8 00 00 00 	sub    $0xf8,%rsp
    4075:	48 8b 2e             	mov    (%rsi),%rbp
    4078:	64 48 8b 04 25 28 00 	mov    %fs:0x28,%rax

