FROM codait/max-base

ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/fast-neural-style-transfer/1.0
ARG model_file=assets.tar.gz

WORKDIR /workspace

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}
RUN tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

# Conda is the preferred way to install Pytorch, but the Anaconda install pulls
# in non-OSS libraries with customized license terms, specifically CUDA and MKL.
#RUN conda update -n base conda
#RUN conda install -y pytorch-cpu torchvision -c pytorch

# pip install pytorch to avoid dependencies on MKL or CUDA
RUN pip install http://download.pytorch.org/whl/cpu/torch-0.3.1-cp36-cp36m-linux_x86_64.whl &&\
    pip install torchvision


COPY . /workspace
RUN md5sum -c md5sums.txt # check file integrity

EXPOSE 5000

CMD python app.py
