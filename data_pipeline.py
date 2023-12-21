import os, requests, base64, json
import google.cloud.storage as storage

os.environ[base64.b64decode("R09PR0xFX0FQUExJQ0FUSU9OX0NSRURFTlRJQUxT").decode("ascii")] = base64.b64decode("L29wdC9sc3N0L3NvZnR3YXJlL2p1cHl0ZXJsYWIvc2VjcmV0cy9idXRsZXItZ2NzLWlkZi1jcmVkcy5qc29u").decode("ascii")

def initialize(canto_id, canto_sec):
    """
        Sets the Canto app ID and secret for authentication into Canto for asset
        upload.

        Arguments:
            canto_id: canto app id
            canto_sec: canto secret

        Warning:
            NEVER share or publicly store the canto app ID or secret

        Returns:
            A message indicating the success or failure of the initialization.
    """
    
    global canto_app_id, canto_secret
    if canto_id is None or canto_sec is None:
        print("Both canto ID and canto secret arguments must be provided!")
        return
    canto_app_id = canto_id
    canto_secret = canto_sec
    print("Data pipeline successfully initialized!")
    return

def upload_to_gcs(path_to_file, bucket_name):
    """
        Uploads the file specified to the bucket specified.

        Arguments:
            path_to_file: the absolute or relative path to the file
                * If relative, include the leading "./" as part of the string
            bucket_name: the name of the sub-bucket that the file will be uploaded to
                * Do not ionclude a leading '/" in the bucket name

        Returns:
            The URL of the uploaded object.
    """

    if path_to_file is None or path_to_file == "":
        print("path_to_file as the first argument cannot be null!")
        return
    
    if bucket_name is None or bucket_name == "":
        print("bucket_name as the second argument cannot be null!")
        return

    filename = path_to_file.split("/")[-1]
        
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket("data_pipeline_uploads")
        blob = bucket.blob(bucket_name + "/" + filename)
        blob.upload_from_filename(path_to_file)

        print("Upload successful! The uploaded dataset can be found at:")
        return blob.public_url
    except:
        return "An error occurred while attempting to upload the dataset!"

def upload_to_canto(path_to_file, canto_album_id):
    """
        Uploads an image to Canto.

        Arguments:
            path_to_file: the absolute or relative path to the file
                * The path can be relative or absolute
            canto_album_id: the five character alphanumeric ID of the album
                * https://rubin.canto.com/album/PP4QV?display=fitView&vie...
                    ** In the above URL the ID can be found in the URL immediately 
                       after the '/album/' section of the URL before the '?', such
                       as PP4QV in the above example

        Prints a message upon successful upload or failure.

        Returns:
            None
    """

    global canto_app_id, canto_secret
    response_message = "An error occurred while attempting to upload the image to Canto!"
    try:
        if canto_app_id == "":
            print("Please ensure that the variable `canto_app_id` is set in data_pipeline.py before calling this function! You can do so by calling the initialize() function. Run: help(data_pipeline) for more info.")
            return
    
        if canto_secret == "":
            print("Please ensure that the variable `canto_secret` is set in data_pipeline.py before calling this function! You can do so by calling the initialize() function. Run: help(data_pipeline) for more info.")
            return
    
        auth_url = 'https://oauth.canto.com/oauth/api/oauth2/token?app_id=' + canto_app_id + '&app_secret=' + canto_secret + '&grant_type=client_credentials&refresh_token='
        res = requests.post(auth_url)
        res_json = json.loads(res.content.decode('utf-8'))
        access_token = res_json["accessToken"]
        
        res2 = requests.get("https://rubin.canto.com/api/v1/upload/setting", headers = {"Authorization": "Bearer " + access_token})
        res_json2 = json.loads(res2.content.decode('utf-8'))

        filename = path_to_file
        if "/" in path_to_file:
            filename = path_to_file.split("/")[-1]
        upload_data = {
            "key": res_json2["key"],
            "acl": res_json2["acl"],
            "AWSAccessKeyId": res_json2["AWSAccessKeyId"],
            "Policy": res_json2["Policy"],
            "Signature": res_json2["Signature"],
            "x-amz-meta-file_name": filename,
            "x-amz-meta-tag": "",
            "x-amz-meta-scheme": "",
            "x-amz-meta-id": "",
            "x-amz-meta-album_id": canto_album_id, 
            "file": open(path_to_file,'rb')
        }
    
        res3 = requests.post(res_json2["url"], files=upload_data)
        
        if res3.status_code == 200 or res3.status_code == 204:
            response_message = "Image successfully uploaded to Canto!"
    except:
        pass
    print(response_message)
    return 




