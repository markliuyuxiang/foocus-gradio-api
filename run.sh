#!/bin/sh
while [ 1 ]; do
  python app.py --server_port $1 --share $2 --server $3

done