#!/usr/bin/env python3
import os
from ez import ez_produce
from dotenv import load_dotenv  # Load environment variables from env file first
load_dotenv(os.getenv('AUTH_ENV', '../.env'))

data = {
  'action': 'oauth2_link',
  'year': '1000',
  'make': 'aaa',
  'model': 'bbb',
  'current_mileage': '100000',
  'weekly_mileage': '1000'
}

response = ez_produce('DATA', 'dmz-queue-rpc', data, is_rpc=True)
print(response)
