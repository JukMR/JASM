
test/binary/smc:     file format elf64-x86-64


Disassembly of section .init:

0000000000001000 <_init>:
    1000:	f3 0f 1e fa          	endbr64
    1004:	48 83 ec 08          	sub    $0x8,%rsp
    1008:	48 8b 05 d9 2f 00 00 	mov    0x2fd9(%rip),%rax        # 3fe8 <__gmon_start__@Base>
    100f:	48 85 c0             	test   %rax,%rax
    1012:	74 02                	je     1016 <_init+0x16>
    1014:	ff d0                	call   *%rax
    1016:	48 83 c4 08          	add    $0x8,%rsp
    101a:	c3                   	ret

Disassembly of section .plt:

0000000000001020 <.plt>:
    1020:	ff 35 8a 2f 00 00    	push   0x2f8a(%rip)        # 3fb0 <_GLOBAL_OFFSET_TABLE_+0x8>
    1026:	f2 ff 25 8b 2f 00 00 	bnd jmp *0x2f8b(%rip)        # 3fb8 <_GLOBAL_OFFSET_TABLE_+0x10>
    102d:	0f 1f 00             	nopl   (%rax)
    1030:	f3 0f 1e fa          	endbr64
    1034:	68 00 00 00 00       	push   $0x0
    1039:	f2 e9 e1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    103f:	90                   	nop
    1040:	f3 0f 1e fa          	endbr64
    1044:	68 01 00 00 00       	push   $0x1
    1049:	f2 e9 d1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    104f:	90                   	nop
    1050:	f3 0f 1e fa          	endbr64
    1054:	68 02 00 00 00       	push   $0x2
    1059:	f2 e9 c1 ff ff ff    	bnd jmp 1020 <_init+0x20>
    105f:	90                   	nop

Disassembly of section .plt.got:

0000000000001060 <__cxa_finalize@plt>:
    1060:	f3 0f 1e fa          	endbr64
    1064:	f2 ff 25 8d 2f 00 00 	bnd jmp *0x2f8d(%rip)        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    106b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

Disassembly of section .plt.sec:

0000000000001070 <__printf_chk@plt>:
    1070:	f3 0f 1e fa          	endbr64
    1074:	f2 ff 25 45 2f 00 00 	bnd jmp *0x2f45(%rip)        # 3fc0 <__printf_chk@GLIBC_2.3.4>
    107b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000001080 <mprotect@plt>:
    1080:	f3 0f 1e fa          	endbr64
    1084:	f2 ff 25 3d 2f 00 00 	bnd jmp *0x2f3d(%rip)        # 3fc8 <mprotect@GLIBC_2.2.5>
    108b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

0000000000001090 <getpagesize@plt>:
    1090:	f3 0f 1e fa          	endbr64
    1094:	f2 ff 25 35 2f 00 00 	bnd jmp *0x2f35(%rip)        # 3fd0 <getpagesize@GLIBC_2.2.5>
    109b:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)

Disassembly of section .text:

00000000000010a0 <main>:
    10a0:	f3 0f 1e fa          	endbr64
    10a4:	48 83 ec 08          	sub    $0x8,%rsp
    10a8:	48 8d 3d 11 01 00 00 	lea    0x111(%rip),%rdi        # 11c0 <n_primes>
    10af:	e8 7c 01 00 00       	call   1230 <change_page_permissions_of_address>
    10b4:	bf 64 00 00 00       	mov    $0x64,%edi
    10b9:	c6 05 39 01 00 00 01 	movb   $0x1,0x139(%rip)        # 11f9 <n_primes+0x39>
    10c0:	e8 fb 00 00 00       	call   11c0 <n_primes>
    10c5:	31 c0                	xor    %eax,%eax
    10c7:	48 83 c4 08          	add    $0x8,%rsp
    10cb:	c3                   	ret
    10cc:	0f 1f 40 00          	nopl   0x0(%rax)

00000000000010d0 <_start>:
    10d0:	f3 0f 1e fa          	endbr64
    10d4:	31 ed                	xor    %ebp,%ebp
    10d6:	49 89 d1             	mov    %rdx,%r9
    10d9:	5e                   	pop    %rsi
    10da:	48 89 e2             	mov    %rsp,%rdx
    10dd:	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
    10e1:	50                   	push   %rax
    10e2:	54                   	push   %rsp
    10e3:	45 31 c0             	xor    %r8d,%r8d
    10e6:	31 c9                	xor    %ecx,%ecx
    10e8:	48 8d 3d b1 ff ff ff 	lea    -0x4f(%rip),%rdi        # 10a0 <main>
    10ef:	ff 15 e3 2e 00 00    	call   *0x2ee3(%rip)        # 3fd8 <__libc_start_main@GLIBC_2.34>
    10f5:	f4                   	hlt
    10f6:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
    10fd:	00 00 00 

