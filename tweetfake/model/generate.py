import os
from collections import namedtuple
from typing import List

import cohere
from dotenv import load_dotenv


load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

GeneratedText = namedtuple("GeneratedText", ["text", "likelihood"])


def generate_text(prompt: str, temperature: float) -> List[GeneratedText]:
    response = co.generate(
        model='xlarge',
        prompt=prompt,
        max_tokens=80,
        temperature=temperature,
        stop_sequences=["\n"],
        num_generations=5,
        return_likelihoods='GENERATION',
    )

    gens = []
    likelihoods = []
    for gen in response.generations:
        gens.append(gen.text.strip("\n "))
        sum_likelihood = 0
        for t in gen.token_likelihoods:
            sum_likelihood += t.likelihood
        # Get sum of likelihoods
        likelihoods.append(sum_likelihood)

    return sorted(
        [GeneratedText(t, l) for t, l in zip(gens, likelihoods)],
        key=lambda x: -x.likelihood,
    )
