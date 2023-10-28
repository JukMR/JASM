
smc:	file format elf64-x86-64

Disassembly of section .init:

0000000000001000 <_init>:
    1000: f3 0f 1e fa                  	endbr64
    1004: 48 83 ec 08                  	subq	$8, %rsp
    1008: 48 8b 05 d9 2f 00 00         	movq	12249(%rip), %rax       # 0x3fe8 <_GLOBAL_OFFSET_TABLE_+0x40>
    100f: 48 85 c0                     	testq	%rax, %rax
    1012: 74 02                        	je	0x1016 <_init+0x16>
    1014: ff d0                        	callq	*%rax
    1016: 48 83 c4 08                  	addq	$8, %rsp
    101a: c3                           	retq

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020: ff 35 8a 2f 00 00            	pushq	12170(%rip)             # 0x3fb0 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026: f2 ff 25 8b 2f 00 00         	repne		jmpq	*12171(%rip)    # 0x3fb8 <_GLOBAL_OFFSET_TABLE_+0x10>
    102d: 0f 1f 00                     	nopl	(%rax)
    1030: f3 0f 1e fa                  	endbr64
    1034: 68 00 00 00 00               	pushq	$0
    1039: f2 e9 e1 ff ff ff            	repne		jmp	0x1020 <.plt>
    103f: 90                           	nop
    1040: f3 0f 1e fa                  	endbr64
    1044: 68 01 00 00 00               	pushq	$1
    1049: f2 e9 d1 ff ff ff            	repne		jmp	0x1020 <.plt>
    104f: 90                           	nop
    1050: f3 0f 1e fa                  	endbr64
    1054: 68 02 00 00 00               	pushq	$2
    1059: f2 e9 c1 ff ff ff            	repne		jmp	0x1020 <.plt>
    105f: 90                           	nop

Disassembly of section .plt.got:

0000000000001060 <.plt.got>:
    1060: f3 0f 1e fa                  	endbr64
    1064: f2 ff 25 8d 2f 00 00         	repne		jmpq	*12173(%rip)    # 0x3ff8 <_GLOBAL_OFFSET_TABLE_+0x50>
    106b: 0f 1f 44 00 00               	nopl	(%rax,%rax)

Disassembly of section .plt.sec:

0000000000001070 <.plt.sec>:
    1070: f3 0f 1e fa                  	endbr64
    1074: f2 ff 25 45 2f 00 00         	repne		jmpq	*12101(%rip)    # 0x3fc0 <_GLOBAL_OFFSET_TABLE_+0x18>
    107b: 0f 1f 44 00 00               	nopl	(%rax,%rax)
    1080: f3 0f 1e fa                  	endbr64
    1084: f2 ff 25 3d 2f 00 00         	repne		jmpq	*12093(%rip)    # 0x3fc8 <_GLOBAL_OFFSET_TABLE_+0x20>
    108b: 0f 1f 44 00 00               	nopl	(%rax,%rax)
    1090: f3 0f 1e fa                  	endbr64
    1094: f2 ff 25 35 2f 00 00         	repne		jmpq	*12085(%rip)    # 0x3fd0 <_GLOBAL_OFFSET_TABLE_+0x28>
    109b: 0f 1f 44 00 00               	nopl	(%rax,%rax)

Disassembly of section .text:

00000000000010a0 <main>:
    10a0: f3 0f 1e fa                  	endbr64
    10a4: 48 83 ec 08                  	subq	$8, %rsp
    10a8: 48 8d 3d 11 01 00 00         	leaq	273(%rip), %rdi         # 0x11c0 <n_primes>
    10af: e8 7c 01 00 00               	callq	0x1230 <change_page_permissions_of_address>
    10b4: bf 64 00 00 00               	movl	$100, %edi
    10b9: c6 05 39 01 00 00 01         	movb	$1, 313(%rip)           # 0x11f9 <n_primes+0x39>
    10c0: e8 fb 00 00 00               	callq	0x11c0 <n_primes>
    10c5: 31 c0                        	xorl	%eax, %eax
    10c7: 48 83 c4 08                  	addq	$8, %rsp
    10cb: c3                           	retq
    10cc: 0f 1f 40 00                  	nopl	(%rax)

00000000000010d0 <_start>:
    10d0: f3 0f 1e fa                  	endbr64
    10d4: 31 ed                        	xorl	%ebp, %ebp
    10d6: 49 89 d1                     	movq	%rdx, %r9
    10d9: 5e                           	popq	%rsi
    10da: 48 89 e2                     	movq	%rsp, %rdx
    10dd: 48 83 e4 f0                  	andq	$-16, %rsp
    10e1: 50                           	pushq	%rax
    10e2: 54                           	pushq	%rsp
    10e3: 45 31 c0                     	xorl	%r8d, %r8d
    10e6: 31 c9                        	xorl	%ecx, %ecx
    10e8: 48 8d 3d b1 ff ff ff         	leaq	-79(%rip), %rdi         # 0x10a0 <main>
    10ef: ff 15 e3 2e 00 00            	callq	*12003(%rip)            # 0x3fd8 <_GLOBAL_OFFSET_TABLE_+0x30>
    10f5: f4                           	hlt
    10f6: 66 2e 0f 1f 84 00 00 00 00 00	nopw	%cs:(%rax,%rax)

