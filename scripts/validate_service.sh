#!/bin/bash
# 서비스 상태 확인
curl -f http://localhost:5000 || exit 1
