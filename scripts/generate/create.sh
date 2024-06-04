## Create total split from the indicvoices dataset
# LANGUAGE=("Tamil")
# LANG_CODE=("tam")
# LENGTH=${#LANGUAGE[@]}

# for ((i=0;i<LENGTH;i++)); do
#     python split.py --lang_code ${LANG_CODE[i]} \
#     --audio_file /slt/data/indicvoices/${LANGUAGE[i]}/v1a/ \
#     --output_dir /slt/data/indicvoices/${LANG_CODE[i]}  \
#     --manifest_dir /slt/emnlp_2024/experiments/dataset/${LANG_CODE[i]} 
# done


# LANGUAGE=("Tamil")
# LANG_CODE=("tam")
# LENGTH=${#LANGUAGE[@]}

# ## Create smaller splits from the indicvoices dataset
# for ((i=0;i<LENGTH;i++)); do
#     for duration in 20 10 5 2 1
#     do
#         python create_small_set.py \
#         --val_duration 1 \
#         --split train \
#         --train_duration ${duration} \
#         --lang_code ${LANG_CODE[i]} \
#         --audio_dir /slt/emnlp_2024/experiments/dataset/${LANG_CODE[i]} \
#         --target_dir /slt/emnlp_2024/experiments/dataset/${LANG_CODE[i]}_${duration}
#         cp /slt/emnlp_2024/experiments/dataset/${LANG_CODE[i]}/test_manifest.json /slt/emnlp_2024/experiments/dataset/${LANG_CODE[i]}_${duration}/test_manifest.json
#     done
# done

