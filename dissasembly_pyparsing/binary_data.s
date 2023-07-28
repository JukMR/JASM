    4000:	f3 0f 1e fa          	endbr64
    4004:	48 83 ec 08          	sub    $0x8,%rsp
    4008:	48 8b 05 61 de 01 00 	mov    0x1de61(%rip),%rax        # 21e70 <__gmon_start__@Base>
    400f:	48 85 c0             	test   %rax,%rax
    4012:	74 02                	je     4016 <_obstack_begin@@Base-0x94aa>
    4014:	ff d0                	call   *%rax
    4016:	48 83 c4 08          	add    $0x8,%rsp
    401a:	c3                   	ret
