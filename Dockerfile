FROM ubuntu:18.04

VOLUME /data
ENV CADDYPATH="/data/caddyssl"
COPY entrypoint.py /usr/bin

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential git python3 curl tar supervisor \
    && git clone https://github.com/solusipse/fiche.git \
    && chmod +x /usr/bin/entrypoint.py \
    && curl -LO https://github.com/kmahyyg/deblan_gist_dockered/releases/download/caddy/caddy.tar.bz2 \
    && tar xvfj caddy.tar.bz2 \
    && chmod +x caddy \
    && rm caddy.tar.bz2 \
    && mkdir -p /data/codes \
    && mkdir -p /data/caddyssl

WORKDIR /root/fiche

RUN make \
    && make install \
    && rm -rf /var/lib/apt/lists/*

CMD ["/usr/bin/entrypoint.py"]
