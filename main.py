
import gdcDownload

data = gdcDownload.GdcData()


data_type = ["Transcriptome Profiling"]
for i in data_type:
    data.full_file_request('cases.project.project_id', "TCGA-GBM", i, 20)

