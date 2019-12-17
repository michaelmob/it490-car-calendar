import os, sys, json, requests


def get_car(action, make, model, year, mileage):
  """
  Generic carmd requester
  """
  headers = {
    'content-type': 'application/json',
    'authorization': 'Basic ' + os.getenv('CARMD_API_KEY'),
    'partner-token': os.getenv('CARMD_PARTNER_TOKEN')
  }
  url = f'http://api.carmd.com/v3.0/{action}'
  params = f'?year={year}&make={make}&model={model}&mileage={mileage}'

  response = requests.get(url + params, headers=headers)
  return response.json()


def get_recalls(*args):
  """
  Get car recalls.
  """
  return get_car('recall', *args)


def get_maintenance(*args):
  """
  Get car maintenance.
  """
  return get_car('maint', *args)
