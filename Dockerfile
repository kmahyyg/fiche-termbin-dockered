FROM ubuntu:18.04 as builder

WORKDIR /root

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential git python3 curl tar ca-certificates apt-utils \
    && git clone https://github.com/solusipse/fiche.git /root/fiche \
    && curl -LO https://github.com/kmahyyg/deblan_gist_dockered/releases/download/caddy/caddy.tar.bz2 \
    && tar xvfj caddy.tar.bz2 \
    && chmod +x caddy

WORKDIR /root/fiche 

RUN make \
    && rm -rf /var/lib/apt/lists/*
    
FROM ubuntu:18.04 as runner

VOLUME /data
ENV CADDYPATH="/data/caddyssl"
COPY entrypoint.py /usr/bin

WORKDIR /root

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends python3 supervisor ca-certificates apt-utils \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /data/codes \
    && mkdir -p /data/caddyssl
    
COPY --from=builder /root/caddy .
COPY --from=builder /root/fiche/fiche .

EXPOSE 80
EXPOSE 443
EXPOSE 8989

CMD ["/usr/bin/python3","/usr/bin/entrypoint.py"]
