FROM ghcr.io/developmentseed/titiler:latest

USER root

WORKDIR /opt/app
COPY app /opt/app/app

# Create a dedicated non-root user and writable directories.
RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin appuser \
	&& mkdir -p /tmp/titiler \
	&& chown -R 10001:10001 /tmp/titiler /home/appuser

ENV MODULE_NAME=app.main
ENV PORT=8000
EXPOSE 8000

USER 10001