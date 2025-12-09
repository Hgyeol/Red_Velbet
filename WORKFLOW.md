# Git 브랜치 전략 및 작업 워크플로우

이 문서는 새로운 작업을 시작하고, 버전 관리하며, 최종적으로 프로젝트에 병합하는 전체 프로세스를 설명합니다. 모든 작업은 독립적인 브랜치에서 수행하는 것을 원칙으로 합니다.

## 1. 브랜치 생성 및 이동

새로운 작업을 시작하기 전, 메인 브랜치(예: `main` 또는 `master`)에서 최신 변경 사항을 받아온 후, 기능에 맞는 이름으로 새 브랜치를 생성하고 그 브랜치로 이동합니다.

```bash
# 메인 브랜치로 이동
git checkout main

# 원격 저장소의 최신 변경사항을 가져옴
git pull origin main

# 새로운 기능 브랜치 생성 및 이동
git checkout -b <branch-name>
```

- **브랜치 이름 규칙:** `feat/작업-요약`, `fix/문제-요약` 등 Type과 목적을 명시합니다.

## 2. 작업 수행

생성된 브랜치에서 요청된 작업을 성공적으로 완료합니다. 코드 수정, 파일 추가/삭제 등 모든 변경 사항이 포함됩니다.

## 3. 작업일지 작성 (`WORKLOG.md`)

`WORKLOG.md` 파일에 완료된 작업 내역을 기록합니다. 작업일지는 다음 형식을 따릅니다.

```markdown
### YYYY-MM-DD

- **브랜치:** `feat/login-feature`
- **작업 내용:** 로그인 기능 구현
- **변경 사항:**
  - `login.py`: 로그인 로직 추가
  - `user_model.py`: 사용자 모델 수정
- **특이 사항:** 없음
```

## 4. 변경사항 커밋 및 푸시

작업 내용과 작업일지를 Staging Area에 추가하고, 커밋 메시지와 함께 로컬 저장소에 기록한 후 원격 저장소에 푸시합니다.

```bash
# 변경된 모든 파일 추가
git add .

# 커밋
git commit -m "feat: [작업 요약] 작업 완료"

# 원격 저장소에 새로운 브랜치 푸시
git push origin <branch-name>
```

- **커밋 메시지 규칙:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore` 등의 접두사를 사용하여 커밋 목적을 명확히 합니다.

## 5. 병합 (Merge)

작업이 완료되고 변경 사항이 준비되면, 작업 브랜치에서 메인 브랜치로 로컬 병합을 수행합니다.

```bash
# 1. 메인 브랜치로 이동
git checkout main

# 2. 작업 브랜치의 변경 사항을 메인 브랜치로 병합 (fast-forward 또는 3-way merge)
git merge <branch-name>

# 3. 병합된 메인 브랜치를 원격 저장소에 푸시
git push origin main
```

## 6. 브랜치 삭제

병합이 완료된 작업 브랜치는 로컬과 원격 저장소에서 삭제하여 정리합니다.

```bash
# 로컬 브랜치 삭제
git branch -d <branch-name>

# 원격 브랜치 삭제
git push origin --delete <branch-name>
```

---
