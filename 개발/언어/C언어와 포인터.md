---
publish: true
draft: false
---

# C 언어와 포인터

> **분류:** 개발 › 언어 · [[생활위키 목차]]

C는 **메모리·주소를 직접 다루는** 저수준에 가까운 고수준 언어다. 
운영체제, 임베디드, 드라이버, 성능 민감 코드, 다른 언어 런타임의 기반에 쓰인다.

포인터는 “변수가 담은 **값의 주소**”를 다루는 타입이다. 
대부분의 혼란은 **값 vs 주소 vs 그 주소에 있는 값**을 한 기호로 섞어 쓸 때 생긴다.

확인일: 2026-08-06

---

## 0. 학습 지도

```text
기초 타입·제어문·함수·배열
핵심 포인터·배열·문자열·malloc
중급 포인터 연산·다중 포인터·함수 포인터·구조체
함정 수명·정렬·const·void*·스택/힙
```

도구: GCC/Clang/MSVC, [[VS Code 사용법]] / [[Cursor 사용법]].

---

# Part 1 — C 기초 요약

## 1. 프로그램 골격

```c
#include <stdio.h>

int main(void) {
 printf("hello\n");
 return 0;
}
```

```bash
gcc -Wall -Wextra -o hello hello.c
./hello
```

## 2. 타입·변수

| 타입 | 설명 |
|------|------|
| `char` | 최소 1바이트, 문자/작은 정수 |
| `int` / `long` / `long long` | 정수 (크기는 플랫폼 의존 — `stdint.h`의 `int32_t` 권장) |
| `float` / `double` | 실수 |
| `size_t` | 크기·인덱스용 부호 없는 정수 |
| `_Bool` / `bool` (`stdbool.h`) | 참/거짓 |

- 지역 변수: 초기화 안 하면 **쓰레기 값** 
- `const`: 읽기 전용으로 취급 (완벽 방탄은 아님)

## 3. 제어·함수

`if`, `for`, `while`, `switch`, `break`, `continue` — 다른 언어와 유사. 
함수는 **값 전달(call by value)** 이 기본. “참조처럼” 바꾸려면 **포인터를 넘긴다**.

```c
void add_one(int *p) {
 *p = *p + 1;
}
```

## 4. 배열·문자열

```c
int a[5] = {1, 2, 3, 4, 5};
char s[] = "hi"; // {'h','i','\0'}
```

- 배열 이름은 많은 식에서 **첫 요소의 주소**로 감쇠(decay) 
- C 문자열은 `\0`으로 끝나는 `char` 배열 
- `strlen`, `strcpy` → 가능하면 `strncpy`/`strlcpy`·길이 검사 (버퍼 오버플로)

---

# Part 2 — 포인터 핵심

## 5. 한 장으로 이해하기

```text
int x = 10;
int *p = &x;

 이름 들어 있는 것
 x → 10 (값)
 p → x의 주소 (포인터 값 = 주소)
 *p → 10 (역참조 = 그 주소의 값)
 &x → x의 주소
 &p → p라는 변수의 주소 (포인터의 포인터로 이어짐)
```

| 기호 | 이름 | 하는 일 |
|------|------|---------|
| `&` | address-of | 변수 → 주소 |
| `*` (선언) | pointer type | “이걸 가리키는 포인터” |
| `*` (식) | dereference | 주소 → 그곳의 값 |
| `->` | | `(*ptr).member` 축약 |

```c
int x = 10;
int *p = &x; // p는 int를 가리킴
*p = 20; // x가 20이 됨
printf("%d\n", x); // 20
```

### 선언을 읽는 법

**“선언은 사용하듯이 읽는다”** (clockwise/spiral rule).

```c
int *p; // *p 가 int → p는 int*
int *p, q; // p만 포인터, q는 int ← 헷갈림 포인트!
int *p, *q; // 둘 다 포인터
```

한 줄에 포인터·일반 변수를 섞지 않는 편이 안전하다.

---

## 6. 헷갈리기 쉬운 포인트 (집중)

### 6.1 `*`가 선언에 있을 때 vs 식에 있을 때

```c
int *p = &x; // 선언: p의 타입은 int*
*p = 5; // 식: p가 가리키는 곳에 5
```

같은 글자 `*`인데 역할이 다르다.

### 6.2 `int* p` vs `int *p`

의미는 같다. 팀 스타일 문제. 
다만 `int* p, q`는 착각을 부르니 `int *p; int q;`로 나누자.

