FROM codait/max-base:v1.1.1

ARG model_bucket=http://max-assets.s3.us.cloud-object-storage.appdomain.cloud/pytorch/neuralstyle
ARG model_file=neuralstyle.tar.gz

WORKDIR /workspace

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=assets/${model_file} && \
  tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

# Conda is the preferred way to install Pytorch, but the Anaconda install pulls
# in non-OSS libraries with customized license terms, specifically CUDA and MKL.
#RUN conda update -n base conda
#RUN conda install -y pytorch-cpu torchvision -c pytorch

# pip install pytorch to avoid dependencies on MKL or CUDA
COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

# check file integrity
RUN md5sum -c md5sums.txt

EXPOSE 5000

CMD python app.py
