FROM ghcr.io/actions/actions-runner:latest
COPY image /
USER root
RUN /build.sh
USER runner
CMD ["/home/runner/control.py"]

