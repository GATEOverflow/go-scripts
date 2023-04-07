<details>
<summary>Click here to see the table of contents.</summary>

* [Usage](#usage)
  * [ CM installation](#cm-installation)
  * [ CM script automation help](#cm-script-automation-help)
  * [ CM CLI](#cm-cli)
  * [ CM Python API](#cm-python-api)
* [Customization](#customization)
  * [ Variations](#variations)
* [Maintainers](#maintainers)

</details>

___
### Usage

#### CM installation

[Guide](https://github.com/mlcommons/ck/blob/master/docs/installation.md)

#### CM script automation help

```cm run script --help```

#### CM CLI

`cm run script --tags=app,question-classification,topic-classification,go,question-topic(,variations from below) (flags from below)`

*or*

`cm run script "app question-classification topic-classification go question-topic (variations from below)" (flags from below)`

*or*

`cm run script f559634052574b50`

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


___
### Customization


#### Variations

  * *No group (any variation can be selected)*
    <details>
    <summary>Click here to expand this section.</summary>

    * `_rh`
      - Environment variables:
        - *CM_ML_MODEL_NAME*: `go_1`
      - Workflow:
        1. ***Read "deps" on other CM scripts***
           * get, ml-model, question-classification, go, qa, question-topic, _rh

    </details>
___
### Maintainers

* [GATEOverflow](https://github.com/orgs/GATEOverflow)
* [Arjun Suresh](https://github.com/arjunsuresh)
* [Anandhu S](https://github.com/anandhu-eng)