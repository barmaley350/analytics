# syntax=docker/dockerfile:1

FROM jupyter/minimal-notebook:x86_64-ubuntu-22.04

USER root

RUN apt-get update && apt-get install -y --no-install-recommends bash 
RUN pip install --upgrade pip --no-cache-dir
RUN pip install uv --no-cache-dir

USER jovyan

RUN uv pip install --system \ 
        psycopg2-binary \ 
        matplotlib \ 
        pandas \ 
        tabulate \
        openpyxl \
        clickhouse-connect \
        ipython-sql \
        fg-data-profiling \ 
        ipywidgets

RUN uv pip install --system "dask[complete]"

RUN uv pip install --system jupyter-resource-usage

RUN uv pip install --system memory_profiler        

RUN uv pip install --system polars

RUN uv pip install --system "chdb[pandas,pyarrow]"

# RUN uv pip install --system chdb-ds
RUN uv pip install --system ipython-autotime
RUN uv pip install --system pyarrow

COPY ./services/jupyter/jupyter_notebook_config.py /home/jovyan/.jupyter/



# #USER jovyan
# RUN mkdir /home/jovyan/work/db/