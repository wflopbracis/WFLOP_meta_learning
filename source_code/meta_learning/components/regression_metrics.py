import os
import pandas as pd
import numpy as np
import sys
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

if len(sys.argv) != 2:
    print("Uso: python regression_metrics.py <label>")
    sys.exit(1)

label = sys.argv[1] 

models_path = f'result/{label}/models/theoretical_models/'
output_path = f'result/{label}/regression_metrics/'
os.makedirs(output_path, exist_ok=True)

l_values = [100, 50, 25, 10, 5]  
r_values = ["1.0", "0.5", "0.25", "0.1", "0.05"]

mse_table = pd.DataFrame(index=r_values, columns=l_values)
rmse_table = pd.DataFrame(index=r_values, columns=l_values)
mae_table = pd.DataFrame(index=r_values, columns=l_values)
mape_table = pd.DataFrame(index=r_values, columns=l_values)
r2_table = pd.DataFrame(index=r_values, columns=l_values)

os.makedirs(output_path, exist_ok=True)

#------------ BUILDING THE DATASET FOR RANDOM WALK ------------
print("-> Getting regression metrics for random walk")

for l in l_values:
    for r in r_values:
        vbs_path = os.path.join(models_path, f"l{l}_r{r}", "VBS", f"l{l}_r{r}_VBSModel.csv").replace("\\", "/")
        as_path = os.path.join(models_path, f"l{l}_r{r}", "AS" , f"l{l}_r{r}_ASModel.csv").replace("\\", "/")

        try:
            vbs_df = pd.read_csv(vbs_path)
            as_df = pd.read_csv(as_path)

            if "Instance" in vbs_df.columns and "VBS_Prediction" in vbs_df.columns and \
               "Instance" in as_df.columns and "AS_Prediction" in as_df.columns:

                merged_df = pd.merge(vbs_df, as_df, on="Instance")

                merged_df["VBS_Prediction"] = merged_df["VBS_Prediction"].astype(float)
                merged_df["AS_Prediction"] = merged_df["AS_Prediction"].astype(float)

                mse_value = mean_squared_error(merged_df["VBS_Prediction"], merged_df["AS_Prediction"])
                rmse_value = np.sqrt(mse_value)
                mae_value = mean_absolute_error(merged_df["VBS_Prediction"], merged_df["AS_Prediction"])
                
                valid_indices = merged_df["VBS_Prediction"] != 0
                mape_value = (np.abs((merged_df["VBS_Prediction"] - merged_df["AS_Prediction"]) / merged_df["VBS_Prediction"]))[valid_indices].mean() * 100
                
                r2_value = r2_score(merged_df["VBS_Prediction"], merged_df["AS_Prediction"])

                mse_table.at[r, l] = round(mse_value, 10)
                rmse_table.at[r, l] = round(rmse_value, 10)
                mae_table.at[r, l] = round(mae_value, 10)
                mape_table.at[r, l] = round(mape_value, 10) if not np.isnan(mape_value) else "Erro"
                r2_table.at[r, l] = round(r2_value, 10)

            else:
                raise ValueError("Colunas esperadas não encontradas nos arquivos.")

        except Exception as e:
            print(f"Error processing l={l}, r={r}: {e}")
            mse_table.at[r, l] = "Erro"
            rmse_table.at[r, l] = "Erro"
            mae_table.at[r, l] = "Erro"
            mape_table.at[r, l] = "Erro"
            r2_table.at[r, l] = "Erro"

#------------ BUILDING THE DATASET FOR ADAPTIVE WALK ------------
print("-> Getting regression metrics for adaptive walk")

adaptive_walk_mse_values = []
adaptive_walk_rmse_values = []
adaptive_walk_mae_values = []
adaptive_walk_mape_values = []
adaptive_walk_r2_values = []

for r in r_values:
    vbs_path = os.path.join(models_path, f"r{r}", "VBS", f"r{r}_VBSModel.csv").replace("\\", "/")
    as_path = os.path.join(models_path, f"r{r}", "AS" , f"r{r}_ASModel.csv").replace("\\", "/")

    try:
        vbs_df = pd.read_csv(vbs_path)
        as_df = pd.read_csv(as_path)

        if "Instance" in vbs_df.columns and "VBS_Prediction" in vbs_df.columns and \
               "Instance" in as_df.columns and "AS_Prediction" in as_df.columns:
            
            merged_df = pd.merge(vbs_df, as_df, on="Instance")

            merged_df["VBS_Prediction"] = merged_df["VBS_Prediction"].astype(float)
            merged_df["AS_Prediction"] = merged_df["AS_Prediction"].astype(float)

            mse_value = mean_squared_error(merged_df["VBS_Prediction"], merged_df["AS_Prediction"])
            rmse_value = np.sqrt(mse_value)
            mae_value = mean_absolute_error(merged_df["VBS_Prediction"], merged_df["AS_Prediction"])
            
            valid_indices = merged_df["VBS_Prediction"] != 0
            mape_value = (np.abs((merged_df["VBS_Prediction"] - merged_df["AS_Prediction"]) / merged_df["VBS_Prediction"]))[valid_indices].mean() * 100

            r2_value = r2_score(merged_df["VBS_Prediction"], merged_df["AS_Prediction"])

            adaptive_walk_mse_values.append(round(mse_value, 10))
            adaptive_walk_rmse_values.append(round(rmse_value, 10))
            adaptive_walk_mae_values.append(round(mae_value, 10))
            adaptive_walk_mape_values.append(round(mape_value, 10) if not np.isnan(mape_value) else "Erro")
            adaptive_walk_r2_values.append(round(r2_value, 10))

    except Exception as e:
        print(f"Error processing r={r}: {e}")
        adaptive_walk_mse_values.append("Erro")
        adaptive_walk_rmse_values.append("Erro")
        adaptive_walk_mae_values.append("Erro")
        adaptive_walk_mape_values.append("Erro")
        adaptive_walk_r2_values.append("Erro")

mse_table["Adaptive Walk"] = adaptive_walk_mse_values
rmse_table["Adaptive Walk"] = adaptive_walk_rmse_values
mae_table["Adaptive Walk"] = adaptive_walk_mae_values
mape_table["Adaptive Walk"] = adaptive_walk_mape_values
r2_table["Adaptive Walk"] = adaptive_walk_r2_values

for table in [mse_table, rmse_table, mae_table, mape_table, r2_table]:
    table.index = [f"{int(float(r) * 100)}%" for r in r_values]
    table.columns = [f"ℓ = {l}" for l in l_values] + ["Adaptive Walk"]
    table.index.name = "r"

mse_table.to_csv(os.path.join(output_path, "mse.csv"), float_format="%.10f")
rmse_table.to_csv(os.path.join(output_path, "rmse.csv"), float_format="%.10f")
mae_table.to_csv(os.path.join(output_path, "mae.csv"), float_format="%.10f")
mape_table.to_csv(os.path.join(output_path, "mape.csv"), float_format="%.10f")
r2_table.to_csv(os.path.join(output_path, "r2.csv"), float_format="%.10f")

