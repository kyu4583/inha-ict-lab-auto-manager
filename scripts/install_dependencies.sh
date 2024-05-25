#!/bin/bash

# Docker가 이미 설치되어 있는지 확인
if ! [ -x "$(command -v docker)" ]; then
  echo "Docker is not installed. Installing Docker..."

  # 기존 Docker 관련 패키지 제거
  sudo apt-get remove -y docker docker-engine docker.io containerd runc

  # 패키지 목록 업데이트
  sudo apt-get update

  # 필요한 패키지 설치
  sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

  # Docker GPG 키 추가
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

  # Docker 저장소 추가
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

  # 패키지 목록 다시 업데이트
  sudo apt-get update

  # Docker 설치
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io

  echo "Docker has been installed successfully."
else
  echo "Docker is already installed."
fi
