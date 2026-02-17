"""
CDN 적용 여부 확인 결과

## 현재 상황
1. `.env` 파일에 R2 CDN 설정이 있음:
   - R2_CUSTOM_DOMAIN=https://assets.goal-runner.com

2. `settings.py`에서 R2 설정이 구성되어 있음:
   - AWS_S3_CUSTOM_DOMAIN이 설정됨
   - STORAGES 백엔드가 S3Boto3Storage로 설정됨

3. 하지만 실제 웹사이트에서는:
   - CSS와 JS 파일이 인라인으로 포함됨
   - `assets.goal-runner.com` 도메인이 사용되지 않음
   - `{% static %}` 태그가 렌더링되지 않음

## 문제 분석
웹사이트 https://map.goal-runner.com/portal/의 HTML을 분석한 결과:
- <link> 태그: 0개 (외부 CSS 파일 없음)
- <style> 태그: 3개 (인라인 CSS)
- <script> 태그: 3개 (인라인 JavaScript)

이것은 Django가 정적 파일을 **인라인으로 포함**하고 있다는 의미입니다.
템플릿에는 `{% static 'css/map_app.css' %}`와 `{% static 'js/map_app.js' %}`가 있지만,
실제 렌더링된 HTML에는 이 파일들이 외부 링크가 아닌 인라인 코드로 포함되어 있습니다.

## 결론
**R2 저장소의 CDN이 현재 적용되지 않고 있습니다.**

정적 파일이 인라인으로 포함되는 이유는 다음 중 하나일 수 있습니다:
1. Django 템플릿 프로세서가 정적 파일 내용을 직접 읽어서 인라인으로 삽입
2. 서버 측 미들웨어나 커스텀 템플릿 태그가 파일을 인라인화
3. 빌드 프로세스에서 정적 파일을 번들링/인라인화

## 권장 사항
CDN을 적용하려면:
1. 정적 파일을 R2에 업로드 (collectstatic 실행)
2. 템플릿에서 {% static %} 태그가 외부 URL을 생성하도록 설정 확인
3. 서버 재시작 및 배포
"""

print(__doc__)
