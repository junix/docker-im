FROM erlang:17.5
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
