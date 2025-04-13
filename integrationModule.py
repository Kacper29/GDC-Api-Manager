import pandas as pd
import glob
import os
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from scipy.stats import shapiro, anderson, normaltest




def methylation_beta_valueto_data_frame(directory, output_file="test.csv"):
    files = glob.glob(directory + "/*.txt")
    print(files)
    dfs = []

    for file in files:
        df = pd.read_csv(file, sep="\t", header=None, names=["CpG", os.path.basename(file)], index_col=0)

        dfs.append(df)

    merged_df = pd.concat(dfs, axis=1)

    merged_df.to_csv(output_file)

    print(f"Files have been successfully merged into: {output_file}")



def txt_to_df(directory, output_file="test.csv", scaler: str = None):
    files = glob.glob(os.path.join(directory, "*.txt"))
    print(f"Number of files: {len(files)}")

    dfs = []

    for file in files:
        try:
            df = pd.read_csv(file, sep="\t", header=0)


            df["Source_File"] = os.path.basename(file)

            dfs.append(df)

        except Exception as e:
            print(f"Error occured while processing {file}: {e}")

    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)
        merged_df.to_csv(output_file, index=False)
        print(f"Files have been successfully merged into: {output_file}")
    else:
        print("No valid files to proccess")


def tsv_to_df(folder_path: str, output_path: str = "połączone.tsv", scale: str = None):
    # scale should be set to: None, 'minmax', 'zscore' or 'robust'


    tsv_files = glob.glob(os.path.join(folder_path, "*.tsv"))
    dfs = []

    for file in tsv_files:
        try:
            df = pd.read_csv(file, sep='\t', comment='#', dtype=str)
            df['source'] = os.path.basename(file)
            dfs.append(df)
        except Exception as e:
            print(f"Error occured while reading {file}: {e}")

    if not dfs:
        print("No files found.")
        return

    merged_df = pd.concat(dfs, ignore_index=True)

    numeric_cols = merged_df.select_dtypes(include='object').columns
    numeric_cols = [col for col in numeric_cols if merged_df[col].str.replace('.', '', 1).str.isnumeric().all()]

    for col in numeric_cols:
        merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

    if scale == 'minmax':
        scaler = MinMaxScaler()
        merged_df[numeric_cols] = scaler.fit_transform(merged_df[numeric_cols])
    elif scale == 'zscore':
        scaler = StandardScaler()
        merged_df[numeric_cols] = scaler.fit_transform(merged_df[numeric_cols])
    elif scale == 'robust':
        scaler = RobustScaler()
        merged_df[numeric_cols] = scaler.fit_transform(merged_df[numeric_cols])



    merged_df.to_csv(output_path, sep='\t', index=False)
    print(f"Zapisano połączony plik do: {output_path}")







#
# tsvToDataframe(r"D:\pracav2D\TCGA-LGG\Copy_Number_Variation\Gene Level Copy Number", output_path="gene_leveltest.csv")
# #

#txtToDataFrame(r"D:\pracav2D\TCGA-LGG\Transcriptome_Profiling\Gene Expression Quantification", output_file="test.csv")
# methylationBetaValuetoDataFrame("D:\pracav2D\TCGA-LGG\DNA_Methylation\Methylation Beta Value", output_file="TestDoNormalizacji.csv")
df = pd.read_csv("gene_leveltest.csv", sep='\t')
print(df.head())
