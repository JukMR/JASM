; Pattern found in :
;  8c7:	41 c1 c4 10          	rol    $0x10,%r12d
;  8cb:	44 31 e1             	xor    %r12d,%ecx
;  8ce:	44 8d 66 03          	lea    0x3(%rsi),%r12d
;  8d2:	83 c6 04             	add    $0x4,%esi
AesCore.o:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <AesExpandKey>:
   0:	f3 0f 1e fa          	endbr64
   4:	89 f1                	mov    %esi,%ecx
   6:	41 57                	push   %r15
   8:	49 89 fa             	mov    %rdi,%r10
   b:	41 56                	push   %r14
   d:	c1 e9 05             	shr    $0x5,%ecx
  10:	41 55                	push   %r13
  12:	89 c8                	mov    %ecx,%eax
  14:	41 54                	push   %r12
  16:	83 e0 fd             	and    $0xfffffffd,%eax
  19:	55                   	push   %rbp
  1a:	53                   	push   %rbx
  1b:	48 89 54 24 f0       	mov    %rdx,-0x10(%rsp)
  20:	83 f8 04             	cmp    $0x4,%eax
  23:	74 0e                	je     33 <AesExpandKey+0x33>
  25:	b8 01 00 00 00       	mov    $0x1,%eax
  2a:	83 f9 08             	cmp    $0x8,%ecx
  2d:	0f 85 cf 04 00 00    	jne    502 <AesExpandKey+0x502>
  33:	48 8b 44 24 f0       	mov    -0x10(%rsp),%rax
  38:	44 8d 04 8d 1c 00 00 	lea    0x1c(,%rcx,4),%r8d
  3f:	00
  40:	89 08                	mov    %ecx,(%rax)
  42:	48 8d 50 04          	lea    0x4(%rax),%rdx
  46:	85 c9                	test   %ecx,%ecx
  48:	0f 84 7e 02 00 00    	je     2cc <AesExpandKey+0x2cc>
  4e:	48 89 c3             	mov    %rax,%rbx
  51:	4c 29 d0             	sub    %r10,%rax
  54:	48 83 c0 03          	add    $0x3,%rax
  58:	48 83 f8 3e          	cmp    $0x3e,%rax
  5c:	0f 86 ab 04 00 00    	jbe    50d <AesExpandKey+0x50d>
  62:	8d 41 ff             	lea    -0x1(%rcx),%eax
  65:	83 f8 0e             	cmp    $0xe,%eax
  68:	0f 86 9f 04 00 00    	jbe    50d <AesExpandKey+0x50d>
  6e:	c1 ee 09             	shr    $0x9,%esi
  71:	48 89 d0             	mov    %rdx,%rax
  74:	66 0f ef ff          	pxor   %xmm7,%xmm7
  78:	4c 89 d7             	mov    %r10,%rdi
  7b:	44 8d 4e ff          	lea    -0x1(%rsi),%r9d
  7f:	66 0f ef d2          	pxor   %xmm2,%xmm2
  83:	66 44 0f 6f 05 00 00 	movdqa 0x0(%rip),%xmm8        # 8c <AesExpandKey+0x8c>
  8a:	00 00
  8c:	49 c1 e1 06          	shl    $0x6,%r9
  90:	4e 8d 4c 0b 44       	lea    0x44(%rbx,%r9,1),%r9
  95:	0f 1f 00             	nopl   (%rax)
  98:	f3 0f 6f 07          	movdqu (%rdi),%xmm0
  9c:	f3 0f 6f 4f 10       	movdqu 0x10(%rdi),%xmm1
  a1:	66 41 0f 6f f0       	movdqa %xmm8,%xmm6
  a6:	48 83 c0 40          	add    $0x40,%rax
  aa:	f3 0f 6f 5f 10       	movdqu 0x10(%rdi),%xmm3
  af:	f3 0f 6f 67 30       	movdqu 0x30(%rdi),%xmm4
  b4:	48 83 c7 40          	add    $0x40,%rdi
  b8:	66 41 0f db c8       	pand   %xmm8,%xmm1
  bd:	66 41 0f db c0       	pand   %xmm8,%xmm0
  c2:	f3 0f 6f 6f e0       	movdqu -0x20(%rdi),%xmm5
  c7:	66 0f 67 c1          	packuswb %xmm1,%xmm0
  cb:	f3 0f 6f 4f c0       	movdqu -0x40(%rdi),%xmm1
  d0:	66 0f 71 d3 08       	psrlw  $0x8,%xmm3
  d5:	66 41 0f db e0       	pand   %xmm8,%xmm4
  da:	66 0f 71 d5 08       	psrlw  $0x8,%xmm5
  df:	66 0f 71 d1 08       	psrlw  $0x8,%xmm1
  e4:	66 0f 67 cb          	packuswb %xmm3,%xmm1
  e8:	f3 0f 6f 5f e0       	movdqu -0x20(%rdi),%xmm3
  ed:	66 41 0f db d8       	pand   %xmm8,%xmm3
  f2:	66 0f 67 dc          	packuswb %xmm4,%xmm3
  f6:	f3 0f 6f 67 f0       	movdqu -0x10(%rdi),%xmm4
  fb:	66 0f db f3          	pand   %xmm3,%xmm6
  ff:	66 0f 71 d3 08       	psrlw  $0x8,%xmm3
 104:	66 0f 71 d4 08       	psrlw  $0x8,%xmm4
 109:	66 0f 67 ec          	packuswb %xmm4,%xmm5
 10d:	66 41 0f 6f e0       	movdqa %xmm8,%xmm4
 112:	66 0f db e0          	pand   %xmm0,%xmm4
 116:	66 0f 71 d0 08       	psrlw  $0x8,%xmm0
 11b:	66 0f 67 e6          	packuswb %xmm6,%xmm4
 11f:	66 0f 67 c3          	packuswb %xmm3,%xmm0
 123:	66 41 0f 6f f0       	movdqa %xmm8,%xmm6
 128:	66 41 0f 6f d8       	movdqa %xmm8,%xmm3
 12d:	66 0f db f5          	pand   %xmm5,%xmm6
 131:	66 44 0f 6f dc       	movdqa %xmm4,%xmm11
 136:	66 0f db d9          	pand   %xmm1,%xmm3
 13a:	66 0f 71 d5 08       	psrlw  $0x8,%xmm5
 13f:	66 44 0f 60 df       	punpcklbw %xmm7,%xmm11
 144:	66 0f 67 de          	packuswb %xmm6,%xmm3
 148:	66 0f 71 d1 08       	psrlw  $0x8,%xmm1
 14d:	66 0f 6f f0          	movdqa %xmm0,%xmm6
 151:	66 0f 67 cd          	packuswb %xmm5,%xmm1
 155:	66 0f 6f eb          	movdqa %xmm3,%xmm5
 159:	66 45 0f 6f e3       	movdqa %xmm11,%xmm12
 15e:	66 0f 60 ef          	punpcklbw %xmm7,%xmm5
 162:	66 44 0f 6f d1       	movdqa %xmm1,%xmm10
 167:	66 0f 60 f7          	punpcklbw %xmm7,%xmm6
 16b:	66 44 0f 6f cd       	movdqa %xmm5,%xmm9
 170:	66 44 0f 61 e2       	punpcklwd %xmm2,%xmm12
 175:	66 44 0f 60 d7       	punpcklbw %xmm7,%xmm10
 17a:	66 44 0f 61 ca       	punpcklwd %xmm2,%xmm9
 17f:	66 0f 71 f6 08       	psllw  $0x8,%xmm6
 184:	66 0f 69 ea          	punpckhwd %xmm2,%xmm5
 188:	66 41 0f 72 f4 18    	pslld  $0x18,%xmm12
 18e:	66 41 0f 72 f1 10    	pslld  $0x10,%xmm9
 194:	66 44 0f 69 da       	punpckhwd %xmm2,%xmm11
 199:	66 45 0f eb cc       	por    %xmm12,%xmm9
 19e:	66 45 0f 6f ea       	movdqa %xmm10,%xmm13
 1a3:	66 44 0f 6f e6       	movdqa %xmm6,%xmm12
 1a8:	66 0f 72 f5 10       	pslld  $0x10,%xmm5
 1ad:	66 41 0f 72 f3 18    	pslld  $0x18,%xmm11
 1b3:	66 44 0f 69 d2       	punpckhwd %xmm2,%xmm10
 1b8:	66 0f 69 f2          	punpckhwd %xmm2,%xmm6
 1bc:	66 41 0f eb eb       	por    %xmm11,%xmm5
 1c1:	66 0f 68 e7          	punpckhbw %xmm7,%xmm4
 1c5:	66 41 0f eb f2       	por    %xmm10,%xmm6
 1ca:	66 0f 68 df          	punpckhbw %xmm7,%xmm3
 1ce:	66 44 0f 61 ea       	punpcklwd %xmm2,%xmm13
 1d3:	66 0f eb ee          	por    %xmm6,%xmm5
 1d7:	66 44 0f 61 e2       	punpcklwd %xmm2,%xmm12
 1dc:	66 0f 6f f4          	movdqa %xmm4,%xmm6
 1e0:	0f 11 68 d0          	movups %xmm5,-0x30(%rax)
 1e4:	66 0f 6f eb          	movdqa %xmm3,%xmm5
 1e8:	66 0f 68 c7          	punpckhbw %xmm7,%xmm0
 1ec:	66 0f 61 f2          	punpcklwd %xmm2,%xmm6
 1f0:	66 45 0f eb e5       	por    %xmm13,%xmm12
 1f5:	66 0f 61 ea          	punpcklwd %xmm2,%xmm5
 1f9:	66 0f 68 cf          	punpckhbw %xmm7,%xmm1
 1fd:	66 0f 71 f0 08       	psllw  $0x8,%xmm0
 202:	66 45 0f eb cc       	por    %xmm12,%xmm9
 207:	66 0f 69 da          	punpckhwd %xmm2,%xmm3
 20b:	66 0f 72 f6 18       	pslld  $0x18,%xmm6
 210:	66 0f 72 f5 10       	pslld  $0x10,%xmm5
 215:	44 0f 11 48 c0       	movups %xmm9,-0x40(%rax)
 21a:	66 0f 69 e2          	punpckhwd %xmm2,%xmm4
 21e:	66 0f eb ee          	por    %xmm6,%xmm5
 222:	66 44 0f 6f c9       	movdqa %xmm1,%xmm9
 227:	66 0f 6f f0          	movdqa %xmm0,%xmm6
 22b:	66 44 0f 61 ca       	punpcklwd %xmm2,%xmm9
 230:	66 0f 61 f2          	punpcklwd %xmm2,%xmm6
 234:	66 0f 69 ca          	punpckhwd %xmm2,%xmm1
 238:	66 0f 72 f3 10       	pslld  $0x10,%xmm3
 23d:	66 0f 72 f4 18       	pslld  $0x18,%xmm4
 242:	66 0f 69 c2          	punpckhwd %xmm2,%xmm0
 246:	66 41 0f eb f1       	por    %xmm9,%xmm6
 24b:	66 0f eb dc          	por    %xmm4,%xmm3
 24f:	66 0f eb c1          	por    %xmm1,%xmm0
 253:	66 0f eb ee          	por    %xmm6,%xmm5
 257:	66 0f eb c3          	por    %xmm3,%xmm0
 25b:	0f 11 68 e0          	movups %xmm5,-0x20(%rax)
 25f:	0f 11 40 f0          	movups %xmm0,-0x10(%rax)
 263:	49 39 c1             	cmp    %rax,%r9
 266:	0f 85 2c fe ff ff    	jne    98 <AesExpandKey+0x98>
 26c:	41 89 f1             	mov    %esi,%r9d
 26f:	c1 e6 06             	shl    $0x6,%esi
 272:	41 c1 e1 04          	shl    $0x4,%r9d
 276:	44 39 c9             	cmp    %r9d,%ecx
 279:	74 48                	je     2c3 <AesExpandKey+0x2c3>
 27b:	48 8b 5c 24 f0       	mov    -0x10(%rsp),%rbx
 280:	41 8d 41 01          	lea    0x1(%r9),%eax
 284:	4c 01 d6             	add    %r10,%rsi
 287:	49 89 c1             	mov    %rax,%r9
 28a:	4c 8d 14 83          	lea    (%rbx,%rax,4),%r10
 28e:	eb 04                	jmp    294 <AesExpandKey+0x294>
 290:	41 83 c1 01          	add    $0x1,%r9d
 294:	0f b6 46 01          	movzbl 0x1(%rsi),%eax
 298:	0f b6 3e             	movzbl (%rsi),%edi
 29b:	49 83 c2 04          	add    $0x4,%r10
 29f:	48 83 c6 04          	add    $0x4,%rsi
 2a3:	c1 e7 18             	shl    $0x18,%edi
 2a6:	c1 e0 10             	shl    $0x10,%eax
 2a9:	09 f8                	or     %edi,%eax
 2ab:	0f b6 7e ff          	movzbl -0x1(%rsi),%edi
 2af:	09 f8                	or     %edi,%eax
 2b1:	0f b6 7e fe          	movzbl -0x2(%rsi),%edi
 2b5:	c1 e7 08             	shl    $0x8,%edi
 2b8:	09 f8                	or     %edi,%eax
 2ba:	41 89 42 fc          	mov    %eax,-0x4(%r10)
 2be:	44 39 c9             	cmp    %r9d,%ecx
 2c1:	77 cd                	ja     290 <AesExpandKey+0x290>
 2c3:	44 39 c1             	cmp    %r8d,%ecx
 2c6:	0f 83 34 02 00 00    	jae    500 <AesExpandKey+0x500>
 2cc:	44 8d 61 04          	lea    0x4(%rcx),%r12d
 2d0:	8d 71 03             	lea    0x3(%rcx),%esi
 2d3:	41 ba 04 00 00 00    	mov    $0x4,%r10d
 2d9:	41 89 c9             	mov    %ecx,%r9d
 2dc:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 2e3 <AesExpandKey+0x2e3>
 2e3:	44 8d 79 05          	lea    0x5(%rcx),%r15d
 2e7:	48 89 44 24 e0       	mov    %rax,-0x20(%rsp)
 2ec:	8d 69 01             	lea    0x1(%rcx),%ebp
 2ef:	44 8d 69 02          	lea    0x2(%rcx),%r13d
 2f3:	4c 8d 1d 00 00 00 00 	lea    0x0(%rip),%r11        # 2fa <AesExpandKey+0x2fa>
 2fa:	e9 a3 00 00 00       	jmp    3a2 <AesExpandKey+0x3a2>
 2ff:	90                   	nop
 300:	83 f9 01             	cmp    $0x1,%ecx
 303:	76 7a                	jbe    37f <AesExpandKey+0x37f>
 305:	41 39 e8             	cmp    %ebp,%r8d
 308:	76 75                	jbe    37f <AesExpandKey+0x37f>
 30a:	48 8b 7c 24 e8       	mov    -0x18(%rsp),%rdi
 30f:	48 8b 5c 24 f0       	mov    -0x10(%rsp),%rbx
 314:	41 8d 42 fd          	lea    -0x3(%r10),%eax
 318:	8b 04 82             	mov    (%rdx,%rax,4),%eax
 31b:	33 44 3b 04          	xor    0x4(%rbx,%rdi,1),%eax
 31f:	89 ef                	mov    %ebp,%edi
 321:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 324:	83 f9 02             	cmp    $0x2,%ecx
 327:	74 56                	je     37f <AesExpandKey+0x37f>
 329:	45 39 e8             	cmp    %r13d,%r8d
 32c:	76 51                	jbe    37f <AesExpandKey+0x37f>
 32e:	41 8d 7a fe          	lea    -0x2(%r10),%edi
 332:	33 04 ba             	xor    (%rdx,%rdi,4),%eax
 335:	44 89 ef             	mov    %r13d,%edi
 338:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 33b:	83 f9 03             	cmp    $0x3,%ecx
 33e:	74 3f                	je     37f <AesExpandKey+0x37f>
 340:	44 39 c6             	cmp    %r8d,%esi
 343:	73 3a                	jae    37f <AesExpandKey+0x37f>
 345:	41 8d 7a ff          	lea    -0x1(%r10),%edi
 349:	33 04 ba             	xor    (%rdx,%rdi,4),%eax
 34c:	89 f7                	mov    %esi,%edi
 34e:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 351:	83 f9 04             	cmp    $0x4,%ecx
 354:	74 29                	je     37f <AesExpandKey+0x37f>
 356:	45 39 c4             	cmp    %r8d,%r12d
 359:	73 24                	jae    37f <AesExpandKey+0x37f>
 35b:	44 89 d7             	mov    %r10d,%edi
 35e:	33 04 ba             	xor    (%rdx,%rdi,4),%eax
 361:	44 89 e7             	mov    %r12d,%edi
 364:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 367:	83 f9 06             	cmp    $0x6,%ecx
 36a:	75 13                	jne    37f <AesExpandKey+0x37f>
 36c:	45 39 c7             	cmp    %r8d,%r15d
 36f:	73 0e                	jae    37f <AesExpandKey+0x37f>
 371:	45 8d 4a 01          	lea    0x1(%r10),%r9d
 375:	44 89 ff             	mov    %r15d,%edi
 378:	42 33 04 8a          	xor    (%rdx,%r9,4),%eax
 37c:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 37f:	01 ce                	add    %ecx,%esi
 381:	48 83 44 24 e0 04    	addq   $0x4,-0x20(%rsp)
 387:	41 01 cc             	add    %ecx,%r12d
 38a:	41 01 cf             	add    %ecx,%r15d
 38d:	44 8d 4e fd          	lea    -0x3(%rsi),%r9d
 391:	41 01 ca             	add    %ecx,%r10d
 394:	01 cd                	add    %ecx,%ebp
 396:	41 01 cd             	add    %ecx,%r13d
 399:	45 39 c8             	cmp    %r9d,%r8d
 39c:	0f 86 5e 01 00 00    	jbe    500 <AesExpandKey+0x500>
 3a2:	8d 46 fc             	lea    -0x4(%rsi),%eax
 3a5:	4c 8d 34 82          	lea    (%rdx,%rax,4),%r14
 3a9:	4a 8d 04 8d 00 00 00 	lea    0x0(,%r9,4),%rax
 3b0:	00
 3b1:	48 89 44 24 e8       	mov    %rax,-0x18(%rsp)
 3b6:	41 8d 42 fc          	lea    -0x4(%r10),%eax
 3ba:	41 8b 1e             	mov    (%r14),%ebx
 3bd:	8b 3c 82             	mov    (%rdx,%rax,4),%edi
 3c0:	48 8b 44 24 e0       	mov    -0x20(%rsp),%rax
 3c5:	33 38                	xor    (%rax),%edi
 3c7:	0f b6 c3             	movzbl %bl,%eax
 3ca:	41 8b 04 83          	mov    (%r11,%rax,4),%eax
 3ce:	25 00 ff 00 00       	and    $0xff00,%eax
 3d3:	31 c7                	xor    %eax,%edi
 3d5:	89 d8                	mov    %ebx,%eax
 3d7:	c1 e8 18             	shr    $0x18,%eax
 3da:	41 8b 04 83          	mov    (%r11,%rax,4),%eax
 3de:	c1 c8 08             	ror    $0x8,%eax
 3e1:	0f b6 c0             	movzbl %al,%eax
 3e4:	31 c7                	xor    %eax,%edi
 3e6:	89 d8                	mov    %ebx,%eax
 3e8:	0f b6 df             	movzbl %bh,%ebx
 3eb:	c1 e8 10             	shr    $0x10,%eax
 3ee:	89 db                	mov    %ebx,%ebx
 3f0:	0f b6 c0             	movzbl %al,%eax
 3f3:	41 8b 04 83          	mov    (%r11,%rax,4),%eax
 3f7:	c1 c0 10             	rol    $0x10,%eax
 3fa:	25 00 00 00 ff       	and    $0xff000000,%eax
 3ff:	31 f8                	xor    %edi,%eax
 401:	41 8b 3c 9b          	mov    (%r11,%rbx,4),%edi
 405:	c1 c7 08             	rol    $0x8,%edi
 408:	81 e7 00 00 ff 00    	and    $0xff0000,%edi
 40e:	31 f8                	xor    %edi,%eax
 410:	42 89 04 8a          	mov    %eax,(%rdx,%r9,4)
 414:	83 f9 06             	cmp    $0x6,%ecx
 417:	0f 86 e3 fe ff ff    	jbe    300 <AesExpandKey+0x300>
 41d:	41 39 e8             	cmp    %ebp,%r8d
 420:	76 2e                	jbe    450 <AesExpandKey+0x450>
 422:	8d 7e f6             	lea    -0xa(%rsi),%edi
 425:	33 04 ba             	xor    (%rdx,%rdi,4),%eax
 428:	89 ef                	mov    %ebp,%edi
 42a:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 42d:	45 39 e8             	cmp    %r13d,%r8d
 430:	76 1e                	jbe    450 <AesExpandKey+0x450>
 432:	8d 7e f7             	lea    -0x9(%rsi),%edi
 435:	33 04 ba             	xor    (%rdx,%rdi,4),%eax
 438:	44 89 ef             	mov    %r13d,%edi
 43b:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 43e:	44 39 c6             	cmp    %r8d,%esi
 441:	73 0d                	jae    450 <AesExpandKey+0x450>
 443:	44 8d 4e f8          	lea    -0x8(%rsi),%r9d
 447:	89 f7                	mov    %esi,%edi
 449:	42 33 04 8a          	xor    (%rdx,%r9,4),%eax
 44d:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 450:	45 39 c4             	cmp    %r8d,%r12d
 453:	73 5d                	jae    4b2 <AesExpandKey+0x4b2>
 455:	89 f0                	mov    %esi,%eax
 457:	44 89 d7             	mov    %r10d,%edi
 45a:	8b 1c 82             	mov    (%rdx,%rax,4),%ebx
 45d:	0f b6 c3             	movzbl %bl,%eax
 460:	41 8b 04 83          	mov    (%r11,%rax,4),%eax
 464:	c1 c8 08             	ror    $0x8,%eax
 467:	0f b6 c0             	movzbl %al,%eax
 46a:	33 04 ba             	xor    (%rdx,%rdi,4),%eax
 46d:	89 df                	mov    %ebx,%edi
 46f:	c1 ef 10             	shr    $0x10,%edi
 472:	40 0f b6 ff          	movzbl %dil,%edi
 476:	41 8b 3c bb          	mov    (%r11,%rdi,4),%edi
 47a:	c1 c7 08             	rol    $0x8,%edi
 47d:	81 e7 00 00 ff 00    	and    $0xff0000,%edi
 483:	31 f8                	xor    %edi,%eax
 485:	89 df                	mov    %ebx,%edi
 487:	0f b6 df             	movzbl %bh,%ebx
 48a:	c1 ef 18             	shr    $0x18,%edi
 48d:	89 db                	mov    %ebx,%ebx
 48f:	41 8b 3c bb          	mov    (%r11,%rdi,4),%edi
 493:	45 8b 0c 9b          	mov    (%r11,%rbx,4),%r9d
 497:	44 89 e3             	mov    %r12d,%ebx
 49a:	c1 c7 10             	rol    $0x10,%edi
 49d:	41 81 e1 00 ff 00 00 	and    $0xff00,%r9d
 4a4:	81 e7 00 00 00 ff    	and    $0xff000000,%edi
 4aa:	44 09 cf             	or     %r9d,%edi
 4ad:	31 f8                	xor    %edi,%eax
 4af:	89 04 9a             	mov    %eax,(%rdx,%rbx,4)
 4b2:	45 39 c7             	cmp    %r8d,%r15d
 4b5:	0f 83 c4 fe ff ff    	jae    37f <AesExpandKey+0x37f>
 4bb:	44 89 e7             	mov    %r12d,%edi
 4be:	8d 46 fa             	lea    -0x6(%rsi),%eax
 4c1:	8b 04 82             	mov    (%rdx,%rax,4),%eax
 4c4:	33 04 ba             	xor    (%rdx,%rdi,4),%eax
 4c7:	44 89 ff             	mov    %r15d,%edi
 4ca:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 4cd:	8d 7e 03             	lea    0x3(%rsi),%edi
 4d0:	41 39 f8             	cmp    %edi,%r8d
 4d3:	0f 86 a6 fe ff ff    	jbe    37f <AesExpandKey+0x37f>
 4d9:	44 8d 4e fb          	lea    -0x5(%rsi),%r9d
 4dd:	42 33 04 8a          	xor    (%rdx,%r9,4),%eax
 4e1:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 4e4:	8d 7e 04             	lea    0x4(%rsi),%edi
 4e7:	41 39 f8             	cmp    %edi,%r8d
 4ea:	0f 86 8f fe ff ff    	jbe    37f <AesExpandKey+0x37f>
 4f0:	41 33 06             	xor    (%r14),%eax
 4f3:	89 04 ba             	mov    %eax,(%rdx,%rdi,4)
 4f6:	e9 84 fe ff ff       	jmp    37f <AesExpandKey+0x37f>
 4fb:	0f 1f 44 00 00       	nopl   0x0(%rax,%rax,1)
 500:	31 c0                	xor    %eax,%eax
 502:	5b                   	pop    %rbx
 503:	5d                   	pop    %rbp
 504:	41 5c                	pop    %r12
 506:	41 5d                	pop    %r13
 508:	41 5e                	pop    %r14
 50a:	41 5f                	pop    %r15
 50c:	c3                   	ret
 50d:	4c 8b 5c 24 f0       	mov    -0x10(%rsp),%r11
 512:	41 89 c9             	mov    %ecx,%r9d
 515:	31 ff                	xor    %edi,%edi
 517:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
 51e:	00 00
 520:	41 0f b6 44 ba 01    	movzbl 0x1(%r10,%rdi,4),%eax
 526:	41 0f b6 34 ba       	movzbl (%r10,%rdi,4),%esi
 52b:	c1 e0 10             	shl    $0x10,%eax
 52e:	c1 e6 18             	shl    $0x18,%esi
 531:	09 f0                	or     %esi,%eax
 533:	41 0f b6 74 ba 03    	movzbl 0x3(%r10,%rdi,4),%esi
 539:	09 f0                	or     %esi,%eax
 53b:	41 0f b6 74 ba 02    	movzbl 0x2(%r10,%rdi,4),%esi
 541:	c1 e6 08             	shl    $0x8,%esi
 544:	09 f0                	or     %esi,%eax
 546:	41 89 44 bb 04       	mov    %eax,0x4(%r11,%rdi,4)
 54b:	48 83 c7 01          	add    $0x1,%rdi
 54f:	49 39 f9             	cmp    %rdi,%r9
 552:	75 cc                	jne    520 <AesExpandKey+0x520>
 554:	e9 6a fd ff ff       	jmp    2c3 <AesExpandKey+0x2c3>
 559:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)

