import pandas as pd
import glob
import os

def methylation_array_sesame_integration(directory, output_file="test.csv"):
    files = glob.glob(directory + "/*.txt")
    print(files)
    dfs = []

    for file in files:
        df = pd.read_csv(file, sep="\t", header=None, names=["CpG", os.path.basename(file)], index_col=0)

        dfs.append(df)

    merged_df = pd.concat(dfs, axis=1)

    merged_df.to_csv(output_file)

    print(f"Files have been successfully merged into: {output_file}")



def integrateMrMcToDataFrame(directory, output_file="test.csv"):
    files = glob.glob(os.path.join(directory, "*.txt"))
    print(f"Number of files: {len(files)}")

    dfs = []

    for file in files:
        try:
            df = pd.read_csv(file, sep="\t", header=0)


            df["Source_File"] = os.path.basename(file)

            dfs.append(df)

        except Exception as e:
            print(f"Error occured during processing file {file}: {e}")

    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)
        merged_df.to_csv(output_file, index=False)
        print(f"Files have been successfully merged into: {output_file}")
    else:
        print("No valid files to proccess")





integrateMrMcToDataFrame(r"D:\pracav2D\TCGA-LGG\Transcriptome_Profiling\Gene Expression Quantification", output_file="test.csv")
# methylation_array_sesame_integration("D:\pracav2D\TCGA-LGG\DNA_Methylation\Methylation Beta Value")