# Data pipeline scripts

The name of this repo will likely change at some point.

This repo houses the various scripts and tools that can be used to transfer non-citSci data to the EDC. For citSci related tools see the `citizen_science_notebooks` repo.

**Important: The Jupyter notebook in this repo isn't intended to be used for actual data curation, it is only here to demonstrate usage and continued support of the notebook is not planned.**

## Getting Started

You will need the Canto app ID and Canto secret in order to use this script.

First, import and initialize the pipeline script:

```
import data_pipeline

data_pipeline.initialize("app ID", "app secret")
```

The pipeline script is self-documenting:

```
help(data_pipeline)
```

## Uploading files to Google Cloud Storage

Files of any type can be uploaded, including images.

Given a file that already exists in the RSP notebook filesystem:

```
url_to_uploaded_file = data_pipeline.upload_to_gcs("./some_data.json", "some_sub_bucket_name")
url_to_uploaded_file
```

## Uploading images to Canto

First, identify which album to upload the image to - this is a manual process and involves logging into the Canto platform and navigating to the target album.

Once on the webpage of the target album, take note of the URL, for example:

`https://rubin.canto.com/album/PP4QV?display=fitView&viewIndex=1&gSortingForward=false&gOrderProp=uploadDate&referenceTo=&from=fitView`

Remove everything after and including the `?` for clarity:

`https://rubin.canto.com/album/PP4QV`

The album ID is the top-level section of the URL, in this case `PP4QV`.

With the album ID, upload the image to Canto:

```
import data_pipeline
res = data_pipeline.upload_to_canto("./some_sciencey_image.jpg", "PP4QV")
```

**Unfortunately, the Canto API processes uploads asynchronously and does not provide any information about the URL of the upload. You will need to manually verify that the image has been uploaded.**