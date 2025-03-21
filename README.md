# Quick start

## Clone repo

```sh
git clone --recurse-submodules https://github.com/YunTechAi-FreeSpaceTechnic/ModelServer.git
```

## Copy model

```sh
cp -r {YOUR_MODEL} model
```

## Build or Run

### Build docker

```sh
export MODEL_NAME={YOUR_MODEL_NAME}
docker build --build-arg MODEL=./model/ -t $MODEL_NAME:latest .
```

### Run

```sh
python server.py 0.0.0.0 6666
```

## Test

```sh
python ./tools/attack.py 0.0.0.0 6666
```
