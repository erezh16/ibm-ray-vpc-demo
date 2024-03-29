# ibm-ray-vpc-demo
A small demo of model serving on CUDA using Ray, Hugging Face and PyTorch, intended for IBM VPC, but can also run on any Linux machine or Ray cluster. The model being served is GPT-2 (Hugging Face on PyTorch). This demo is based on Ray's Batching Tutorial: https://docs.ray.io/en/latest/serve/tutorials/batch.html . There is also a second demo app (CPU-only) of computing Pi.

## Installation
1. Clone the repo on a Linux machine that has GPU and CUDA. The demo will also run without either, but much slower.
2. Recommended: do the next steps in a Python virtual environment, e.g., pyenv-virtualenv, venv etc.
3. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Deploy the service:
    
    If you have a Ray cluster running (e.g., on IBM VPC), use its YAML file, e.g., `config.yaml`, as following: 
    ```
    ray submit config.yaml tutorial_batch.py
    ```
    If you're running on a stand-alone Linux machine, use:
    ```
    python tutorial_batch.py
    ```
    If you wish to deploy the Pi computation app, do the above commands replacing `tutorial_batch.py` with `ray-pi.py`
2. CUDA app only: to test the service, connect the test client:
    ```
    python batch_client.py
    ```
    Note: the client assumes connecting via localhost port 8000 using plain http. If you're using a remote Ray cluster, either make sure the port is open in the head node (risky - insecure) and modify the client, or set up an SSH tunnel(recommended). 


