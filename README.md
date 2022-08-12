# dlsproc
> Download Spanish procurement


One is better off checking the wiki, but this is Python code meant to download Spanish government's [Plataforma de contratación del sector público](https://contrataciondelestado.es) *metadata* (right now, it does **not** download any document).

## Install

`pip install dlsproc`

## How to use

The software can be exploited as a library or as *standalone* scripts. 

```python
### Scripts
```

For testing purposes one can download, e.g., [Outsiders contracts for 2018](https://contrataciondelsectorpublico.gob.es/sindicacion/sindicacion_1044/PlataformasAgregadasSinMenores_2018.zip) and then

`dlsproc_extend_parquet_with_zip.py`extends an existing [parquet](https://parquet.apache.org/) file with data extracted from a given *zip* file.
