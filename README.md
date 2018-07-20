# Path RNN for Movie Recommendation

Code for paper [Chains of Reasoning over Entities, Relations, and Text using
Recurrent Neural Networks](https://arxiv.org/abs/1607.01426)

## Dependencies

- [torch](https://github.com/torch/torch7)
- [nn](https://github.com/torch/nn)
- [rnn](https://github.com/Element-Research/rnn)
- [optim](https://github.com/torch/optim)
- [cunn](https://github.com/torch/cunn) (optional: required if you train on GPU)


## Instructions for running the code

### Generate Train and Test Data
Data Source: [movieLens 1M](https://grouplens.org/datasets/movielens/1m/)

```shell
cd data
bash movie_data_format.sh
vim large_test_file.txt (because of the memory constraints you should add those large test files into "large_test_file")
python split_test_data.py
bash test_part_data_format.sh
```

### Train Model
```shell
cd ../run_scripts
bash train.sh ./config.sh
```

### Evaluation
```shell
cd ../eval
bash model_test.sh <mode_path> <gpu_id>
bash combine_result.sh
bash concat.sh
python resort.py total_combine.txt total_combine_sorted.txt
bash eval_socre.sh <sorted file path> <result save path>
```