0000000000001100 <deregister_tm_clones>:
    1100: 48 8d 3d 09 2f 00 00         	leaq	12041(%rip), %rdi       # 0x4010 <completed.0>
    1107: 48 8d 05 02 2f 00 00         	leaq	12034(%rip), %rax       # 0x4010 <completed.0>
    110e: 48 39 f8                     	cmpq	%rdi, %rax
    1111: 74 15                        	je	0x1128 <deregister_tm_clones+0x28>
    1113: 48 8b 05 c6 2e 00 00         	movq	11974(%rip), %rax       # 0x3fe0 <_GLOBAL_OFFSET_TABLE_+0x38>
    111a: 48 85 c0                     	testq	%rax, %rax
    111d: 74 09                        	je	0x1128 <deregister_tm_clones+0x28>
    111f: ff e0                        	jmpq	*%rax
    1121: 0f 1f 80 00 00 00 00         	nopl	(%rax)
    1128: c3                           	retq
    1129: 0f 1f 80 00 00 00 00         	nopl	(%rax)

0000000000001130 <register_tm_clones>:
    1130: 48 8d 3d d9 2e 00 00         	leaq	11993(%rip), %rdi       # 0x4010 <completed.0>
    1137: 48 8d 35 d2 2e 00 00         	leaq	11986(%rip), %rsi       # 0x4010 <completed.0>
    113e: 48 29 fe                     	subq	%rdi, %rsi
    1141: 48 89 f0                     	movq	%rsi, %rax
    1144: 48 c1 ee 3f                  	shrq	$63, %rsi
    1148: 48 c1 f8 03                  	sarq	$3, %rax
    114c: 48 01 c6                     	addq	%rax, %rsi
    114f: 48 d1 fe                     	sarq	%rsi
    1152: 74 14                        	je	0x1168 <register_tm_clones+0x38>
    1154: 48 8b 05 95 2e 00 00         	movq	11925(%rip), %rax       # 0x3ff0 <_GLOBAL_OFFSET_TABLE_+0x48>
    115b: 48 85 c0                     	testq	%rax, %rax
    115e: 74 08                        	je	0x1168 <register_tm_clones+0x38>
    1160: ff e0                        	jmpq	*%rax
    1162: 66 0f 1f 44 00 00            	nopw	(%rax,%rax)
    1168: c3                           	retq
    1169: 0f 1f 80 00 00 00 00         	nopl	(%rax)

0000000000001170 <__do_global_dtors_aux>:
    1170: f3 0f 1e fa                  	endbr64
    1174: 80 3d 95 2e 00 00 00         	cmpb	$0, 11925(%rip)         # 0x4010 <completed.0>
    117b: 75 2b                        	jne	0x11a8 <__do_global_dtors_aux+0x38>
    117d: 55                           	pushq	%rbp
    117e: 48 83 3d 72 2e 00 00 00      	cmpq	$0, 11890(%rip)         # 0x3ff8 <_GLOBAL_OFFSET_TABLE_+0x50>
    1186: 48 89 e5                     	movq	%rsp, %rbp
    1189: 74 0c                        	je	0x1197 <__do_global_dtors_aux+0x27>
    118b: 48 8b 3d 76 2e 00 00         	movq	11894(%rip), %rdi       # 0x4008 <__dso_handle>
    1192: e8 c9 fe ff ff               	callq	0x1060 <.plt.got>
    1197: e8 64 ff ff ff               	callq	0x1100 <deregister_tm_clones>
    119c: c6 05 6d 2e 00 00 01         	movb	$1, 11885(%rip)         # 0x4010 <completed.0>
    11a3: 5d                           	popq	%rbp
    11a4: c3                           	retq
    11a5: 0f 1f 00                     	nopl	(%rax)
    11a8: c3                           	retq
    11a9: 0f 1f 80 00 00 00 00         	nopl	(%rax)

00000000000011b0 <frame_dummy>:
    11b0: f3 0f 1e fa                  	endbr64
    11b4: e9 77 ff ff ff               	jmp	0x1130 <register_tm_clones>
    11b9: 0f 1f 80 00 00 00 00         	nopl	(%rax)