0000000000001100 <deregister_tm_clones>:
    1100:	48 8d 3d 09 2f 00 00 	lea    0x2f09(%rip),%rdi        # 4010 <__TMC_END__>
    1107:	48 8d 05 02 2f 00 00 	lea    0x2f02(%rip),%rax        # 4010 <__TMC_END__>
    110e:	48 39 f8             	cmp    %rdi,%rax
    1111:	74 15                	je     1128 <deregister_tm_clones+0x28>
    1113:	48 8b 05 c6 2e 00 00 	mov    0x2ec6(%rip),%rax        # 3fe0 <_ITM_deregisterTMCloneTable@Base>
    111a:	48 85 c0             	test   %rax,%rax
    111d:	74 09                	je     1128 <deregister_tm_clones+0x28>
    111f:	ff e0                	jmp    *%rax
    1121:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
    1128:	c3                   	ret
    1129:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000001130 <register_tm_clones>:
    1130:	48 8d 3d d9 2e 00 00 	lea    0x2ed9(%rip),%rdi        # 4010 <__TMC_END__>
    1137:	48 8d 35 d2 2e 00 00 	lea    0x2ed2(%rip),%rsi        # 4010 <__TMC_END__>
    113e:	48 29 fe             	sub    %rdi,%rsi
    1141:	48 89 f0             	mov    %rsi,%rax
    1144:	48 c1 ee 3f          	shr    $0x3f,%rsi
    1148:	48 c1 f8 03          	sar    $0x3,%rax
    114c:	48 01 c6             	add    %rax,%rsi
    114f:	48 d1 fe             	sar    %rsi
    1152:	74 14                	je     1168 <register_tm_clones+0x38>
    1154:	48 8b 05 95 2e 00 00 	mov    0x2e95(%rip),%rax        # 3ff0 <_ITM_registerTMCloneTable@Base>
    115b:	48 85 c0             	test   %rax,%rax
    115e:	74 08                	je     1168 <register_tm_clones+0x38>
    1160:	ff e0                	jmp    *%rax
    1162:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)
    1168:	c3                   	ret
    1169:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000001170 <__do_global_dtors_aux>:
    1170:	f3 0f 1e fa          	endbr64
    1174:	80 3d 95 2e 00 00 00 	cmpb   $0x0,0x2e95(%rip)        # 4010 <__TMC_END__>
    117b:	75 2b                	jne    11a8 <__do_global_dtors_aux+0x38>
    117d:	55                   	push   %rbp
    117e:	48 83 3d 72 2e 00 00 	cmpq   $0x0,0x2e72(%rip)        # 3ff8 <__cxa_finalize@GLIBC_2.2.5>
    1185:	00 
    1186:	48 89 e5             	mov    %rsp,%rbp
    1189:	74 0c                	je     1197 <__do_global_dtors_aux+0x27>
    118b:	48 8b 3d 76 2e 00 00 	mov    0x2e76(%rip),%rdi        # 4008 <__dso_handle>
    1192:	e8 c9 fe ff ff       	call   1060 <__cxa_finalize@plt>
    1197:	e8 64 ff ff ff       	call   1100 <deregister_tm_clones>
    119c:	c6 05 6d 2e 00 00 01 	movb   $0x1,0x2e6d(%rip)        # 4010 <__TMC_END__>
    11a3:	5d                   	pop    %rbp
    11a4:	c3                   	ret
    11a5:	0f 1f 00             	nopl   (%rax)
    11a8:	c3                   	ret
    11a9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000000000011b0 <frame_dummy>:
    11b0:	f3 0f 1e fa          	endbr64
    11b4:	e9 77 ff ff ff       	jmp    1130 <register_tm_clones>
    11b9:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

