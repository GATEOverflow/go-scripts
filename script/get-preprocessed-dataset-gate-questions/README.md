### MLC installation

[Guide](https://docs.mlcommons.org/mlcflow/install)

### Download this repository

```
mlc pull repo gateoverflow@go-scripts
```

#### Run Commands

```
 mlcr get,dataset,original,gate-questions,_gatecse-2025 -j
[2025-04-14 17:02:47,664 module.py:575 INFO] - * mlcr get,dataset,original,gate-questions,_gatecse-2025
[2025-04-14 17:02:47,671 module.py:575 INFO] -   * mlcr download,file
[2025-04-14 17:02:47,672 module.py:1284 INFO] -        ! load /home/arjun/MLC/repos/local/cache/download-file_8c2ea479/mlc-cached-state.json
[2025-04-14 17:02:47,673 module.py:5113 INFO] -        ! cd /mnt/arjun/MLC/repos/gateoverflow@go-scripts/script/get-preprocessed-dataset-gate-questions
[2025-04-14 17:02:47,673 module.py:5114 INFO] -        ! call /home/arjun/MLC/repos/gateoverflow@go-scripts/script/get-dataset-gate-questions/run.sh from tmp-run.sh
[2025-04-14 17:02:47,682 module.py:5259 INFO] -        ! call "postprocess" from /home/arjun/MLC/repos/gateoverflow@go-scripts/script/get-dataset-gate-questions/customize.py
[2025-04-14 17:02:47,684 module.py:2195 INFO] - {
  "return": 0,
  "env": {
    "MLC_GATE_QUESTIONS_JSON_FILE_PATH": "/home/arjun/MLC/repos/local/cache/download-file_8c2ea479/questions.json"
  },
  "new_env": {
    "MLC_GATE_QUESTIONS_JSON_FILE_PATH": "/home/arjun/MLC/repos/local/cache/download-file_8c2ea479/questions.json"
  },
  "state": {},
  "new_state": {},
  "deps": [
    "download,file"
  ]
}
```
```
```

### WIP
```
mlcr get,preprocessed,dataset,gate-questions,_gatecse-2025 -j
```

The output here should be `MLC_PREPROCESSED_GATE_QUESTIONS_JSON_FILE_PATH` which contains `question_num`, `num_images` as additional keys and also any necessary formatting for the question content.

