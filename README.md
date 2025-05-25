### Usage

#### MLC installation

[Guide](https://docs.mlcommons.org/mlcflow/install)

#### Run Commands

To evaluate GATE CSE 2025 paper with OpenAI.

```
mlcr app,question,_gate --api_key=<sk-proj-...>
```

`--api_key`: The OpenAI API key

To evaluate GATE CSE 2025 paper with Gemini.

```
mlcr gemini-evaluation --api_key=<AIz...>
```

`--api_key`: The Gemini API key

To seperately download and parse the GATE Question Paper and Answer Key, to generate JSON file

```
mlcr parse-gate-question
```

(By default CS25 Set 2 paper and key is downloaded)

Optional tags:

```
--MLC_GATE_QUESTION_PDF_URL 
--MLC_GATE_ANSWER_PDF_URL
--MLC_GATE_OUTPUT_JSON_PATH
```