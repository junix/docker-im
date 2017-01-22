FROM erlang:17.5
ENV QIDA_ZK '192.0.2.1:2181,192.0.2.2:2181,192.0.2.3:2181,192.0.2.4:2181,192.0.2.5:2181'
ENV LECAI_ZK '192.0.2.101:2181,192.0.2.102:2181,192.0.2.103:2181'
ADD sources.list /etc/apt/sources.list
ADD bashrc /root/.bashrc
RUN set -xe \
&& apt-get update \
&& apt-get install -y --no-install-recommends vim-nox \
&& apt-get install -y --no-install-recommends git \
&& apt-get install -y --no-install-recommends curl \
&& apt-get install -y --no-install-recommends libsqlite3-0 \
&& apt-get clean \
&& apt-get autoclean
CMD ["/bin/bash"]
