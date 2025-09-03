# OptiMUS

#### This repository contains a literature review and simple implementation of [OptiMUS: Optimization Modeling Using Solvers and large language models] (https://github.com/teshnizi/OptiMUS).

Papers regarding the project can be found at here:


- V0.1: [OptiMUS: Optimization Modeling Using mip Solvers and large language models](https://arxiv.org/pdf/2310.06116).

- V0.2: [OptiMUS: Scalable Optimization Modeling with (MI) LP Solvers and Large Language Models](https://arxiv.org/pdf/2402.10172).

- V0.3: [OptiMUS-0.3: Using Large Language Models to Model and Solve Optimization Problems at Scale](https://arxiv.org/abs/2407.19633).


This literature review heavily focuses on the V0.1 article.


## Problem Statement

Optimization problems are common in many fields such as operations, economics, engineering, and computer science. However, optimization modeling - transforming a business problem into a mathematical optimization problem - requires an expert knowledge. Therefore, automating optimization modeling would allow people who cannot afford an access to optimization experts to improve their work efficiency using optimization techniques. The paper (V0.1 article) explored the capabilities and limitations of large language models (LLMs) in optimization, aiming to extend an access to optimization across application domains.


## Key Contributions in the Paper

- They introduced a novel dataset, NLP4LP, consisting of 52 (currently 269) LP and MILP optimization problems. To construct the dataset, they introduced a standardized format to represent optimization problems in natural languages.

- They presented OptiMUS, an LLM-based agent to formulate and solve optimization problems.

- They developed techniques to improve the quality of OptiMUS, such as debugging, automated testing, and data augmentation.


#### You can download the dataset from [https://huggingface.co/datasets/udell-lab/NLP4LP](https://huggingface.co/datasets/udell-lab/NLP4LP).

Please note that NLP4LP is intended and licensed for research use only. The dataset is CC BY NC 4.0 (allowing only non-commercial use) and models trained using the dataset should not be used outside of research purposes.


## Methodology

OptiMUS starts with a structured description of the optimization problem, called SNOP, and a separate data file. It first transforms SNOP into (1) a mathematical formulation of the problem and (2) tests that check the validity of a purported solution. Afterwards, OptiMUS transforms the mathematical formulation into solver (e.g., Gurobi, CPLEX) code. It joins the solver code with the problem data to solve the problem. If the code raises an error or fails a
test, OptiMUS revises the code (debugging) and repeats until the problem is solved or maximum iterations are reached.

<img width="655" height="379" alt="Screenshot 2025-09-01 at 4 30 34 PM" src="https://github.com/user-attachments/assets/804ded22-1ead-4fea-af82-8f4b42630cd6" />

#### Left: Natural language of problem description, Right: SNOP (Source: https://arxiv.org/pdf/2310.06116)


### SNOP is no longer required, as the preprocesser converting natural languages to structured forms has been developed from the V0.2 article.


## Experiments

They evaluated OptiMUS on NLP4LP dataset and used GPT-3.5 and GPT-4 models for their experiments. For the experiments, they considered these five modes:

- Prompt (baseline): The problem is described in a few prompts and the LLM is asked to formulate the problem and write code to solve it using a given optimization solver.

- Prompt + Debug: In addition to the above, if the code raises syntax or runtime errors, the errors along with the code and the problem info are passed to the LLM, which is prompted to debug the code.

- Prompt + Debug + AutoTests: In addition to the above, when the code successfully runs and produces an output, automatically-generated tests are run to check the validity of the output.

- Prompt + Debug + Supervised Tests: Same as the above, except that the automatically-generated tests are all manually revised and fixed by experts if necessary.

- Prompt + Debug + Supervised Tests + Augmentation (OptiMUS): In addition to the above, each problem is rephrased using an LLM five times, and then the whole pipeline is applied to each of the rephrased versions independently.

They assessed the models based on two metrics: success rate (the ratio of outputs satisfying all constraints and finding the optimal solution) and execution rate (the ratio of generated codes that are executable and generate an output).

<img width="687" height="376" alt="Screenshot 2025-09-01 at 4 31 27 PM" src="https://github.com/user-attachments/assets/f9cbc11e-b35d-466a-a419-2d952728ae02" />

#### Success and Execution Rates of the Five Modes (Source: https://arxiv.org/pdf/2310.06116)

When using GPT-4, the success rate improves with each additional feature, and OptiMUS (Prompt + Debug + Supervised Test + Augmentation) achieves the highest success and execution rates among the five modes. However, with the weaker model (GPT-3.5), the results fluctuate across modes. Because GPT-3.5 makes errors more frequently than GPT-4, debugging or testing can increase the number of incorrect codes. However, augmentation (OptiMUS) significantly improves the success rate by giving the model multiple attempts to solve the problem with different rephrasings.


## Simple Implementation by Jaden Lee

As the article compared GPT-3.5 and GPT-4, I was curious about the performance of the newest model, GPT-5, on optimization modeling. Since there was an issue accessing the GPT-5 API, I used GPT-5-mini instead and compared it with GPT-4. From the NLP4LP dataset, I selected the first five instances as test sets. I applied the Prompt + Debug mode, and the performance was already strong enough that I did not proceed with additional methods such as AutoTests, Supervised Tests, or Augmentation.

#### For all five problems, both GPT-4 and GPT-5-mini achieved a 100% success rate.

<img width="1663" height="1003" alt="Picture1" src="https://github.com/user-attachments/assets/49f2c4f4-0650-438c-aa80-4f8314787865" />

#### Number of Errors by GPT Model (Source: Jaden Lee)

An interesting finding is that the debugging process caused by errors occurred as frequently, or even more often, with GPT-5-mini compared to GPT-4. This difference stems from the distinct purposes of the two models. GPT-4, as a high-performance general-purpose model, excels at solving complex problems, reasoning, and maintaining logical consistency. In contrast, GPT-5-mini is a lightweight and faster model, better suited for short responses, repetitive tasks, and simple code generation. This demonstrates that a higher model number does not necessarily mean superiority; rather, each model has its own appropriate use cases.


### The results of the tasks can be found in the repository.


## How Can We Expand OptiMUS to Transportation Problems?

1. #### Domain-Specific Structured Format:
Similar to SNOP, we can design a structured format tailored to transportation. Problem types can be categorized as Network Flow Optimization, Traffic Assignment, Fleet Assignment, Facility Location, Routing, and others. This taxonomy allows the system to recognize the nature of the problem and generate appropriate formulations automatically.

2. #### Problem-Type-Specific Solvers and Algorithms:
Each problem type can be mapped to the most suitable solver or algorithm. For example, routing problems can be linked to specialized graph algorithms (e.g., A*, K-shortest path) rather than generic MILP formulations. This reduces computation time and increases solution reliability, as the LLM does not need to explore unnecessary solution methods.

3. #### Integration with External APIs:
Transportation problems are highly dynamic, with conditions changing over time. By integrating real-time data sources such as Google Maps or Apple Maps APIs, the system can capture up-to-date travel times, congestion, and road closures. Incorporating these data into optimization models significantly improves realism and practical applicability.