00000000000011c0 <n_primes>:
    11c0: f3 0f 1e fa                  	endbr64
    11c4: 41 54                        	pushq	%r12
    11c6: 41 bc 01 00 00 00            	movl	$1, %r12d
    11cc: 55                           	pushq	%rbp
    11cd: 48 8d 2d 30 0e 00 00         	leaq	3632(%rip), %rbp        # 0x2004 <_IO_stdin_used+0x4>
    11d4: 53                           	pushq	%rbx
    11d5: 89 fb                        	movl	%edi, %ebx
    11d7: 85 ff                        	testl	%edi, %edi
    11d9: 7e 42                        	jle	0x121d <n_primes+0x5d>
    11db: 41 83 c4 0c                  	addl	$12, %r12d
    11df: 44 39 e3                     	cmpl	%r12d, %ebx
    11e2: 7c 39                        	jl	0x121d <n_primes+0x5d>
    11e4: b9 02 00 00 00               	movl	$2, %ecx
    11e9: eb 0f                        	jmp	0x11fa <n_primes+0x3a>
    11eb: 0f 1f 44 00 00               	nopl	(%rax,%rax)
    11f0: 44 89 e0                     	movl	%r12d, %eax
    11f3: 99                           	cltd
    11f4: f7 f9                        	idivl	%ecx
    11f6: 85 d2                        	testl	%edx, %edx
    11f8: 74 e1                        	je	0x11db <n_primes+0x1b>
    11fa: 83 c1 01                     	addl	$1, %ecx
    11fd: 41 39 cc                     	cmpl	%ecx, %r12d
    1200: 75 ee                        	jne	0x11f0 <n_primes+0x30>
    1202: 44 89 e2                     	movl	%r12d, %edx
    1205: 48 89 ee                     	movq	%rbp, %rsi
    1208: bf 01 00 00 00               	movl	$1, %edi
    120d: 31 c0                        	xorl	%eax, %eax
    120f: e8 5c fe ff ff               	callq	0x1070 <.plt.sec>
    1214: 41 83 c4 0c                  	addl	$12, %r12d
    1218: 44 39 e3                     	cmpl	%r12d, %ebx
    121b: 7d c7                        	jge	0x11e4 <n_primes+0x24>
    121d: 5b                           	popq	%rbx
    121e: 5d                           	popq	%rbp
    121f: 41 5c                        	popq	%r12
    1221: c3                           	retq
    1222: 66 66 2e 0f 1f 84 00 00 00 00 00     	nopw	%cs:(%rax,%rax)
    122d: 0f 1f 00                     	nopl	(%rax)

0000000000001230 <change_page_permissions_of_address>:
    1230: f3 0f 1e fa                  	endbr64
    1234: 53                           	pushq	%rbx
    1235: 48 89 fb                     	movq	%rdi, %rbx
    1238: e8 53 fe ff ff               	callq	0x1090 <.plt.sec+0x20>
    123d: 31 d2                        	xorl	%edx, %edx
    123f: 48 63 f0                     	movslq	%eax, %rsi
    1242: 48 89 d8                     	movq	%rbx, %rax
    1245: 48 f7 f6                     	divq	%rsi
    1248: 48 29 d3                     	subq	%rdx, %rbx
    124b: ba 07 00 00 00               	movl	$7, %edx
    1250: 48 89 df                     	movq	%rbx, %rdi
    1253: 5b                           	popq	%rbx
    1254: e9 27 fe ff ff               	jmp	0x1080 <.plt.sec+0x10>
    1259: 0f 1f 80 00 00 00 00         	nopl	(%rax)

0000000000001260 <is_prime>:
    1260: f3 0f 1e fa                  	endbr64
    1264: 31 c0                        	xorl	%eax, %eax
    1266: 83 ff 01                     	cmpl	$1, %edi
    1269: 74 37                        	je	0x12a2 <is_prime+0x42>
    126b: 83 ff 02                     	cmpl	$2, %edi
    126e: 7e 20                        	jle	0x1290 <is_prime+0x30>
    1270: 40 f6 c7 01                  	testb	$1, %dil
    1274: 74 2c                        	je	0x12a2 <is_prime+0x42>
    1276: b9 02 00 00 00               	movl	$2, %ecx
    127b: eb 0c                        	jmp	0x1289 <is_prime+0x29>
    127d: 0f 1f 00                     	nopl	(%rax)
    1280: 89 f8                        	movl	%edi, %eax
    1282: 99                           	cltd
    1283: f7 f9                        	idivl	%ecx
    1285: 85 d2                        	testl	%edx, %edx
    1287: 74 17                        	je	0x12a0 <is_prime+0x40>
    1289: 83 c1 01                     	addl	$1, %ecx
    128c: 39 cf                        	cmpl	%ecx, %edi
    128e: 75 f0                        	jne	0x1280 <is_prime+0x20>
    1290: b8 01 00 00 00               	movl	$1, %eax
    1295: c3                           	retq
    1296: 66 2e 0f 1f 84 00 00 00 00 00	nopw	%cs:(%rax,%rax)
    12a0: 31 c0                        	xorl	%eax, %eax
    12a2: c3                           	retq

Disassembly of section .fini:

00000000000012a4 <_fini>:
    12a4: f3 0f 1e fa                  	endbr64
    12a8: 48 83 ec 08                  	subq	$8, %rsp
    12ac: 48 83 c4 08                  	addq	$8, %rsp
    12b0: c3                           	retq
