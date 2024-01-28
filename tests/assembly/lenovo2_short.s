
tests/binary/lenovo2.bin:     file format pei-x86-64
# shorted for clarity
# vulnerable range 44c5 - 44e1

Disassembly of section .text:

0000000000000280 <.text>:

    44ba:	48 8b c8             	mov    %rax,%rcx
    44bd:	48 89 07             	mov    %rax,(%rdi)
    44c0:	48 85 c0             	test   %rax,%rax
    44c3:	74 66                	je     0x452b
    44c5:	48 8b 43 78          	mov    0x78(%rbx),%rax
    44c9:	66 83 78 20 03       	cmpw   $0x3,0x20(%rax)
    44ce:	75 17                	jne    0x44e7
    44d0:	48 8d 59 10          	lea    0x10(%rcx),%rbx
    44d4:	48 83 c1 02          	add    $0x2,%rcx
    44d8:	e8 3b 44 00 00       	call   0x8918
    44dd:	66 c1 c0 08          	rol    $0x8,%ax
    44e1:	66 83 e8 0c          	sub    $0xc,%ax
    44e5:	eb 15                	jmp    0x44fc
    44e7:	48 8d 59 08          	lea    0x8(%rcx),%rbx
    44eb:	48 83 c1 02          	add    $0x2,%rcx
    44ef:	e8 24 44 00 00       	call   0x8918
    44f4:	66 c1 c0 08          	rol    $0x8,%ax