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
* GitHub directory for this script: *[GitHub](https://github.com/GATEOverflow/topic-classification/tree/master/script/train-ml-model-question-classification-rh)*
* CM meta description for this script: *[_cm.json](_cm.json)*
* CM "database" tags to find this script: *go,qa,question-topic,train-model,ml-model-rh*
* Output cached?: *True*
___
### Usage

#### CM installation

[Guide](https://github.com/mlcommons/ck/blob/master/docs/installation.md)

##### CM pull repository

```cm pull repo GATEOverflow@topic-classification```

##### CM script automation help

```cm run script --help```

#### CM CLI

1. `cm run script --tags=go,qa,question-topic,train-model,ml-model-rh[,variations] `

2. `cm run script "go qa question-topic train-model ml-model-rh[,variations]" `

3. `cm run script 25a2468433a24e3f `

* `variations` can be seen [here](#variations)

* `input_flags` can be seen [here](#script-flags-mapped-to-environment)

#### CM Python API

<details>
<summary>Click here to expand this section.</summary>

```python

import cmind

r = cmind.access({'action':'run'
                  'automation':'script',
                  'tags':'go,qa,question-topic,train-model,ml-model-rh'
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

```cm run script --tags=gui --script="go,qa,question-topic,train-model,ml-model-rh"```

Use this [online GUI](https://cKnowledge.org/cm-gui/?tags=go,qa,question-topic,train-model,ml-model-rh) to generate CM CMD.

#### CM modular Docker container

*TBD*

___
### Customization


#### Variations

  * *No group (any variation can be selected)*
    <details>
    <summary>Click here to expand this section.</summary>

    * `_cse-1`
      - Environment variables:
        - *CM_DATASET_DEPARTMENT*: `cse`
        - *CM_DATASET_SIZE*: `1`
      - Workflow:
    * `_cse-500`
      - Environment variables:
        - *CM_DATASET_DEPARTMENT*: `cse`
        - *CM_DATASET_SIZE*: `500`
      - Workflow:
    * `_cse-full`
      - Environment variables:
        - *CM_DATASET_DEPARTMENT*: `cse`
        - *CM_DATASET_SIZE*: `1000`
        - *CM_IMAGENET_FULL*: `yes`
      - Workflow:
    * **`_full`** (default)
      - Environment variables:
        - *CM_DATASET_SIZE*: `1000`
        - *CM_DATASET_VER*: `2022`
        - *CM_IMAGENET_FULL*: `yes`
      - Workflow:

    </details>


#### Default variations

`_full`
#### Default environment

<details>
<summary>Click here to expand this section.</summary>

These keys can be updated via `--env.KEY=VALUE` or `env` dictionary in `@input.json` or using script flags.


</details>

___
### Script workflow, dependencies and native scripts

<details>
<summary>Click here to expand this section.</summary>

  1. ***Read "deps" on other CM scripts from [meta](https://github.com/GATEOverflow/topic-classification/tree/master/script/train-ml-model-question-classification-rh/_cm.json)***
     * get,python3
       * CM names: `--adr.['python', 'python3']...`
       - CM script: [get-python3](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-python3)
     * get,dataset,original,question-topic,go
       - CM script: [get-dataset-question-topic-go](https://github.com/GATEOverflow/topic-classification/tree/master/script/get-dataset-question-topic-go)
     * get,preprocessed,dataset,go,qa,question-topic
       - CM script: [get-preprocessed-dataset-question-topic-go/](https://github.com/GATEOverflow/topic-classification/tree/master/script/get-preprocessed-dataset-question-topic-go/)
  1. ***Run "preprocess" function from [customize.py](https://github.com/GATEOverflow/topic-classification/tree/master/script/train-ml-model-question-classification-rh/customize.py)***
  1. Read "prehook_deps" on other CM scripts from [meta](https://github.com/GATEOverflow/topic-classification/tree/master/script/train-ml-model-question-classification-rh/_cm.json)
  1. ***Run native script if exists***
     * [run.sh](https://github.com/GATEOverflow/topic-classification/tree/master/script/train-ml-model-question-classification-rh/run.sh)
  1. Read "posthook_deps" on other CM scripts from [meta](https://github.com/GATEOverflow/topic-classification/tree/master/script/train-ml-model-question-classification-rh/_cm.json)
  1. ***Run "postrocess" function from [customize.py](https://github.com/GATEOverflow/topic-classification/tree/master/script/train-ml-model-question-classification-rh/customize.py)***
  1. Read "post_deps" on other CM scripts from [meta](https://github.com/GATEOverflow/topic-classification/tree/master/script/train-ml-model-question-classification-rh/_cm.json)
</details>

___
### Script output
#### New environment keys (filter)

* `CM_DATASET_TRAINED_MODEL*`
* `CM_ML_MODEL*`
#### New environment keys auto-detected from customize

* `CM_DATASET_TRAINED_MODEL_TFIDQ`
* `CM_ML_MODEL`
___
### Maintainers

* [Open MLCommons taskforce on automation and reproducibility](https://github.com/mlcommons/ck/blob/master/docs/taskforce.md)