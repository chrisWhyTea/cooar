from cooar.file import File


def download(session, file: File, **kwargs):
    with session.get(url=file.url, stream=True) as r:
        r.raise_for_status()
        with open(file.absolute_file_download_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    f.flush()
    file.absolute_file_download_path.rename(file.absolute_file_path)
