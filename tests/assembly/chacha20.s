
chacha20.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <chacha20_init_context>:
   0:	48 c7 07 00 00 00 00 	movq   $0x0,(%rdi)
   7:	49 89 f8             	mov    %rdi,%r8
   a:	48 8d 7f 08          	lea    0x8(%rdi),%rdi
   e:	31 c0                	xor    %eax,%eax
  10:	48 c7 87 b0 00 00 00 	movq   $0x0,0xb0(%rdi)
  17:	00 00 00 00 
  1b:	49 89 c9             	mov    %rcx,%r9
  1e:	48 83 e7 f8          	and    $0xfffffffffffffff8,%rdi
  22:	4c 89 c1             	mov    %r8,%rcx
  25:	48 29 f9             	sub    %rdi,%rcx
  28:	66 0f 6f 05 00 00 00 	movdqa 0x0(%rip),%xmm0        # 30 <chacha20_init_context+0x30>
  2f:	00 
  30:	81 c1 c0 00 00 00    	add    $0xc0,%ecx
  36:	c1 e9 03             	shr    $0x3,%ecx
  39:	f3 48 ab             	rep stos %rax,%es:(%rdi)
  3c:	4c 89 c8             	mov    %r9,%rax
  3f:	48 c1 e8 20          	shr    $0x20,%rax
  43:	f3 0f 6f 0e          	movdqu (%rsi),%xmm1
  47:	41 0f 11 48 48       	movups %xmm1,0x48(%r8)
  4c:	f3 0f 6f 56 10       	movdqu 0x10(%rsi),%xmm2
  51:	41 0f 11 50 58       	movups %xmm2,0x58(%r8)
  56:	48 8b 0a             	mov    (%rdx),%rcx
  59:	49 89 48 68          	mov    %rcx,0x68(%r8)
  5d:	8b 4a 08             	mov    0x8(%rdx),%ecx
  60:	41 0f 11 80 80 00 00 	movups %xmm0,0x80(%r8)
  67:	00 
  68:	41 89 48 70          	mov    %ecx,0x70(%r8)
  6c:	8b 0e                	mov    (%rsi),%ecx
  6e:	41 89 88 90 00 00 00 	mov    %ecx,0x90(%r8)
  75:	8b 4e 04             	mov    0x4(%rsi),%ecx
  78:	41 89 88 94 00 00 00 	mov    %ecx,0x94(%r8)
  7f:	8b 4e 08             	mov    0x8(%rsi),%ecx
  82:	41 89 88 98 00 00 00 	mov    %ecx,0x98(%r8)
  89:	8b 4e 0c             	mov    0xc(%rsi),%ecx
  8c:	41 89 88 9c 00 00 00 	mov    %ecx,0x9c(%r8)
  93:	8b 4e 10             	mov    0x10(%rsi),%ecx
  96:	41 89 88 a0 00 00 00 	mov    %ecx,0xa0(%r8)
  9d:	8b 4e 14             	mov    0x14(%rsi),%ecx
  a0:	41 89 88 a4 00 00 00 	mov    %ecx,0xa4(%r8)
  a7:	8b 4e 18             	mov    0x18(%rsi),%ecx
  aa:	41 89 88 a8 00 00 00 	mov    %ecx,0xa8(%r8)
  b1:	8b 4e 1c             	mov    0x1c(%rsi),%ecx
  b4:	41 89 88 ac 00 00 00 	mov    %ecx,0xac(%r8)
  bb:	8b 0a                	mov    (%rdx),%ecx
  bd:	41 89 88 b4 00 00 00 	mov    %ecx,0xb4(%r8)
  c4:	8b 4a 04             	mov    0x4(%rdx),%ecx
  c7:	41 89 88 b8 00 00 00 	mov    %ecx,0xb8(%r8)
  ce:	8b 4a 08             	mov    0x8(%rdx),%ecx
  d1:	41 89 88 bc 00 00 00 	mov    %ecx,0xbc(%r8)
  d8:	48 8b 0a             	mov    (%rdx),%rcx
  db:	49 89 48 68          	mov    %rcx,0x68(%r8)
  df:	8b 52 08             	mov    0x8(%rdx),%edx
  e2:	41 03 40 68          	add    0x68(%r8),%eax
  e6:	45 89 88 b0 00 00 00 	mov    %r9d,0xb0(%r8)
  ed:	41 89 50 70          	mov    %edx,0x70(%r8)
  f1:	41 89 80 b4 00 00 00 	mov    %eax,0xb4(%r8)
  f8:	4d 89 48 78          	mov    %r9,0x78(%r8)
  fc:	49 c7 40 40 40 00 00 	movq   $0x40,0x40(%r8)
 103:	00 
 104:	c3                   	ret
 105:	66 66 2e 0f 1f 84 00 	data16 cs nopw 0x0(%rax,%rax,1)
 10c:	00 00 00 00 

