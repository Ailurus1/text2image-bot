cd ..
docker build \
    --build-arg TG_TOKEN_ARG=$TG_TOKEN \
    --build-arg HF_TOKEN_ARG=$HF_TOKEN \
    -t text2image-bot:latest .
docker run text2image-bot:latest