0000000000000560 <AesEncrypt>:
 560:	f3 0f 1e fa          	endbr64
 564:	41 57                	push   %r15
 566:	48 89 f8             	mov    %rdi,%rax
 569:	48 89 d7             	mov    %rdx,%rdi
 56c:	41 56                	push   %r14
 56e:	41 55                	push   %r13
 570:	41 54                	push   %r12
 572:	55                   	push   %rbp
 573:	53                   	push   %rbx
 574:	48 81 ec 38 02 00 00 	sub    $0x238,%rsp
 57b:	64 48 8b 14 25 28 00 	mov    %fs:0x28,%rdx
 582:	00 00
 584:	48 89 94 24 28 02 00 	mov    %rdx,0x228(%rsp)
 58b:	00
 58c:	31 d2                	xor    %edx,%edx
 58e:	48 85 f6             	test   %rsi,%rsi
 591:	0f 94 c2             	sete   %dl
 594:	48 85 ff             	test   %rdi,%rdi
 597:	0f 94 c1             	sete   %cl
 59a:	08 ca                	or     %cl,%dl
 59c:	0f 85 c6 05 00 00    	jne    b68 <AesEncrypt+0x608>
 5a2:	48 85 c0             	test   %rax,%rax
 5a5:	0f 84 bd 05 00 00    	je     b68 <AesEncrypt+0x608>
 5ab:	44 0f b6 18          	movzbl (%rax),%r11d
 5af:	0f b6 50 03          	movzbl 0x3(%rax),%edx
 5b3:	48 89 f3             	mov    %rsi,%rbx
 5b6:	c7 44 24 40 04 00 00 	movl   $0x4,0x40(%rsp)
 5bd:	00
 5be:	44 0f b6 50 05       	movzbl 0x5(%rax),%r10d
 5c3:	44 0f b6 48 09       	movzbl 0x9(%rax),%r9d
 5c8:	48 8d 2d 00 00 00 00 	lea    0x0(%rip),%rbp        # 5cf <AesEncrypt+0x6f>
 5cf:	4c 8d a4 24 f4 00 00 	lea    0xf4(%rsp),%r12
 5d6:	00
 5d7:	41 c1 e3 18          	shl    $0x18,%r11d
 5db:	0f b6 48 0d          	movzbl 0xd(%rax),%ecx
 5df:	4c 8d 05 00 00 00 00 	lea    0x0(%rip),%r8        # 5e6 <AesEncrypt+0x86>
 5e6:	41 c1 e2 10          	shl    $0x10,%r10d
 5ea:	41 09 d3             	or     %edx,%r11d
 5ed:	0f b6 50 01          	movzbl 0x1(%rax),%edx
 5f1:	41 c1 e1 10          	shl    $0x10,%r9d
 5f5:	c1 e1 10             	shl    $0x10,%ecx
 5f8:	c1 e2 10             	shl    $0x10,%edx
 5fb:	41 09 d3             	or     %edx,%r11d
 5fe:	0f b6 50 02          	movzbl 0x2(%rax),%edx
 602:	c1 e2 08             	shl    $0x8,%edx
 605:	41 09 d3             	or     %edx,%r11d
 608:	0f b6 50 04          	movzbl 0x4(%rax),%edx
 60c:	44 89 5c 24 44       	mov    %r11d,0x44(%rsp)
 611:	c1 e2 18             	shl    $0x18,%edx
 614:	41 09 d2             	or     %edx,%r10d
 617:	0f b6 50 07          	movzbl 0x7(%rax),%edx
 61b:	41 09 d2             	or     %edx,%r10d
 61e:	0f b6 50 06          	movzbl 0x6(%rax),%edx
 622:	c1 e2 08             	shl    $0x8,%edx
 625:	41 09 d2             	or     %edx,%r10d
 628:	0f b6 50 08          	movzbl 0x8(%rax),%edx
 62c:	44 89 54 24 48       	mov    %r10d,0x48(%rsp)
 631:	c1 e2 18             	shl    $0x18,%edx
 634:	41 09 d1             	or     %edx,%r9d
 637:	0f b6 50 0b          	movzbl 0xb(%rax),%edx
 63b:	41 09 d1             	or     %edx,%r9d
 63e:	0f b6 50 0a          	movzbl 0xa(%rax),%edx
 642:	c1 e2 08             	shl    $0x8,%edx
 645:	41 09 d1             	or     %edx,%r9d
 648:	0f b6 50 0c          	movzbl 0xc(%rax),%edx
 64c:	44 89 4c 24 4c       	mov    %r9d,0x4c(%rsp)
 651:	c1 e2 18             	shl    $0x18,%edx
 654:	09 ca                	or     %ecx,%edx
 656:	0f b6 48 0f          	movzbl 0xf(%rax),%ecx
 65a:	0f b6 40 0e          	movzbl 0xe(%rax),%eax
 65e:	09 ca                	or     %ecx,%edx
 660:	c1 e0 08             	shl    $0x8,%eax
 663:	48 8d 4c 24 54       	lea    0x54(%rsp),%rcx
 668:	09 c2                	or     %eax,%edx
 66a:	89 54 24 50          	mov    %edx,0x50(%rsp)
 66e:	66 90                	xchg   %ax,%ax
 670:	89 d6                	mov    %edx,%esi
 672:	0f b6 c2             	movzbl %dl,%eax
 675:	48 83 c1 10          	add    $0x10,%rcx
 679:	48 83 c5 04          	add    $0x4,%rbp
 67d:	c1 ee 18             	shr    $0x18,%esi
 680:	41 8b 04 80          	mov    (%r8,%rax,4),%eax
 684:	41 8b 34 b0          	mov    (%r8,%rsi,4),%esi
 688:	25 00 ff 00 00       	and    $0xff00,%eax
 68d:	33 45 fc             	xor    -0x4(%rbp),%eax
 690:	c1 ce 08             	ror    $0x8,%esi
 693:	40 0f b6 f6          	movzbl %sil,%esi
 697:	31 f0                	xor    %esi,%eax
 699:	89 d6                	mov    %edx,%esi
 69b:	c1 ee 10             	shr    $0x10,%esi
 69e:	40 0f b6 f6          	movzbl %sil,%esi
 6a2:	41 8b 34 b0          	mov    (%r8,%rsi,4),%esi
 6a6:	c1 c6 10             	rol    $0x10,%esi
 6a9:	81 e6 00 00 00 ff    	and    $0xff000000,%esi
 6af:	31 f0                	xor    %esi,%eax
 6b1:	0f b6 f6             	movzbl %dh,%esi
 6b4:	89 f6                	mov    %esi,%esi
 6b6:	41 8b 34 b0          	mov    (%r8,%rsi,4),%esi
 6ba:	c1 c6 08             	rol    $0x8,%esi
 6bd:	81 e6 00 00 ff 00    	and    $0xff0000,%esi
 6c3:	31 f0                	xor    %esi,%eax
 6c5:	41 31 c3             	xor    %eax,%r11d
 6c8:	45 31 da             	xor    %r11d,%r10d
 6cb:	44 89 59 f0          	mov    %r11d,-0x10(%rcx)
 6cf:	45 31 d1             	xor    %r10d,%r9d
 6d2:	44 89 51 f4          	mov    %r10d,-0xc(%rcx)
 6d6:	44 31 ca             	xor    %r9d,%edx
 6d9:	44 89 49 f8          	mov    %r9d,-0x8(%rcx)
 6dd:	89 51 fc             	mov    %edx,-0x4(%rcx)
 6e0:	4c 39 e1             	cmp    %r12,%rcx
 6e3:	75 8b                	jne    670 <AesEncrypt+0x110>
 6e5:	8b 44 24 40          	mov    0x40(%rsp),%eax
 6e9:	0f b6 53 03          	movzbl 0x3(%rbx),%edx
 6ed:	0f b6 4b 08          	movzbl 0x8(%rbx),%ecx
 6f1:	0f b6 73 0d          	movzbl 0xd(%rbx),%esi
 6f5:	8d 68 06             	lea    0x6(%rax),%ebp
 6f8:	0f b6 03             	movzbl (%rbx),%eax
 6fb:	f3 0f 6f 64 24 44    	movdqu 0x44(%rsp),%xmm4
 701:	c1 e1 18             	shl    $0x18,%ecx
 704:	c1 e6 10             	shl    $0x10,%esi
 707:	c1 e0 18             	shl    $0x18,%eax
 70a:	09 d0                	or     %edx,%eax
 70c:	0f b6 53 01          	movzbl 0x1(%rbx),%edx
 710:	c1 e2 10             	shl    $0x10,%edx
 713:	09 d0                	or     %edx,%eax
 715:	0f b6 53 02          	movzbl 0x2(%rbx),%edx
 719:	c1 e2 08             	shl    $0x8,%edx
 71c:	09 d0                	or     %edx,%eax
 71e:	0f b6 53 04          	movzbl 0x4(%rbx),%edx
 722:	66 0f 6e c0          	movd   %eax,%xmm0
 726:	0f b6 43 05          	movzbl 0x5(%rbx),%eax
 72a:	c1 e2 18             	shl    $0x18,%edx
 72d:	c1 e0 10             	shl    $0x10,%eax
 730:	09 d0                	or     %edx,%eax
 732:	0f b6 53 07          	movzbl 0x7(%rbx),%edx
 736:	09 d0                	or     %edx,%eax
 738:	0f b6 53 06          	movzbl 0x6(%rbx),%edx
 73c:	c1 e2 08             	shl    $0x8,%edx
 73f:	09 c2                	or     %eax,%edx
 741:	0f b6 43 09          	movzbl 0x9(%rbx),%eax
 745:	66 0f 6e da          	movd   %edx,%xmm3
 749:	c1 e0 10             	shl    $0x10,%eax
 74c:	66 0f 62 c3          	punpckldq %xmm3,%xmm0
 750:	09 c8                	or     %ecx,%eax
 752:	0f b6 4b 0b          	movzbl 0xb(%rbx),%ecx
 756:	09 c8                	or     %ecx,%eax
 758:	0f b6 4b 0a          	movzbl 0xa(%rbx),%ecx
 75c:	c1 e1 08             	shl    $0x8,%ecx
 75f:	09 c8                	or     %ecx,%eax
 761:	0f b6 4b 0c          	movzbl 0xc(%rbx),%ecx
 765:	66 0f 6e c8          	movd   %eax,%xmm1
 769:	c1 e1 18             	shl    $0x18,%ecx
 76c:	09 f1                	or     %esi,%ecx
 76e:	0f b6 73 0f          	movzbl 0xf(%rbx),%esi
 772:	09 f1                	or     %esi,%ecx
 774:	0f b6 73 0e          	movzbl 0xe(%rbx),%esi
 778:	c1 e6 08             	shl    $0x8,%esi
 77b:	09 f1                	or     %esi,%ecx
 77d:	66 0f 6e d1          	movd   %ecx,%xmm2
 781:	66 0f 62 ca          	punpckldq %xmm2,%xmm1
 785:	66 0f 6c c1          	punpcklqdq %xmm1,%xmm0
 789:	66 0f ef c4          	pxor   %xmm4,%xmm0
 78d:	66 0f 70 c8 ff       	pshufd $0xff,%xmm0,%xmm1
 792:	66 41 0f 7e c3       	movd   %xmm0,%r11d
 797:	0f 29 44 24 20       	movaps %xmm0,0x20(%rsp)
 79c:	66 0f 7e c9          	movd   %xmm1,%ecx
 7a0:	66 0f 6f c8          	movdqa %xmm0,%xmm1
 7a4:	66 0f 6a c8          	punpckhdq %xmm0,%xmm1
 7a8:	66 0f 7e ca          	movd   %xmm1,%edx
 7ac:	66 0f 70 c8 55       	pshufd $0x55,%xmm0,%xmm1
 7b1:	66 0f 7e c8          	movd   %xmm1,%eax
 7b5:	83 fd 01             	cmp    $0x1,%ebp
 7b8:	0f 86 d4 03 00 00    	jbe    b92 <AesEncrypt+0x632>
 7be:	bb 01 00 00 00       	mov    $0x1,%ebx
 7c3:	be 04 00 00 00       	mov    $0x4,%esi
 7c8:	4c 8d 54 24 30       	lea    0x30(%rsp),%r10
 7cd:	4c 8d 4c 24 20       	lea    0x20(%rsp),%r9
 7d2:	eb 0d                	jmp    7e1 <AesEncrypt+0x281>
 7d4:	0f 1f 40 00          	nopl   0x0(%rax)
 7d8:	4d 89 cc             	mov    %r9,%r12
 7db:	4d 89 d1             	mov    %r10,%r9
 7de:	4d 89 e2             	mov    %r12,%r10
 7e1:	c1 e8 10             	shr    $0x10,%eax
 7e4:	0f b6 c9             	movzbl %cl,%ecx
 7e7:	0f b6 d6             	movzbl %dh,%edx
 7ea:	41 c1 eb 18          	shr    $0x18,%r11d
 7ee:	0f b6 c0             	movzbl %al,%eax
 7f1:	41 8b 0c 88          	mov    (%r8,%rcx,4),%ecx
 7f5:	89 d2                	mov    %edx,%edx
 7f7:	83 c3 01             	add    $0x1,%ebx
 7fa:	41 8b 04 80          	mov    (%r8,%rax,4),%eax
 7fe:	41 8b 14 90          	mov    (%r8,%rdx,4),%edx
 802:	c1 c1 08             	rol    $0x8,%ecx
 805:	43 33 0c 98          	xor    (%r8,%r11,4),%ecx
 809:	c1 c8 08             	ror    $0x8,%eax
 80c:	c1 c2 10             	rol    $0x10,%edx
 80f:	31 c8                	xor    %ecx,%eax
 811:	31 d0                	xor    %edx,%eax
 813:	89 f2                	mov    %esi,%edx
 815:	33 44 94 44          	xor    0x44(%rsp,%rdx,4),%eax
 819:	41 89 02             	mov    %eax,(%r10)
 81c:	41 89 c3             	mov    %eax,%r11d
 81f:	41 0f b6 01          	movzbl (%r9),%eax
 823:	41 0f b6 51 07       	movzbl 0x7(%r9),%edx
 828:	41 8b 04 80          	mov    (%r8,%rax,4),%eax
 82c:	c1 c0 08             	rol    $0x8,%eax
 82f:	41 33 04 90          	xor    (%r8,%rdx,4),%eax
 833:	41 0f b6 51 0a       	movzbl 0xa(%r9),%edx
 838:	41 8b 14 90          	mov    (%r8,%rdx,4),%edx
 83c:	c1 ca 08             	ror    $0x8,%edx
 83f:	31 d0                	xor    %edx,%eax
 841:	41 0f b6 51 0d       	movzbl 0xd(%r9),%edx
 846:	41 8b 14 90          	mov    (%r8,%rdx,4),%edx
 84a:	c1 c2 10             	rol    $0x10,%edx
 84d:	31 d0                	xor    %edx,%eax
 84f:	8d 56 01             	lea    0x1(%rsi),%edx
 852:	33 44 94 44          	xor    0x44(%rsp,%rdx,4),%eax
 856:	41 89 42 04          	mov    %eax,0x4(%r10)
 85a:	41 0f b6 51 04       	movzbl 0x4(%r9),%edx
 85f:	41 0f b6 49 0b       	movzbl 0xb(%r9),%ecx
 864:	41 8b 14 90          	mov    (%r8,%rdx,4),%edx
 868:	c1 c2 08             	rol    $0x8,%edx
 86b:	41 33 14 88          	xor    (%r8,%rcx,4),%edx
 86f:	41 0f b6 49 0e       	movzbl 0xe(%r9),%ecx
 874:	41 8b 0c 88          	mov    (%r8,%rcx,4),%ecx
 878:	c1 c9 08             	ror    $0x8,%ecx
 87b:	31 ca                	xor    %ecx,%edx
 87d:	41 8b 09             	mov    (%r9),%ecx
 880:	0f b6 cd             	movzbl %ch,%ecx
 883:	89 c9                	mov    %ecx,%ecx
 885:	41 8b 0c 88          	mov    (%r8,%rcx,4),%ecx
 889:	c1 c1 10             	rol    $0x10,%ecx
 88c:	31 ca                	xor    %ecx,%edx
 88e:	8d 4e 02             	lea    0x2(%rsi),%ecx
 891:	33 54 8c 44          	xor    0x44(%rsp,%rcx,4),%edx
 895:	41 89 52 08          	mov    %edx,0x8(%r10)
 899:	41 0f b6 49 08       	movzbl 0x8(%r9),%ecx
 89e:	45 0f b6 61 0f       	movzbl 0xf(%r9),%r12d
 8a3:	41 8b 0c 88          	mov    (%r8,%rcx,4),%ecx
 8a7:	c1 c1 08             	rol    $0x8,%ecx
 8aa:	43 33 0c a0          	xor    (%r8,%r12,4),%ecx
 8ae:	45 0f b6 61 02       	movzbl 0x2(%r9),%r12d
 8b3:	47 8b 24 a0          	mov    (%r8,%r12,4),%r12d
 8b7:	41 c1 cc 08          	ror    $0x8,%r12d
 8bb:	44 31 e1             	xor    %r12d,%ecx
 8be:	45 0f b6 61 05       	movzbl 0x5(%r9),%r12d
 8c3:	47 8b 24 a0          	mov    (%r8,%r12,4),%r12d
 8c7:	41 c1 c4 10          	rol    $0x10,%r12d
 8cb:	44 31 e1             	xor    %r12d,%ecx
 8ce:	44 8d 66 03          	lea    0x3(%rsi),%r12d
 8d2:	83 c6 04             	add    $0x4,%esi
 8d5:	42 33 4c a4 44       	xor    0x44(%rsp,%r12,4),%ecx
 8da:	41 89 4a 0c          	mov    %ecx,0xc(%r10)
 8de:	39 dd                	cmp    %ebx,%ebp
 8e0:	0f 85 f2 fe ff ff    	jne    7d8 <AesEncrypt+0x278>
 8e6:	44 8d 34 ad 00 00 00 	lea    0x0(,%rbp,4),%r14d
 8ed:	00
 8ee:	4c 89 f5             	mov    %r14,%rbp
 8f1:	49 c1 e6 02          	shl    $0x2,%r14
 8f5:	44 8d 6d 01          	lea    0x1(%rbp),%r13d
 8f9:	44 8d 65 02          	lea    0x2(%rbp),%r12d
 8fd:	8d 5d 03             	lea    0x3(%rbp),%ebx
 900:	49 c1 e5 02          	shl    $0x2,%r13
 904:	49 c1 e4 02          	shl    $0x2,%r12
 908:	48 c1 e3 02          	shl    $0x2,%rbx
 90c:	c1 e8 10             	shr    $0x10,%eax
 90f:	0f b6 d6             	movzbl %dh,%edx
 912:	0f b6 c9             	movzbl %cl,%ecx
 915:	41 c1 eb 18          	shr    $0x18,%r11d
 919:	89 d2                	mov    %edx,%edx
 91b:	0f b6 c0             	movzbl %al,%eax
 91e:	41 8b 34 90          	mov    (%r8,%rdx,4),%esi
 922:	41 8b 14 88          	mov    (%r8,%rcx,4),%edx
 926:	41 8b 04 80          	mov    (%r8,%rax,4),%eax
 92a:	c1 ca 08             	ror    $0x8,%edx
 92d:	81 e6 00 ff 00 00    	and    $0xff00,%esi
 933:	0f b6 d2             	movzbl %dl,%edx
 936:	c1 c0 08             	rol    $0x8,%eax
 939:	09 d6                	or     %edx,%esi
 93b:	43 8b 14 98          	mov    (%r8,%r11,4),%edx
 93f:	25 00 00 ff 00       	and    $0xff0000,%eax
 944:	42 33 74 34 44       	xor    0x44(%rsp,%r14,1),%esi
 949:	c1 c2 10             	rol    $0x10,%edx
 94c:	81 e2 00 00 00 ff    	and    $0xff000000,%edx
 952:	09 d0                	or     %edx,%eax
 954:	31 c6                	xor    %eax,%esi
 956:	41 89 31             	mov    %esi,(%r9)
 959:	41 0f b6 12          	movzbl (%r10),%edx
 95d:	89 f5                	mov    %esi,%ebp
 95f:	41 0f b6 42 0d       	movzbl 0xd(%r10),%eax
 964:	41 0f b6 4a 07       	movzbl 0x7(%r10),%ecx
 969:	41 8b 14 90          	mov    (%r8,%rdx,4),%edx
 96d:	41 8b 04 80          	mov    (%r8,%rax,4),%eax
 971:	41 8b 0c 88          	mov    (%r8,%rcx,4),%ecx
 975:	c1 ca 08             	ror    $0x8,%edx
 978:	25 00 ff 00 00       	and    $0xff00,%eax
 97d:	0f b6 d2             	movzbl %dl,%edx
 980:	c1 c1 10             	rol    $0x10,%ecx
 983:	09 d0                	or     %edx,%eax
 985:	41 0f b6 52 0a       	movzbl 0xa(%r10),%edx
 98a:	81 e1 00 00 00 ff    	and    $0xff000000,%ecx
 990:	42 33 44 2c 44       	xor    0x44(%rsp,%r13,1),%eax
 995:	41 8b 14 90          	mov    (%r8,%rdx,4),%edx
 999:	c1 c2 08             	rol    $0x8,%edx
 99c:	81 e2 00 00 ff 00    	and    $0xff0000,%edx
 9a2:	09 ca                	or     %ecx,%edx
 9a4:	31 d0                	xor    %edx,%eax
 9a6:	41 89 41 04          	mov    %eax,0x4(%r9)
 9aa:	41 8b 12             	mov    (%r10),%edx
 9ad:	41 89 c7             	mov    %eax,%r15d
 9b0:	41 89 c5             	mov    %eax,%r13d
 9b3:	45 0f b6 5a 0b       	movzbl 0xb(%r10),%r11d
 9b8:	41 89 c6             	mov    %eax,%r14d
 9bb:	0f b6 c0             	movzbl %al,%eax
 9be:	0f b6 d6             	movzbl %dh,%edx
 9c1:	89 d2                	mov    %edx,%edx
 9c3:	47 8b 1c 98          	mov    (%r8,%r11,4),%r11d
 9c7:	41 8b 0c 90          	mov    (%r8,%rdx,4),%ecx
 9cb:	41 0f b6 52 04       	movzbl 0x4(%r10),%edx
 9d0:	41 c1 c3 10          	rol    $0x10,%r11d
 9d4:	41 8b 14 90          	mov    (%r8,%rdx,4),%edx
 9d8:	81 e1 00 ff 00 00    	and    $0xff00,%ecx
 9de:	41 81 e3 00 00 00 ff 	and    $0xff000000,%r11d
 9e5:	c1 ca 08             	ror    $0x8,%edx
 9e8:	0f b6 d2             	movzbl %dl,%edx
 9eb:	09 d1                	or     %edx,%ecx
 9ed:	41 0f b6 52 0e       	movzbl 0xe(%r10),%edx
 9f2:	42 33 4c 24 44       	xor    0x44(%rsp,%r12,1),%ecx
 9f7:	41 89 f4             	mov    %esi,%r12d
 9fa:	41 8b 14 90          	mov    (%r8,%rdx,4),%edx
 9fe:	c1 c2 08             	rol    $0x8,%edx
 a01:	81 e2 00 00 ff 00    	and    $0xff0000,%edx
 a07:	44 09 da             	or     %r11d,%edx
 a0a:	31 d1                	xor    %edx,%ecx
 a0c:	41 89 49 08          	mov    %ecx,0x8(%r9)
 a10:	41 0f b6 52 05       	movzbl 0x5(%r10),%edx
 a15:	45 0f b6 4a 08       	movzbl 0x8(%r10),%r9d
 a1a:	41 8b 14 90          	mov    (%r8,%rdx,4),%edx
 a1e:	47 8b 0c 88          	mov    (%r8,%r9,4),%r9d
 a22:	81 e2 00 ff 00 00    	and    $0xff00,%edx
 a28:	41 c1 ef 08          	shr    $0x8,%r15d
 a2c:	41 c1 c9 08          	ror    $0x8,%r9d
 a30:	48 c1 e0 08          	shl    $0x8,%rax
 a34:	45 0f b6 ff          	movzbl %r15b,%r15d
 a38:	41 c1 ee 10          	shr    $0x10,%r14d
 a3c:	45 0f b6 c9          	movzbl %r9b,%r9d
 a40:	4c 09 f8             	or     %r15,%rax
 a43:	41 c1 ed 18          	shr    $0x18,%r13d
 a47:	44 09 ca             	or     %r9d,%edx
 a4a:	45 0f b6 4a 02       	movzbl 0x2(%r10),%r9d
 a4f:	33 54 1c 44          	xor    0x44(%rsp,%rbx,1),%edx
 a53:	48 c1 e0 08          	shl    $0x8,%rax
 a57:	45 0f b6 f6          	movzbl %r14b,%r14d
 a5b:	45 0f b6 ed          	movzbl %r13b,%r13d
 a5f:	89 cb                	mov    %ecx,%ebx
 a61:	41 c1 ec 08          	shr    $0x8,%r12d
 a65:	47 8b 0c 88          	mov    (%r8,%r9,4),%r9d
 a69:	45 0f b6 52 0f       	movzbl 0xf(%r10),%r10d
 a6e:	4c 09 f0             	or     %r14,%rax
 a71:	c1 eb 18             	shr    $0x18,%ebx
 a74:	48 c1 e0 08          	shl    $0x8,%rax
 a78:	89 1c 24             	mov    %ebx,(%rsp)
 a7b:	45 0f b6 e4          	movzbl %r12b,%r12d
 a7f:	c1 ed 10             	shr    $0x10,%ebp
 a82:	47 8b 04 90          	mov    (%r8,%r10,4),%r8d
 a86:	41 c1 c1 08          	rol    $0x8,%r9d
 a8a:	4c 09 e8             	or     %r13,%rax
 a8d:	44 0f b6 ee          	movzbl %sil,%r13d
 a91:	41 81 e1 00 00 ff 00 	and    $0xff0000,%r9d
 a98:	48 c1 e0 08          	shl    $0x8,%rax
 a9c:	41 89 ca             	mov    %ecx,%r10d
 a9f:	40 0f b6 ed          	movzbl %bpl,%ebp
 aa3:	41 c1 c0 10          	rol    $0x10,%r8d
 aa7:	41 c1 ea 10          	shr    $0x10,%r10d
 aab:	41 81 e0 00 00 00 ff 	and    $0xff000000,%r8d
 ab2:	44 89 54 24 1c       	mov    %r10d,0x1c(%rsp)
 ab7:	45 09 c8             	or     %r9d,%r8d
 aba:	41 89 c9             	mov    %ecx,%r9d
 abd:	0f b6 c9             	movzbl %cl,%ecx
 ac0:	44 31 c2             	xor    %r8d,%edx
 ac3:	41 89 f0             	mov    %esi,%r8d
 ac6:	48 89 c6             	mov    %rax,%rsi
 ac9:	41 c1 e9 08          	shr    $0x8,%r9d
 acd:	4c 09 ee             	or     %r13,%rsi
 ad0:	89 d3                	mov    %edx,%ebx
 ad2:	41 89 d2             	mov    %edx,%r10d
 ad5:	41 89 d3             	mov    %edx,%r11d
 ad8:	48 c1 e6 08          	shl    $0x8,%rsi
 adc:	c1 eb 08             	shr    $0x8,%ebx
 adf:	0f b6 c2             	movzbl %dl,%eax
 ae2:	45 0f b6 c9          	movzbl %r9b,%r9d
 ae6:	4c 09 e6             	or     %r12,%rsi
 ae9:	41 c1 e8 18          	shr    $0x18,%r8d
 aed:	0f b6 db             	movzbl %bl,%ebx
 af0:	0f b6 54 24 1c       	movzbl 0x1c(%rsp),%edx
 af5:	41 c1 ea 18          	shr    $0x18,%r10d
 af9:	41 c1 eb 10          	shr    $0x10,%r11d
 afd:	45 0f b6 c0          	movzbl %r8b,%r8d
 b01:	48 c1 e6 08          	shl    $0x8,%rsi
 b05:	48 c1 e0 08          	shl    $0x8,%rax
 b09:	45 0f b6 db          	movzbl %r11b,%r11d
 b0d:	45 0f b6 d2          	movzbl %r10b,%r10d
 b11:	48 09 d8             	or     %rbx,%rax
 b14:	48 09 ee             	or     %rbp,%rsi
 b17:	48 c1 e0 08          	shl    $0x8,%rax
 b1b:	48 c1 e6 08          	shl    $0x8,%rsi
 b1f:	4c 09 d8             	or     %r11,%rax
 b22:	4c 09 c6             	or     %r8,%rsi
 b25:	48 c1 e0 08          	shl    $0x8,%rax
 b29:	4c 09 d0             	or     %r10,%rax
 b2c:	48 c1 e0 08          	shl    $0x8,%rax
 b30:	48 09 c8             	or     %rcx,%rax
 b33:	48 c1 e0 08          	shl    $0x8,%rax
 b37:	4c 09 c8             	or     %r9,%rax
 b3a:	48 c1 e0 08          	shl    $0x8,%rax
 b3e:	48 09 d0             	or     %rdx,%rax
 b41:	0f b6 14 24          	movzbl (%rsp),%edx
 b45:	48 89 34 24          	mov    %rsi,(%rsp)
 b49:	48 c1 e0 08          	shl    $0x8,%rax
 b4d:	48 09 d0             	or     %rdx,%rax
 b50:	48 89 44 24 08       	mov    %rax,0x8(%rsp)
 b55:	66 0f 6f 2c 24       	movdqa (%rsp),%xmm5
 b5a:	31 c0                	xor    %eax,%eax
 b5c:	0f 11 2f             	movups %xmm5,(%rdi)
 b5f:	eb 0c                	jmp    b6d <AesEncrypt+0x60d>
 b61:	0f 1f 80 00 00 00 00 	nopl   0x0(%rax)
 b68:	b8 01 00 00 00       	mov    $0x1,%eax
 b6d:	48 8b 94 24 28 02 00 	mov    0x228(%rsp),%rdx
 b74:	00
 b75:	64 48 2b 14 25 28 00 	sub    %fs:0x28,%rdx
 b7c:	00 00
 b7e:	75 38                	jne    bb8 <AesEncrypt+0x658>
 b80:	48 81 c4 38 02 00 00 	add    $0x238,%rsp
 b87:	5b                   	pop    %rbx
 b88:	5d                   	pop    %rbp
 b89:	41 5c                	pop    %r12
 b8b:	41 5d                	pop    %r13
 b8d:	41 5e                	pop    %r14
 b8f:	41 5f                	pop    %r15
 b91:	c3                   	ret
 b92:	bb 1c 00 00 00       	mov    $0x1c,%ebx
 b97:	4c 8d 4c 24 30       	lea    0x30(%rsp),%r9
 b9c:	4c 8d 54 24 20       	lea    0x20(%rsp),%r10
 ba1:	41 bc 18 00 00 00    	mov    $0x18,%r12d
 ba7:	41 bd 14 00 00 00    	mov    $0x14,%r13d
 bad:	41 be 10 00 00 00    	mov    $0x10,%r14d
 bb3:	e9 54 fd ff ff       	jmp    90c <AesEncrypt+0x3ac>
 bb8:	e8 00 00 00 00       	call   bbd <AesEncrypt+0x65d>
