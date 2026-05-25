# nf-sc2-data-summary
a data summary script to raggle output from nf-sc2 into the report format

## dependency
```
panda = 3.0.3
python >= 3.11
```

## Config file
There is an example file in example/config.toml
The script supports 4 types of input -- csv(with header), tsv(with header), tsv(without header) and plain txt seperate key and value with delimit.
The information required were showed in the config.toml example

## Run

```
#modify the sc2-data-summary.py file
#first input is path to the config file
#optional output path is the second input
collapse_info(
        "example/config.toml", output="example/summary_name_can_be_change.csv"
    )
```
