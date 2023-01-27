FROM python:3.10.9

WORKDIR /app

COPY ./dist ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir *.whl

RUN rm *.whl *.tar.gz

ENTRYPOINT ["python", "-m", "synthetic_data.app"]
