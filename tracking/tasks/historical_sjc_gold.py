from datetime import datetime
import json


from tracking.tasks.base import runner
import tracking.database as db

TASK_NAME="historical_sjc_gold"

# this should only be run once
@runner(TASK_NAME)
def run(**kwargs):
  # data got from https://www.pricedancing.com/SJC-SJC.1L-VND-chart-rAAvxj on 5th Nov 2022
  # with period = ALl and interval = 4M
  data = [{"c": 26740000,
           "t": "2009-09-01T00:00:00"},
          {"c": 26560000,
           "t": "2010-01-01T00:00:00"},
          {"c": 28950000,
           "t": "2010-05-01T00:00:00"},
          {"c": 36000000,
           "t": "2010-09-01T00:00:00"},
          {"c": 37790000,
           "t": "2011-01-01T00:00:00"},
          {"c": 46930000,
           "t": "2011-05-01T00:00:00"},
          {"c": 41800000,
           "t": "2011-09-01T00:00:00"},
          {"c": 43000000,
           "t": "2012-01-01T00:00:00"},
          {"c": 44520000,
           "t": "2012-05-01T00:00:00"},
          {"c": 46300000,
           "t": "2012-09-01T00:00:00"},
          {"c": 42900000,
           "t": "2013-01-01T00:00:00"},
          {"c": 38450000,
           "t": "2013-05-01T00:00:00"},
          {"c": 34780000,
           "t": "2013-09-01T00:00:00"},
          {"c": 35460000,
           "t": "2014-01-01T00:00:00"},
          {"c": 36530000,
           "t": "2014-05-01T00:00:00"},
          {"c": 35130000,
           "t": "2014-09-01T00:00:00"},
          {"c": 35070000,
           "t": "2015-01-01T00:00:00"},
          {"c": 34400000,
           "t": "2015-05-01T00:00:00"},
          {"c": 32700000,
           "t": "2015-09-01T00:00:00"},
          {"c": 34350000,
           "t": "2016-01-01T00:00:00"},
          {"c": 36390000,
           "t": "2016-05-01T00:00:00"},
          {"c": 36100000,
           "t": "2016-09-01T00:00:00"},
          {"c": 36880000,
           "t": "2017-01-01T00:00:00"},
          {"c": 36500000,
           "t": "2017-05-01T00:00:00"},
          {"c": 36440000,
           "t": "2017-09-01T00:00:00"},
          {"c": 36870000,
           "t": "2018-01-01T00:00:00"},
      {"c": 36730000,
       "t": "2018-05-01T00:00:00"},
      {"c": 36420000,
       "t": "2018-09-01T00:00:00"},
      {"c": 36400000,
       "t": "2019-01-01T00:00:00"},
      {"c": 42425000,
       "t": "2019-05-01T00:00:00"},
      {"c": 42500000,
       "t": "2019-09-01T00:00:00"},
      {"c": 48175000,
       "t": "2020-01-01T00:00:00"},
      {"c": 56925000,
       "t": "2020-05-01T00:00:00"},
      {"c": 55825000,
       "t": "2020-09-01T00:00:00"},
      {"c": 55475000,
       "t": "2021-01-01T00:00:00"},
      {"c": 57050000,
       "t": "2021-05-01T00:00:00"},
      {"c": 61300000,
       "t": "2021-09-01T00:00:00"},
      {"c": 70000000,
       "t": "2022-01-01T00:00:00"},
      {"c": 66250000,
       "t": "2022-05-01T00:00:00"},
      {"c": 67200000,
       "t": "2022-09-01T00:00:00"}]

  added_count = 0
  with db.connection() as conn:
    for d in data:
      price = d["c"]
      timestamp = datetime.strptime(d["t"], "%Y-%m-%dT%H:%M:%S")

      data = {"name": "sjc_gold_buy",
              "value": price,
              "type": "gold",
              "source": "www.pricedancing.com",
              "settings": json.dumps({"currency": "VND", "unit": "1luong", "mode": "historical"}),
              "timestamp": timestamp}
      conn.execute(*db.insert_sql("data", data))

      data = {"name": "sjc_gold_sell",
              "value": price,
              "type": "gold",
              "source": "www.pricedancing.com",
              "settings": json.dumps({"currency": "VND", "unit": "1luong", "mode": "historical"}),
              "timestamp": timestamp}
      conn.execute(*db.insert_sql("data", data))
      added_count+=1

  return {"items_added": added_count}

if __name__ == "__main__":
  run()
