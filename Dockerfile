FROM ghcr.io/developmentseed/titiler:latest

USER root

# Create a dedicated non-root user and writable directories.
RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin appuser \
	&& mkdir -p /tmp/titiler \
	&& chown -R 10001:10001 /tmp/titiler /home/appuser

ENV PORT=8000
EXPOSE 8000

USER 10001