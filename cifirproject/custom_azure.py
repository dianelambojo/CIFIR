from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = 'cifirstorage' # Must be replaced by your <storage_account_name>
    account_key = 'JqyShfPKPk/ZdhAAvDS+JVAiR63fe0mczAAuD8fcDsLL5MTCTvZgbbGjimZ7Nji+jcVjr+7YnmOv+AStIR/4tw==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None
