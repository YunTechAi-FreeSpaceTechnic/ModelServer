# Quick start

```sh
# 首先 clone 下來
git clone --recurse-submodules https://github.com/YunTechAi-FreeSpaceTechnic/ModelServer.git

# 先登入 docker
export GHCR_PAT="Your Personal Access Token"
echo $GHCR_PAT | docker login ghcr.io -u xiaoxigua-1 --password-stdin

# 直接 docker-compose 或 docker compose 跑起來
docker-compose --env-file ./env/yuan.env up yuan_model
```
