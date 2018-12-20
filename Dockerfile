FROM ubuntu:18.04 as builder

WORKDIR /root

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential git ca-certificates apt-utils \
    && git clone https://github.com/solusipse/fiche.git /root/fiche 

WORKDIR /root/fiche 

RUN make \
    && rm -rf /var/lib/apt/lists/*
    
FROM ubuntu:18.04 as runner

VOLUME /data
COPY entrypoint.py /usr/bin
COPY highl.py /usr/bin

WORKDIR /root

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends python3 python3-flask python3-pygments supervisor ca-certificates apt-utils \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /data/codes \
    && chmod +x /usr/bin/highl.py
    
COPY --from=builder /root/fiche/fiche .

EXPOSE 8988
EXPOSE 8989

CMD ["/usr/bin/python3","/usr/bin/entrypoint.py"]