0000000000000110 <chacha20_xor>:
 110:	48 85 d2             	test   %rdx,%rdx
 113:	0f 84 9e 03 00 00    	je     4b7 <chacha20_xor+0x3a7>
 119:	41 57                	push   %r15
 11b:	48 01 f2             	add    %rsi,%rdx
 11e:	41 56                	push   %r14
 120:	41 55                	push   %r13
 122:	41 54                	push   %r12
 124:	49 89 fc             	mov    %rdi,%r12
 127:	55                   	push   %rbp
 128:	53                   	push   %rbx
 129:	48 83 ec 78          	sub    $0x78,%rsp
 12d:	48 8b 47 40          	mov    0x40(%rdi),%rax
 131:	48 89 74 24 18       	mov    %rsi,0x18(%rsp)
 136:	48 89 54 24 20       	mov    %rdx,0x20(%rsp)
 13b:	eb 35                	jmp    172 <chacha20_xor+0x62>
 13d:	0f 1f 00             	nopl   (%rax)
 140:	4c 01 e0             	add    %r12,%rax
 143:	48 8b 4c 24 18       	mov    0x18(%rsp),%rcx
 148:	0f b6 00             	movzbl (%rax),%eax
 14b:	48 8b 5c 24 20       	mov    0x20(%rsp),%rbx
 150:	30 01                	xor    %al,(%rcx)
 152:	49 8b 44 24 40       	mov    0x40(%r12),%rax
 157:	48 83 c1 01          	add    $0x1,%rcx
 15b:	48 89 4c 24 18       	mov    %rcx,0x18(%rsp)
 160:	48 83 c0 01          	add    $0x1,%rax
 164:	49 89 44 24 40       	mov    %rax,0x40(%r12)
 169:	48 39 d9             	cmp    %rbx,%rcx
 16c:	0f 84 36 03 00 00    	je     4a8 <chacha20_xor+0x398>
 172:	48 83 f8 3f          	cmp    $0x3f,%rax
 176:	76 c8                	jbe    140 <chacha20_xor+0x30>
 178:	45 8b b4 24 b4 00 00 	mov    0xb4(%r12),%r14d
 17f:	00 
 180:	41 8b 84 24 a8 00 00 	mov    0xa8(%r12),%eax
 187:	00 
 188:	41 8b 94 24 ac 00 00 	mov    0xac(%r12),%edx
 18f:	00 
 190:	45 8b ac 24 80 00 00 	mov    0x80(%r12),%r13d
 197:	00 
 198:	44 89 74 24 28       	mov    %r14d,0x28(%rsp)
 19d:	45 8b b4 24 b8 00 00 	mov    0xb8(%r12),%r14d
 1a4:	00 
 1a5:	45 8b 9c 24 84 00 00 	mov    0x84(%r12),%r11d
 1ac:	00 
 1ad:	45 8b 94 24 88 00 00 	mov    0x88(%r12),%r10d
 1b4:	00 
 1b5:	89 44 24 58          	mov    %eax,0x58(%rsp)
 1b9:	45 8b 84 24 8c 00 00 	mov    0x8c(%r12),%r8d
 1c0:	00 
 1c1:	41 8b ac 24 90 00 00 	mov    0x90(%r12),%ebp
 1c8:	00 
 1c9:	44 89 74 24 2c       	mov    %r14d,0x2c(%rsp)
 1ce:	41 8b 9c 24 94 00 00 	mov    0x94(%r12),%ebx
 1d5:	00 
 1d6:	41 8b b4 24 98 00 00 	mov    0x98(%r12),%esi
 1dd:	00 
 1de:	89 54 24 5c          	mov    %edx,0x5c(%rsp)
 1e2:	45 8b bc 24 9c 00 00 	mov    0x9c(%r12),%r15d
 1e9:	00 
 1ea:	45 8b 8c 24 a0 00 00 	mov    0xa0(%r12),%r9d
 1f1:	00 
 1f2:	44 89 6c 24 30       	mov    %r13d,0x30(%rsp)
 1f7:	41 8b bc 24 a4 00 00 	mov    0xa4(%r12),%edi
 1fe:	00 
 1ff:	41 8b 8c 24 b0 00 00 	mov    0xb0(%r12),%ecx
 206:	00 
 207:	44 89 5c 24 34       	mov    %r11d,0x34(%rsp)
 20c:	45 8b b4 24 bc 00 00 	mov    0xbc(%r12),%r14d
 213:	00 
 214:	44 89 54 24 38       	mov    %r10d,0x38(%rsp)
 219:	44 89 44 24 3c       	mov    %r8d,0x3c(%rsp)
 21e:	89 6c 24 40          	mov    %ebp,0x40(%rsp)
 222:	89 5c 24 44          	mov    %ebx,0x44(%rsp)
 226:	89 74 24 48          	mov    %esi,0x48(%rsp)
 22a:	44 89 7c 24 4c       	mov    %r15d,0x4c(%rsp)
 22f:	44 89 4c 24 50       	mov    %r9d,0x50(%rsp)
 234:	89 7c 24 54          	mov    %edi,0x54(%rsp)
 238:	89 4c 24 60          	mov    %ecx,0x60(%rsp)
 23c:	44 89 74 24 64       	mov    %r14d,0x64(%rsp)
 241:	89 54 24 0c          	mov    %edx,0xc(%rsp)
 245:	8b 54 24 28          	mov    0x28(%rsp),%edx
 249:	c7 44 24 14 0a 00 00 	movl   $0xa,0x14(%rsp)
 250:	00 
 251:	89 44 24 08          	mov    %eax,0x8(%rsp)
 255:	8b 44 24 2c          	mov    0x2c(%rsp),%eax
 259:	4c 89 64 24 68       	mov    %r12,0x68(%rsp)
 25e:	45 89 f4             	mov    %r14d,%r12d
 261:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
 268:	41 01 db             	add    %ebx,%r11d
 26b:	41 01 ed             	add    %ebp,%r13d
 26e:	41 01 f2             	add    %esi,%r10d
 271:	44 31 da             	xor    %r11d,%edx
 274:	44 31 e9             	xor    %r13d,%ecx
 277:	44 31 d0             	xor    %r10d,%eax
 27a:	c1 c2 10             	rol    $0x10,%edx
 27d:	c1 c1 10             	rol    $0x10,%ecx
 280:	01 d7                	add    %edx,%edi
 282:	41 01 c9             	add    %ecx,%r9d
 285:	c1 c0 10             	rol    $0x10,%eax
 288:	31 fb                	xor    %edi,%ebx
 28a:	44 31 cd             	xor    %r9d,%ebp
 28d:	c1 c3 0c             	rol    $0xc,%ebx
 290:	c1 c5 0c             	rol    $0xc,%ebp
 293:	41 01 db             	add    %ebx,%r11d
 296:	41 01 ed             	add    %ebp,%r13d
 299:	44 31 da             	xor    %r11d,%edx
 29c:	44 31 e9             	xor    %r13d,%ecx
 29f:	c1 c2 08             	rol    $0x8,%edx
 2a2:	c1 c1 08             	rol    $0x8,%ecx
 2a5:	44 8d 34 17          	lea    (%rdi,%rdx,1),%r14d
 2a9:	8b 7c 24 08          	mov    0x8(%rsp),%edi
 2ad:	41 01 c9             	add    %ecx,%r9d
 2b0:	44 31 cd             	xor    %r9d,%ebp
 2b3:	44 31 f3             	xor    %r14d,%ebx
 2b6:	c1 c5 07             	rol    $0x7,%ebp
 2b9:	01 c7                	add    %eax,%edi
 2bb:	c1 c3 07             	rol    $0x7,%ebx
 2be:	31 fe                	xor    %edi,%esi
 2c0:	89 6c 24 10          	mov    %ebp,0x10(%rsp)
 2c4:	89 fd                	mov    %edi,%ebp
 2c6:	8b 7c 24 0c          	mov    0xc(%rsp),%edi
 2ca:	c1 c6 0c             	rol    $0xc,%esi
 2cd:	41 01 f2             	add    %esi,%r10d
 2d0:	44 31 d0             	xor    %r10d,%eax
 2d3:	c1 c0 08             	rol    $0x8,%eax
 2d6:	01 c5                	add    %eax,%ebp
 2d8:	45 01 f8             	add    %r15d,%r8d
 2db:	41 01 dd             	add    %ebx,%r13d
 2de:	45 31 c4             	xor    %r8d,%r12d
 2e1:	31 ee                	xor    %ebp,%esi
 2e3:	41 c1 c4 10          	rol    $0x10,%r12d
 2e7:	c1 c6 07             	rol    $0x7,%esi
 2ea:	44 01 e7             	add    %r12d,%edi
 2ed:	41 01 f3             	add    %esi,%r11d
 2f0:	41 31 ff             	xor    %edi,%r15d
 2f3:	44 31 d9             	xor    %r11d,%ecx
 2f6:	41 c1 c7 0c          	rol    $0xc,%r15d
 2fa:	c1 c1 10             	rol    $0x10,%ecx
 2fd:	45 01 f8             	add    %r15d,%r8d
 300:	45 31 c4             	xor    %r8d,%r12d
 303:	41 c1 c4 08          	rol    $0x8,%r12d
 307:	44 01 e7             	add    %r12d,%edi
 30a:	45 31 ec             	xor    %r13d,%r12d
 30d:	41 c1 c4 10          	rol    $0x10,%r12d
 311:	41 31 ff             	xor    %edi,%r15d
 314:	01 cf                	add    %ecx,%edi
 316:	44 01 e5             	add    %r12d,%ebp
 319:	31 fe                	xor    %edi,%esi
 31b:	41 c1 c7 07          	rol    $0x7,%r15d
 31f:	31 eb                	xor    %ebp,%ebx
 321:	c1 c3 0c             	rol    $0xc,%ebx
 324:	41 01 dd             	add    %ebx,%r13d
 327:	45 31 ec             	xor    %r13d,%r12d
 32a:	41 c1 c4 08          	rol    $0x8,%r12d
 32e:	44 01 e5             	add    %r12d,%ebp
 331:	31 eb                	xor    %ebp,%ebx
 333:	89 6c 24 08          	mov    %ebp,0x8(%rsp)
 337:	8b 6c 24 10          	mov    0x10(%rsp),%ebp
 33b:	c1 c3 07             	rol    $0x7,%ebx
 33e:	c1 c6 0c             	rol    $0xc,%esi
 341:	45 01 fa             	add    %r15d,%r10d
 344:	41 01 f3             	add    %esi,%r11d
 347:	41 01 e8             	add    %ebp,%r8d
 34a:	44 31 d2             	xor    %r10d,%edx
 34d:	44 31 d9             	xor    %r11d,%ecx
 350:	44 31 c0             	xor    %r8d,%eax
 353:	c1 c2 10             	rol    $0x10,%edx
 356:	c1 c1 08             	rol    $0x8,%ecx
 359:	c1 c0 10             	rol    $0x10,%eax
 35c:	41 01 d1             	add    %edx,%r9d
 35f:	01 cf                	add    %ecx,%edi
 361:	45 31 cf             	xor    %r9d,%r15d
 364:	31 fe                	xor    %edi,%esi
 366:	89 7c 24 0c          	mov    %edi,0xc(%rsp)
 36a:	41 8d 3c 06          	lea    (%r14,%rax,1),%edi
 36e:	41 c1 c7 0c          	rol    $0xc,%r15d
 372:	31 fd                	xor    %edi,%ebp
 374:	45 01 fa             	add    %r15d,%r10d
 377:	c1 c6 07             	rol    $0x7,%esi
 37a:	c1 c5 0c             	rol    $0xc,%ebp
 37d:	44 31 d2             	xor    %r10d,%edx
 380:	41 01 e8             	add    %ebp,%r8d
 383:	c1 c2 08             	rol    $0x8,%edx
 386:	44 31 c0             	xor    %r8d,%eax
 389:	41 01 d1             	add    %edx,%r9d
 38c:	c1 c0 08             	rol    $0x8,%eax
 38f:	45 31 cf             	xor    %r9d,%r15d
 392:	01 c7                	add    %eax,%edi
 394:	41 c1 c7 07          	rol    $0x7,%r15d
 398:	31 fd                	xor    %edi,%ebp
 39a:	c1 c5 07             	rol    $0x7,%ebp
 39d:	83 6c 24 14 01       	subl   $0x1,0x14(%rsp)
 3a2:	0f 85 c0 fe ff ff    	jne    268 <chacha20_xor+0x158>
 3a8:	89 44 24 10          	mov    %eax,0x10(%rsp)
 3ac:	8b 44 24 30          	mov    0x30(%rsp),%eax
 3b0:	45 89 e6             	mov    %r12d,%r14d
 3b3:	4c 8b 64 24 68       	mov    0x68(%rsp),%r12
 3b8:	41 01 c5             	add    %eax,%r13d
 3bb:	8b 44 24 34          	mov    0x34(%rsp),%eax
 3bf:	45 89 2c 24          	mov    %r13d,(%r12)
 3c3:	41 01 c3             	add    %eax,%r11d
 3c6:	8b 44 24 38          	mov    0x38(%rsp),%eax
 3ca:	45 89 5c 24 04       	mov    %r11d,0x4(%r12)
 3cf:	41 01 c2             	add    %eax,%r10d
 3d2:	8b 44 24 3c          	mov    0x3c(%rsp),%eax
 3d6:	45 89 54 24 08       	mov    %r10d,0x8(%r12)
 3db:	41 01 c0             	add    %eax,%r8d
 3de:	8b 44 24 40          	mov    0x40(%rsp),%eax
 3e2:	45 89 44 24 0c       	mov    %r8d,0xc(%r12)
 3e7:	01 c5                	add    %eax,%ebp
 3e9:	8b 44 24 44          	mov    0x44(%rsp),%eax
 3ed:	41 89 6c 24 10       	mov    %ebp,0x10(%r12)
 3f2:	01 c3                	add    %eax,%ebx
 3f4:	8b 44 24 48          	mov    0x48(%rsp),%eax
 3f8:	41 89 5c 24 14       	mov    %ebx,0x14(%r12)
 3fd:	8b 5c 24 60          	mov    0x60(%rsp),%ebx
 401:	01 c6                	add    %eax,%esi
 403:	8b 44 24 4c          	mov    0x4c(%rsp),%eax
 407:	41 89 74 24 18       	mov    %esi,0x18(%r12)
 40c:	8b 74 24 08          	mov    0x8(%rsp),%esi
 410:	01 d9                	add    %ebx,%ecx
 412:	41 01 c7             	add    %eax,%r15d
 415:	8b 44 24 50          	mov    0x50(%rsp),%eax
 419:	41 89 4c 24 30       	mov    %ecx,0x30(%r12)
 41e:	45 89 7c 24 1c       	mov    %r15d,0x1c(%r12)
 423:	41 01 c1             	add    %eax,%r9d
 426:	8b 44 24 54          	mov    0x54(%rsp),%eax
 42a:	45 89 4c 24 20       	mov    %r9d,0x20(%r12)
 42f:	01 c7                	add    %eax,%edi
 431:	8b 44 24 58          	mov    0x58(%rsp),%eax
 435:	41 89 7c 24 24       	mov    %edi,0x24(%r12)
 43a:	01 c6                	add    %eax,%esi
 43c:	8b 44 24 5c          	mov    0x5c(%rsp),%eax
 440:	41 89 74 24 28       	mov    %esi,0x28(%r12)
 445:	8b 74 24 0c          	mov    0xc(%rsp),%esi
 449:	01 c6                	add    %eax,%esi
 44b:	41 89 74 24 2c       	mov    %esi,0x2c(%r12)
 450:	8b 74 24 28          	mov    0x28(%rsp),%esi
 454:	01 f2                	add    %esi,%edx
 456:	41 89 54 24 34       	mov    %edx,0x34(%r12)
 45b:	8b 44 24 2c          	mov    0x2c(%rsp),%eax
 45f:	8b 54 24 10          	mov    0x10(%rsp),%edx
 463:	01 c2                	add    %eax,%edx
 465:	8b 44 24 64          	mov    0x64(%rsp),%eax
 469:	41 89 54 24 38       	mov    %edx,0x38(%r12)
 46e:	44 01 f0             	add    %r14d,%eax
 471:	41 89 44 24 3c       	mov    %eax,0x3c(%r12)
 476:	8d 43 01             	lea    0x1(%rbx),%eax
 479:	41 89 84 24 b0 00 00 	mov    %eax,0xb0(%r12)
 480:	00 
 481:	85 c0                	test   %eax,%eax
 483:	75 0f                	jne    494 <chacha20_xor+0x384>
 485:	89 f0                	mov    %esi,%eax
 487:	83 c0 01             	add    $0x1,%eax
 48a:	41 89 84 24 b4 00 00 	mov    %eax,0xb4(%r12)
 491:	00 
 492:	74 24                	je     4b8 <chacha20_xor+0x3a8>
 494:	49 c7 44 24 40 00 00 	movq   $0x0,0x40(%r12)
 49b:	00 00 
 49d:	4c 89 e0             	mov    %r12,%rax
 4a0:	e9 9e fc ff ff       	jmp    143 <chacha20_xor+0x33>
 4a5:	0f 1f 00             	nopl   (%rax)
 4a8:	48 83 c4 78          	add    $0x78,%rsp
 4ac:	5b                   	pop    %rbx
 4ad:	5d                   	pop    %rbp
 4ae:	41 5c                	pop    %r12
 4b0:	41 5d                	pop    %r13
 4b2:	41 5e                	pop    %r14
 4b4:	41 5f                	pop    %r15
 4b6:	c3                   	ret
 4b7:	c3                   	ret
 4b8:	48 8d 0d 00 00 00 00 	lea    0x0(%rip),%rcx        # 4bf <chacha20_xor+0x3af>
 4bf:	ba 60 00 00 00       	mov    $0x60,%edx
 4c4:	48 8d 35 00 00 00 00 	lea    0x0(%rip),%rsi        # 4cb <chacha20_xor+0x3bb>
 4cb:	48 8d 3d 00 00 00 00 	lea    0x0(%rip),%rdi        # 4d2 <chacha20_xor+0x3c2>
 4d2:	e8 00 00 00 00       	call   4d7 <chacha20_xor+0x3c7>
