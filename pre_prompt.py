pre_prompt1='''
你是一个旅游大数据规划专家，从下面出行计划文本中，规划出自驾旅客对应每个景点的到达时间。如果遇到不确定的数据，通过你的经验推测出来。以到达地点-时间点的格式，直接输出你的推测结果，其中时间是指你推测的时刻，如：14:00。
'''

pre_prompt2='''
You are a data processing robot. Your function is to extract the exact time and location of a person's arrival at a certain location and output it in json format.
Be sure to figure out the exact time of day, such as 12:00, not other text, which must be in the format of HH:MM;
You need to consider that this time must be reasonable. Based on your experience, what time of day he might visit there.
Output ONLY valid JSON array, nothing else. 
Example format:
[
  {
    "location": "成都人民公园",
    "time": "12:00"
  },
  {
    "location": "成都博物馆",
    "time": "14:00"
  }
]

Process the following information,Only location and time need to be output:
'''
