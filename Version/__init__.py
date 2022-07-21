import azure.functions as func

version = "0.0.1"


def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(version)
