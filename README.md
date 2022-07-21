Service created to transform Azure Alerts JSON data and send it into Slack or/and Telegram.

### Requirements
Azure CLI: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli</br>
Azure Function Core Tools (v4): https://github.com/Azure/azure-functions-core-tools

### Local debug
1. Create file _local.settings.json_ and configure desired messengers
```
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "",
    "SLACK_TOKEN": "",
    "SLACK_CHANNEL": "",
    "TELEGRAM_TOKEN": "",
    "TELEGRAM_CHAT_ID": ""
  }
}
```
2. Run
```
func start
```

### Manual deployment
1. Create **Resource Group**, **Azure Storage Account** and **Azure Function App** (Python 3.9)
2. Add configuration variables into Azure Function App configuration
```
SLACK_TOKEN
SLACK_CHANNEL
```
or/and
```
TELEGRAM_TOKEN
TELEGRAM_CHAT_ID
```
3. Login into Azure
```
az login
```
4. Publish Azure Function App
```
func azure functionapp publish ${FUNCTION_NAME}
```

### How to use
##### Debug JSON
```
curl -d @json_data.txt http://${AZURE_FUNC_APP_DOMAIN}/api/sendMessage?code=${AZURE_FUNC_APP_KEY}&template=debug
```
##### Send message using "main" template
```
curl -d @json_data.txt http://${AZURE_FUNC_APP_DOMAIN}/api/sendMessage?code=${AZURE_FUNC_APP_KEY}&template=main
```

### Add new template
Just create new Jinja2 template in directory "_./SendMessage/render_templates_".
