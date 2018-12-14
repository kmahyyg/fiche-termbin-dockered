FROM ubuntu:18.04

VOLUME /data
ENV CADDYPATH="/data/caddyssl"
COPY entrypoint.py /usr/bin

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential git python3 curl tar supervisor ca-certificates apt-utils \
    && git clone https://github.com/solusipse/fiche.git /root/fiche \
    && chmod +x /usr/bin/entrypoint.py \
    && curl -LO https://github.com/kmahyyg/deblan_gist_dockered/releases/download/caddy/caddy.tar.bz2 \
    && tar xvfj caddy.tar.bz2 \
    && chmod +x caddy \
    && rm caddy.tar.bz2 \
    && mkdir -p /data/codes \
    && mkdir -p /data/caddyssl

WORKDIR /root/fiche

EXPOSE 80
EXPOSE 443

RUN make \
    && make install \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

CMD ["/usr/bin/entrypoint.py"]
