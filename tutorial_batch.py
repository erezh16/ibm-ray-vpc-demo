from typing import List

from starlette.requests import Request
from transformers import pipeline, Pipeline
import torch
from ray import serve
import time
import sys
import click

@serve.deployment(autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 3,
        "target_num_ongoing_requests_per_replica": 10,
    }, 
    ray_actor_options={"num_cpus": 0, "num_gpus": 1})
class BatchTextGenerator:
    def __init__(self, use_gpu):
        torch_device = -1
        if use_gpu and torch.cuda.is_available():
            torch_device = torch.cuda.current_device()
            torch.set_grad_enabled(False)
        print ("Device ", torch_device)
        self.model = pipeline("text-generation", "gpt2", device=torch_device)

    @serve.batch(max_batch_size=10)
    async def handle_batch(self, inputs: List[str]) -> List[str]:
        print("Our input array has length:", len(inputs))

        results = self.model(inputs)
        return [result[0]["generated_text"] for result in results]

    async def __call__(self, request: Request) -> List[str]:
        return await self.handle_batch(request.query_params["text"])

@click.command()
@click.option('--cpu', '-c',show_default=True, default=False, help=f'Execute using CPU', is_flag=True)
def builder(cpu):
    generator = BatchTextGenerator.bind(not cpu)
    handle = serve.run(generator)
    print("Deployed successfully")
    try:
        while True:
            # Block, letting Ray print logs to the terminal.
            time.sleep(10)

    except KeyboardInterrupt:
        print("Got KeyboardInterrupt, shutting down...")
        serve.shutdown()
        sys.exit()

if __name__ == '__main__':
    builder()