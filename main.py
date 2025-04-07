
import gdcDownload

data = gdcDownload.GdcData()


data_type = ["Transcriptome Profiling", "Copy Number Variation"]
for i in data_type:
    data.FullFileRequest(data.casesByProjectID, "TCGA-LGG", i, 5)