00000000000011c0 <n_primes>:
    11c0:	f3 0f 1e fa          	endbr64
    11c4:	41 54                	push   %r12
    11c6:	41 bc 01 00 00 00    	mov    $0x1,%r12d
    11cc:	55                   	push   %rbp
    11cd:	48 8d 2d 30 0e 00 00 	lea    0xe30(%rip),%rbp        # 2004 <_IO_stdin_used+0x4>
    11d4:	53                   	push   %rbx
    11d5:	89 fb                	mov    %edi,%ebx
    11d7:	85 ff                	test   %edi,%edi
    11d9:	7e 42                	jle    121d <n_primes+0x5d>
    11db:	41 83 c4 0c          	add    $0xc,%r12d
    11df:	44 39 e3             	cmp    %r12d,%ebx
    11e2:	7c 39                	jl     121d <n_primes+0x5d>
    11e4:	b9 02 00 00 00       	mov    $0x2,%ecx
    11e9:	eb 0f                	jmp    11fa <n_primes+0x3a>
    11eb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
    11f0:	44 89 e0             	mov    %r12d,%eax
    11f3:	99                   	cltd
    11f4:	f7 f9                	idiv   %ecx
    11f6:	85 d2                	test   %edx,%edx
    11f8:	74 e1                	je     11db <n_primes+0x1b>
    11fa:	83 c1 01             	add    $0x1,%ecx
    11fd:	41 39 cc             	cmp    %ecx,%r12d
    1200:	75 ee                	jne    11f0 <n_primes+0x30>
    1202:	44 89 e2             	mov    %r12d,%edx
    1205:	48 89 ee             	mov    %rbp,%rsi
    1208:	bf 01 00 00 00       	mov    $0x1,%edi
    120d:	31 c0                	xor    %eax,%eax
    120f:	e8 5c fe ff ff       	call   1070 <__printf_chk@plt>
    1214:	41 83 c4 0c          	add    $0xc,%r12d
    1218:	44 39 e3             	cmp    %r12d,%ebx
    121b:	7d c7                	jge    11e4 <n_primes+0x24>
    121d:	5b                   	pop    %rbx
    121e:	5d                   	pop    %rbp
    121f:	41 5c                	pop    %r12
    1221:	c3                   	ret
    1222:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
    1229:	00 00 00 00 
    122d:	0f 1f 00             	nopl   (%rax)

0000000000001230 <change_page_permissions_of_address>:
    1230:	f3 0f 1e fa          	endbr64
    1234:	53                   	push   %rbx
    1235:	48 89 fb             	mov    %rdi,%rbx
    1238:	e8 53 fe ff ff       	call   1090 <getpagesize@plt>
    123d:	31 d2                	xor    %edx,%edx
    123f:	48 63 f0             	movslq %eax,%rsi
    1242:	48 89 d8             	mov    %rbx,%rax
    1245:	48 f7 f6             	div    %rsi
    1248:	48 29 d3             	sub    %rdx,%rbx
    124b:	ba 07 00 00 00       	mov    $0x7,%edx
    1250:	48 89 df             	mov    %rbx,%rdi
    1253:	5b                   	pop    %rbx
    1254:	e9 27 fe ff ff       	jmp    1080 <mprotect@plt>
    1259:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000001260 <is_prime>:
    1260:	f3 0f 1e fa          	endbr64
    1264:	31 c0                	xor    %eax,%eax
    1266:	83 ff 01             	cmp    $0x1,%edi
    1269:	74 37                	je     12a2 <is_prime+0x42>
    126b:	83 ff 02             	cmp    $0x2,%edi
    126e:	7e 20                	jle    1290 <is_prime+0x30>
    1270:	40 f6 c7 01          	test   $0x1,%dil
    1274:	74 2c                	je     12a2 <is_prime+0x42>
    1276:	b9 02 00 00 00       	mov    $0x2,%ecx
    127b:	eb 0c                	jmp    1289 <is_prime+0x29>
    127d:	0f 1f 00             	nopl   (%rax)
    1280:	89 f8                	mov    %edi,%eax
    1282:	99                   	cltd
    1283:	f7 f9                	idiv   %ecx
    1285:	85 d2                	test   %edx,%edx
    1287:	74 17                	je     12a0 <is_prime+0x40>
    1289:	83 c1 01             	add    $0x1,%ecx
    128c:	39 cf                	cmp    %ecx,%edi
    128e:	75 f0                	jne    1280 <is_prime+0x20>
    1290:	b8 01 00 00 00       	mov    $0x1,%eax
    1295:	c3                   	ret
    1296:	66 2e 0f 1f 84 00 00 	cs nopw 0x0(%rax,%rax,1)
    129d:	00 00 00 
    12a0:	31 c0                	xor    %eax,%eax
    12a2:	c3                   	ret

Disassembly of section .fini:

00000000000012a4 <_fini>:
    12a4:	f3 0f 1e fa          	endbr64
    12a8:	48 83 ec 08          	sub    $0x8,%rsp
    12ac:	48 83 c4 08          	add    $0x8,%rsp
    12b0:	c3                   	ret
