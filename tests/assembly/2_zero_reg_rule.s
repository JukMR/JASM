; Should match the following pattern:


    00:	55 00 00 00          	mov   %rax,0
    04:	00 00 00 00          	mov   %rbx,0

    08:	55 00 00 00          	xor   %rax,%rax
    12:	00 00 00 00          	xor   %rbx,%rbx

    1a:	55 00 00 00          	and   %rax,0
    1e:	00 00 00 00          	and   %rbx,0