#!/bin/bash

# .env 파일에서 환경 변수 로드
if [ -f /home/kxu45/.env ]; then
  export $(cat /home/kxu45/.env | xargs)
fi

# 새로운 환경에서 Docker 컨테이너 실행
cd /home/kxu45/
docker build -t alm_ser .

# 현재 실행 중인 애플리케이션을 중지
docker stop flask_alm || true
docker rm flask_alm || true

docker run -d --name flask_alm --restart always -p 5000:5000 alm_ser

# 사용되지 않는 Docker 이미지를 정리
docker system prune -a -f