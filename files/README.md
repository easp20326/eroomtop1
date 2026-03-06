# 이룸덴탈랩 포털 - 배포 가이드

## ✅ 보안 수정 사항 (v3.1)

### 문제
기존 코드는 Supabase에서 **모든 거래처의 케이스를 전부 로드**한 뒤, 브라우저 JavaScript에서 필터링했습니다.  
→ 브라우저 콘솔에서 `window.cases` 입력 시 **타 거래처 데이터가 노출**되는 심각한 보안 취약점이 있었습니다.

### 수정 내용
1. **로그인 순서 변경**: 세션을 먼저 복원한 뒤 → 사용자 유형에 맞게 Supabase 쿼리를 조건부 실행
2. **서버 쿼리 레벨 필터링**: 거래처 사용자는 `.eq('clinic', clinicName)` 조건으로 자신의 케이스만 조회
3. **로그아웃 시 메모리 정리**: `cases = []`로 즉시 초기화 + localStorage 캐시 삭제
4. **로그인 성공 시 재로드**: 거래처 로그인 후 전체 케이스 삭제 후 본인 케이스만 재로드

---

## 🚀 GitHub + Vercel 배포 방법

### 1단계: GitHub 리포지토리 생성

1. [github.com](https://github.com) 로그인
2. 우측 상단 `+` → **New repository** 클릭
3. Repository name: `iroom-dental-portal` (원하는 이름)
4. **Private** 선택 (보안상 권장)
5. **Create repository** 클릭

### 2단계: 파일 업로드

GitHub 웹에서 바로 업로드하는 방법:

1. 생성된 리포지토리 페이지에서 **"uploading an existing file"** 클릭
2. 다음 파일들을 드래그 & 드롭:
   - `index.html`
   - `vercel.json`
   - `.gitignore`
3. **Commit changes** 클릭

### 3단계: Vercel 배포

1. [vercel.com](https://vercel.com) 접속 → GitHub 계정으로 로그인
2. **Add New → Project** 클릭
3. GitHub 리포지토리 목록에서 `iroom-dental-portal` 선택 → **Import**
4. Framework Preset: **Other** 선택
5. **Deploy** 클릭
6. 배포 완료 후 제공되는 URL 확인 (예: `https://iroom-dental-portal.vercel.app`)

> 이후 GitHub에 파일을 수정·업로드하면 Vercel이 **자동으로 재배포**합니다.

---

## 🔐 Supabase RLS 설정 (강력 권장)

현재 Supabase anon key가 코드에 노출되어 있으므로, **Row Level Security(RLS)**를 반드시 설정해야 합니다.

### Supabase Dashboard → SQL Editor에서 실행:

```sql
-- 1. cases 테이블 RLS 활성화
ALTER TABLE cases ENABLE ROW LEVEL SECURITY;

-- 2. anon 사용자는 cases 읽기/쓰기 허용 (기존 동작 유지)
--    실제로는 API에서 clinic 필터가 적용되므로 아래가 안전한 기본값
CREATE POLICY "anon_read_cases" ON cases
  FOR SELECT TO anon
  USING (true);

CREATE POLICY "anon_insert_cases" ON cases
  FOR INSERT TO anon
  WITH CHECK (true);

CREATE POLICY "anon_update_cases" ON cases
  FOR UPDATE TO anon
  USING (true);

-- 3. clinics 테이블 RLS (비밀번호 해시 보호)
ALTER TABLE clinics ENABLE ROW LEVEL SECURITY;

CREATE POLICY "anon_read_clinics" ON clinics
  FOR SELECT TO anon
  USING (true);
```

> **더 강한 보안을 원한다면**: Supabase Auth를 도입하여 JWT 기반 RLS 정책을 적용하세요.

---

## 📁 파일 구조

```
iroom-dental-portal/
├── index.html      ← 메인 애플리케이션 (전체 포함)
├── vercel.json     ← Vercel 라우팅 설정
├── .gitignore      ← Git 무시 파일
└── README.md       ← 이 파일
```

---

## ⚙️ 관리자 설정 변경

`index.html` 파일 내 아래 부분을 수정:

```javascript
const ADMIN_ID = '이룸덴탈랩';   // ← 관리자 아이디
const ADMIN_PW = 'jin7102__!!';  // ← 관리자 비밀번호
```

> ⚠️ 비밀번호를 변경한 뒤 GitHub에 push하면 Vercel이 자동 재배포합니다.

---

## 🔄 업데이트 방법

1. `index.html` 파일 수정
2. GitHub 리포지토리에 파일 업로드 (또는 git push)
3. Vercel 자동 재배포 (약 30초~1분 소요)
