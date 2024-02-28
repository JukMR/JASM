; Should match the following pattern:

180002e0c:	b8 4d 5a 00 00       	mov    $0x5a4d,%eax
180002e11:	66 39 01             	cmp    %ax,(%rcx)
180002e14:	0f 85 a5 00 00 00    	jne    0x180002ebf
180002e1a:	48 63 41 3c          	movslq 0x3c(%rcx),%rax
180002e1e:	81 3c 08 50 45 00 00 	cmpl   $0x4550,(%rax,%rcx,1)