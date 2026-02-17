---
description: Cloudflare 통합 배포 (Workers Assets) 표준 가이드
---

이 프로젝트는 Cloudflare의 최신 통합 배포 방식(Workers Assets)을 따릅니다. 다른 프로젝트(audit, npl, bible, chemistry, church, valuation)와의 통일성을 위해 반드시 아래 지침을 준수하십시오.

### 1. 설정 파일 관리
- `wrangler.toml` 대신 **`wrangler.jsonc`** 형식을 사용합니다.
- 정적 자산(Static Assets) 경로는 `frontend` 폴더로 지정합니다.
  ```json
  "assets": {
    "directory": "frontend"
  }
}
```

### 2. 배포 명령어
- 절대로 `npx wrangler pages deploy` 명령어를 사용하지 마십시오.
- 반드시 **`npx wrangler deploy`** 명령어만 사용합니다.

### 3. API 엔드포인트 및 CORS
- 프런트엔드는 `https://api-map.goal-runner.com`을 기본 URL로 사용합니다.
- 백엔드 서버(PORT 8084)는 모든 오리진에 대해 CORS를 허용하도록 설정되어 있습니다.
- 모든 `/proxy/` 요청은 `window.GUNDAM_CONFIG.apiBase`가 붙은 절대 경로로 처리됩니다.
