import json
import os


class Zoom:
    @staticmethod
    def extractData():
        api_client = os.getenv("API_CLIENT", "ZOOM")
        if api_client == "ZOOM":
            # url = api_client + "_URL".format(
            #   year=timezone.now().year,
            #   month=timezone.now().month))
            # headers = {'Authorization': api_client + "_TOKEN",
            #            'Content-Type': 'application/json'
            #            }
            # response = requests.get(url, headers=headers)
            # data = json.loads(response.text)

            """ As demo paid accounts was not available,thus mocked up a few records looking at the API schema into JSON """
            try:
                json_data = open(os.getenv(api_client + "_REPORT_JSON"))
            except FileNotFoundError:
                return None
            api_response = json.load(json_data)
            json_data.close()
            return api_response['dates']