### 6.3 배열 ≠ 포인터 (하지만 자주 같아 보인다)

```c
int a[3] = {1,2,3};
int *p = a; // &a[0] 과 같음 (감쇠)
```

| | 배열 `a` | 포인터 `p` |
|--|----------|------------|
| `sizeof` | 배열 전체 바이트 | 포인터 크기 (4/8) |
| 할당 | 보통 스택(또는 static)에 연속 공간 | 주소만 담음 |
| `&a` | 배열 전체의 주소 (`int (*)[3]`) | `&p`는 포인터 변수의 주소 |

```c
printf("%zu %zu\n", sizeof a, sizeof p); // 예: 12 와 8
```

함수 인자로 배열을 넘기면 **포인터로 감쇠**한다.

```c
void f(int a[10]); // 실제로는 int *a 와 거의 동일
void g(int *a);
```

### 6.4 `a[i]` 와 `*(a+i)`

완전히 같다. `i[a]`도 문법상 가능하지만 쓰지 말 것.

### 6.5 `char *` 문자열 리터럴

```c
char *s = "hello"; // 리터럴은 보통 읽기 전용 영역
s[0] = 'H'; // 미정의 동작(UB)! 크래시 가능

char buf[] = "hello"; // 수정 가능한 복사본
buf[0] = 'H'; // OK
```

현대에는 `const char *s = "hello";` 권장.

### 6.6 널 포인터

```c
int *p = NULL; // 또는 nullptr (C23), 0
if (p) { *p; } // NULL이면 역참조 금지
```

`NULL`을 역참조 = UB. 
해제 후:

```c
free(p);
p = NULL; // 댕글링 방지 습관
```

### 6.7 댕글링 포인터 (수명)

```c
int *bad(void) {
 int x = 10;
 return &x; // 함수 끝나면 x 소멸 → 반환 주소 무효!
}
```

힙은 `malloc`한 동안만 유효. `free` 이후 그 주소 사용 금지.

### 6.8 `const` 위치 (진짜 많이 헷갈림)

```c
const int *p; // 가리키는 int를 못 바꿈 (*p = 1 불가). p는 다른 주소로 가능
int const *p; // 위와 동일
int *const p; // p 자체(주소)를 못 바꿈. *p = 1 은 가능
const int *const p; // 둘 다 const
```

읽는 팁: `const`가 `*` **왼쪽**이면 데이터 const, **오른쪽**이면 포인터 const.

### 6.9 `void *`

“타입 없는 주소”. 어떤 객체 포인터와도 변환 가능(함수 포인터는 별도 주의).

```c
void *v = malloc(100);
int *p = v; // C에서는 암시적 변환 허용 (C++은 캐스트 필요)
```

`void *`는 역참조·산술 불가 → 쓸 타입으로 캐스팅 후 사용.

### 6.10 포인터 산술

```c
int a[5];
int *p = a;
p + 1; // 다음 int (보통 +4바이트), +1바이트 아님
```

단위는 **가리키는 타입의 크기**. `char *`만 +1이 1바이트.

### 6.11 `++` 와 `*` 우선순위

```c
*p++; // *(p++) → 예전 위치를 읽고 p는 다음으로
(*p)++; // 가리키는 값을 1 증가
*++p; // 먼저 p 증가 후 역참조
++*p; // (*p)를 증가
```

헷갈리면 괄호를 친다.

### 6.12 이중 포인터 `int **`

“포인터 변수의 주소” 또는 “포인터 배열”.

```c
void set_ptr(int **pp, int *target) {
 *pp = target; // 호출자 쪽 포인터 변수를 바꿈
}

int *p = NULL;
int x = 1;
set_ptr(&p, &x); // p가 &x를 가리킴
```

`argv`가 `char **`인 이유: 문자열 포인터들의 배열.

### 6.13 포인터 배열 vs 배열 포인터

```c
int *pp[5]; // int* 가 5개 (포인터 배열)
int (*pa)[5]; // int[5] 전체를 가리키는 포인터 (배열 포인터)
```

괄호가 의미를 가른다. `[]`가 `*`보다 우선.

### 6.14 함수 포인터

```c
int add(int a, int b) { return a + b; }
int (*fp)(int, int) = add;
fp(1, 2);
```

콜백, 테이블 디스패치에 사용. 선언이 복잡하면 `typedef`.

