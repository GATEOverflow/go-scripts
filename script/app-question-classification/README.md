<details>
<summary>Click here to see the table of contents.</summary>

* [Description](#description)
* [Information](#information)
* [Usage](#usage)
  * [ CM installation](#cm-installation)
  * [ CM script automation help](#cm-script-automation-help)
  * [ CM CLI](#cm-cli)
  * [ CM Python API](#cm-python-api)
  * [ CM GUI](#cm-gui)
  * [ CM modular Docker container](#cm-modular-docker-container)
* [Customization](#customization)
  * [ Variations](#variations)
  * [ Default environment](#default-environment)
* [Script workflow, dependencies and native scripts](#script-workflow-dependencies-and-native-scripts)
* [Script output](#script-output)
* [New environment keys (filter)](#new-environment-keys-(filter))
* [New environment keys auto-detected from customize](#new-environment-keys-auto-detected-from-customize)
* [Maintainers](#maintainers)

</details>

*Note that this README is automatically generated - don't edit! Use `README-extra.md` to add more info.*

### Description

#### Information

* CM GitHub repository: *[GATEOverflow@topic-classification](https://github.com/GATEOverflow/topic-classification/tree/master)*
* GitHub directory for this script: *[GitHub](https://github.com/GATEOverflow/topic-classification/tree/master/script/app-question-classification)*
* CM meta description for this script: *[_cm.json](_cm.json)*
* CM "database" tags to find this script: *app,question-classification,topic-classification,go,question-topic*
* Output cached?: *False*
___
### Usage

#### CM installation

[Guide](https://github.com/mlcommons/ck/blob/master/docs/installation.md)

##### CM pull repository

```cm pull repo GATEOverflow@topic-classification```

##### CM script automation help

```cm run script --help```

#### CM CLI

1. `cm run script --tags=app,question-classification,topic-classification,go,question-topic[,variations] `

2. `cm run script "app question-classification topic-classification go question-topic[,variations]" `

3. `cm run script f559634052574b50 `

* `variations` can be seen [here](#variations)

* `input_flags` can be seen [here](#script-flags-mapped-to-environment)

#### CM Python API

<details>
<summary>Click here to expand this section.</summary>

```python

import cmind

r = cmind.access({'action':'run'
                  'automation':'script',
                  'tags':'app,question-classification,topic-classification,go,question-topic'
                  'out':'con',
                  ...
                  (other input keys for this script)
                  ...
                 })

if r['return']>0:
    print (r['error'])

```

</details>


#### CM GUI

```cm run script --tags=gui --script="app,question-classification,topic-classification,go,question-topic"```

Use this [online GUI](https://cKnowledge.org/cm-gui/?tags=app,question-classification,topic-classification,go,question-topic) to generate CM CMD.

#### CM modular Docker container

*TBD*

___
### Customization


#### Variations

  * *No group (any variation can be selected)*
    <details>
    <summary>Click here to expand this section.</summary>

    * `_path.#`
      - Environment variables:
        - *CM_DATASET_PATH*: `#`
      - Workflow:
        1. ***Read "deps" on other CM scripts***
           * get, ml-model, question-classification, go, qa, question-topic, _rh
             - CM script: [get-ml-model-question-classification](https://github.com/GATEOverflow/topic-classification/tree/master/script/get-ml-model-question-classification)
    * **`_rh`** (default)
      - Environment variables:
        - *CM_ML_MODEL_NAME*: `go_1`
      - Workflow:
        1. ***Read "deps" on other CM scripts***
           * get, ml-model, question-classification, go, qa, question-topic, _rh
             - CM script: [get-ml-model-question-classification](https://github.com/GATEOverflow/topic-classification/tree/master/script/get-ml-model-question-classification)
    * `_rt`
      - Environment variables:
        - *CM_ML_MODEL_NAME*: `go_2`
      - Workflow:
        1. ***Read "deps" on other CM scripts***
           * get, ml-model, question-classification, go, qa, question-topic, _rt
             - CM script: [get-ml-model-question-classification](https://github.com/GATEOverflow/topic-classification/tree/master/script/get-ml-model-question-classification)
    * `_setfit_dataset_path.#`
      - Environment variables:
        - *CM_SETFIT_DATASET*: `#`
      - Workflow:
        1. ***Read "deps" on other CM scripts***
           * get, ml-model, question-classification, go, qa, question-topic, _rt
             - CM script: [get-ml-model-question-classification](https://github.com/GATEOverflow/topic-classification/tree/master/script/get-ml-model-question-classification)

    </details>


#### Default variations

`_rh`
#### Default environment

<details>
<summary>Click here to expand this section.</summary>

These keys can be updated via `--env.KEY=VALUE` or `env` dictionary in `@input.json` or using script flags.


</details>

___
### Script workflow, dependencies and native scripts

<details>
<summary>Click here to expand this section.</summary>

  1. ***Read "deps" on other CM scripts from [meta](https://github.com/GATEOverflow/topic-classification/tree/master/script/app-question-classification/_cm.json)***
     * get,dataset,original,question-topic,go
       - CM script: [get-dataset-question-topic-go](https://github.com/GATEOverflow/topic-classification/tree/master/script/get-dataset-question-topic-go)
     * get,preprocessed,dataset,go,qa,question-topic
       - CM script: [get-preprocessed-dataset-question-topic-go/](https://github.com/GATEOverflow/topic-classification/tree/master/script/get-preprocessed-dataset-question-topic-go/)
     * get,generic-python-lib,_datasets
       - CM script: [get-generic-python-lib](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-generic-python-lib)
     * get,generic-python-lib,_pandas
       - CM script: [get-generic-python-lib](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-generic-python-lib)
     * get,generic-python-lib,_numpy
       - CM script: [get-generic-python-lib](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-generic-python-lib)
     * get,generic-python-lib,_torch
       - CM script: [get-generic-python-lib](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-generic-python-lib)
     * get,generic-python-lib,_tqdm
       - CM script: [get-generic-python-lib](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-generic-python-lib)
     * get,generic-python-lib,_scikit-learn
       * CM names: `--adr.['scikit-learn']...`
       - CM script: [get-generic-python-lib](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-generic-python-lib)
  1. ***Run "preprocess" function from [customize.py](https://github.com/GATEOverflow/topic-classification/tree/master/script/app-question-classification/customize.py)***
  1. Read "prehook_deps" on other CM scripts from [meta](https://github.com/GATEOverflow/topic-classification/tree/master/script/app-question-classification/_cm.json)
  1. ***Run native script if exists***
     * [run.sh](https://github.com/GATEOverflow/topic-classification/tree/master/script/app-question-classification/run.sh)
  1. Read "posthook_deps" on other CM scripts from [meta](https://github.com/GATEOverflow/topic-classification/tree/master/script/app-question-classification/_cm.json)
  1. ***Run "postrocess" function from [customize.py](https://github.com/GATEOverflow/topic-classification/tree/master/script/app-question-classification/customize.py)***
  1. ***Read "post_deps" on other CM scripts from [meta](https://github.com/GATEOverflow/topic-classification/tree/master/script/app-question-classification/_cm.json)***
     * postprocess,question-classification
       - CM script: [postprocess-question-classification](https://github.com/GATEOverflow/topic-classification/tree/master/script/postprocess-question-classification)
</details>

___
### Script output
#### New environment keys (filter)

* `CM_DATASET_OUTPUT_MODEL*`
#### New environment keys auto-detected from customize

___
### Maintainers

* [Open MLCommons taskforce on automation and reproducibility](https://github.com/mlcommons/ck/blob/master/docs/taskforce.md)