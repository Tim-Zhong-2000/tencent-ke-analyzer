import re


class Student(object):
    def __init__(self, key):
        self.key = key  # 腾讯课堂ID
        self.name_list = []  # 所有使用过的名称
        self.live_list = []  # 参与过的直播
        self.playback_list = []  # 参与过的回放

    def record_live(self, live):
        self.live_list.append(live)

    def record_playback(self, playback):
        self.playback_list.append(playback)

    def record_name(self, name):
        self.name_list.append(name)

    def get_key(self):
        return self.key

    # try to figure out the true name of the student
    def get_name(self):
        for i in range(len(self.name_list)):
            name_process = self._process_name(self.name_list[i])
            if name_process and name_process[1]:
                return str(name_process[1])
        return "获取姓名失败 腾讯课堂id:" + str(self.get_key())

    # try to figure out the true student_id of the student
    def get_student_id(self):
        for i in range(len(self.name_list)):
            name_process = self._process_name(self.name_list[i])
            if name_process and name_process[0] and len(name_process[0]) == 8:
                return str(name_process[0])
        return "获取学号失败 腾讯课堂id:" + str(self.get_key())

    def get_live_num(self):
        return str(len(self.live_list))

    def get_playback_num(self):
        return str(len(self.playback_list))

    def get_live_time(self):
        # use the live_list to cal
        return str(self._process_time(self.live_list))

    def get_playback_time(self):
        # use the playback_list to cal
        return str(self._process_time(self.playback_list))

    def _process_time(self, time_list):
        total_time = 0
        for i in range(len(time_list)):
            time_process = re.findall(r'(\d.*)分钟', time_list[i])
            if time_process:
                total_time += int(time_process[0])
        return total_time

    def _process_name(self, name):
        # 正常情况
        name_process_1 = re.findall(
            r'(\d{8,})\s*-*([\u4e00-\u9fa5 | a-z | A-Z].*)', name)
        if name_process_1:
            return [name_process_1[0][0], name_process_1[0][1]]
        # 名字学号写反
        name_process_2 = re.findall(
            r'([\u4e00-\u9fa5 | a-z | A-Z].*)\s*-*(\d{8,})', name)
        if name_process_2:
            return [name_process_2[0][1], name_process_2[0][0]]
        # 只写名字不写学号
        name_process_3 = re.findall(
            r'([\u4e00-\u9fa5 | a-z | A-Z].*)\s*', name)
        if name_process_3:
            return [0, name_process_3[0]]
        # 只写学号
        name_process_4 = re.findall(r'(\d{8,})\s*', name)
        if name_process_4:
            return [name_process_4[0], 0]
        return 0