```c
typedef int (*binop_t)(int, int);
binop_t fp = add;
```

### 6.15 `sizeof` 함정

```c
void f(int a[100]) {
 // sizeof a == sizeof(int*) (감쇠됨)
}
```

길이는 인자로 따로 넘긴다: `f(a, n)`.

### 6.16 스택 vs 힙

| | 스택 지역변수 | `malloc` 힙 |
|--|---------------|-------------|
| 수명 | 블록 끝 | `free`까지 |
| 크기 | 자동, 상대적으로 작음 | 큼, 실패 가능 |
| 포인터 | `&local` 반환 금지 | 반환·보관 OK (free 전) |

```c
int *p = malloc(sizeof *p * n);
if (!p) { /* 실패 */ }
// ...
free(p);
```

`sizeof *p` 패턴: 타입 바꿔도 식 유지.

### 6.17 정렬·캐스팅 UB

임의 `char` 버퍼를 `int *`로 잘못 캐스팅하면 정렬 UB. 
구조체 padding, 엄격한 aliasing 규칙도 심화 함정.

### 6.18 `++i` 와 시퀀스 포인트 (구버전)

같은 식에서 같은 변수를 두 번 수정하는 `a[i] = i++;` 류는 UB. 
문장을 나누자.

---

## 7. 구조체와 포인터

```c
struct Point { int x; int y; };
struct Point pt = {1, 2};
struct Point *q = &pt;
q->x = 3; // (*q).x
```

동적:

```c
struct Point *q = malloc(sizeof *q);
q->x = 1;
free(q);
```

연결 리스트: `struct Node { int v; struct Node *next; };`

---

## 8. 동적 2차원

```c
// 포인터 배열 방식
int **m = malloc(sizeof *m * rows);
for (int i = 0; i < rows; i++)
 m[i] = malloc(sizeof *m[i] * cols);

// 해제 역순
for (int i = 0; i < rows; i++) free(m[i]);
free(m);
```

연속 블록 하나 + 인덱싱 매크로/함수가 캐시에 유리한 경우도 많다.

---

## 9. 좋은 습관

1. 포인터는 **초기화** (`NULL` 또는 유효 주소) 
2. `malloc` 후 **NULL 검사**, `free` 후 **NULL** 
3. 소유권(누가 free?)을 함수 주석·이름으로 명확히 
4. `const`를 API에 넣어 의도 표현 
5. `-Wall -Wextra`, 가능하면 **AddressSanitizer** (`-fsanitize=address`) 
6. 버퍼 길이·인덱스 검사 
7. 복잡한 선언은 `typedef` 

---

## 10. 미니 연습

1. `swap(int *a, int *b)` 구현 
2. 배열 합: `int sum(const int *a, size_t n)` 
3. 문자열 길이 직접 구현 (`\0`까지) 
4. `malloc`으로 int 배열 n개 → 평균 → `free` 
5. `const char *` vs `char *`에 문자열 리터럴 대입해 보기 (후자는 경고·위험) 
6. `int *p[3]` 와 `int (*p)[3]` 선언·`sizeof` 출력 

---

## 11. C와 다른 언어

| | C 포인터 | Java/Python |
|--|----------|-------------|
| 주소 연산 | 가능 | 참조만, 산술 없음 |
| 수동 free | 있음 | GC |
| 배열 | 포인터와 밀접 | 길이 포함 객체 |
| 안전성 | 프로그래머 책임 | 런타임 검사 많음 |

[[Java 언어 학습]], [[Python 학습과 패키지]]는 추상화가 높고, C는 **메모리를 눈에 보이게** 한다. 
OS·임베디드·[[Docker 사용법]] 이미지 속 네이티브 모듈을 볼 때 도움이 된다.

---

## 12. 치트시트

```c
T x; T *p = &x; *p; p->mem;
a[i] == *(a+i)
const T *p; // 데이터 const
T *const p; // 포인터 const
void *malloc(size); free(p);
int (*fp)(int,int);
int *arr[N]; vs int (*row)[N];
```

**한 줄 요약**: 포인터 변수에는 **주소**가 들어 있고, `*`를 붙여야 **그곳의 값**이다.

---

## 관련

- [[생활위키 목차]]
- [[Java 언어 학습]]
- [[Python 학습과 패키지]]
- [[VS Code 사용법]]
- [[VS Code 추천 확장]] — C/C++·Copilot·Continue
- [[Cursor 사용법]]
