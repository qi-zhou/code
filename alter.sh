#!/bin/bash
TATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3
ES_HOST='172.16.3.233'
Q_BODY='{\'
TODAY=`date +%Y.%m.%d`
RES=`curl ${ES_HOST}:9200/logstash-${TODAY}/collectd/_search?pretty -d '{\
   "size" : 0,
   "query": {
    "bool": {
      "must":    { "match": { "type": "collectd" }},
      "must":    { "match": { "plugin": "load"  }}
      }
   }, 
   "aggs":{
      "recent_load": {
         "filter": { 
            "range": {
               "@timestamp" : {
                  "gte": "now-5m", 
                  "lte": "now"
                }
            }
         },
         "aggs": {
             "current_load": {
                "avg": {
                "field": "midterm"
                   }
             }
         }
      }
   }
}'`
echo $RES
load=`echo $RES |grep value | awk -F: '{print $NF}'`

echo $load
#echo $memory
#memory=`echo $memory_list |awk  '{print $NF}'`
#free=`echo $memory | awk '{printf("%d\n",$0+0.5)}'`
#if [ $free -gt 800000000 ];then
#    echo "TEST OK ,free is: $free "
#    exit $STATE_OK
#elif [ $free -gt 600000000 -a $free -lt 800000000 ];then
#    echo "TEST WARNING ,free is: $free"
#    exit $STATE_WARNING
#elif [ $free -lt 600000000 ];then
#    echo "TEST CRITICAL ,free is: $free"
#    exit $STATE_CRITICAL
#else
#    echo "UNKNOWN STATE"
#    exit $STATE_UNKNOWN
#fi
#

