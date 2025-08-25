class Work():
    def __init__(self,worker_id,worker_name):
        self.worker_id = worker_id
        self.worker_name = worker_name
        self.act = ''
        self.bycycle_model = ''
        self.bycycle_id = ''
        self.bycycle_state_id = ''
        self.iot_id = ''

        self.works = []
        self.spare_parts = []
        self.status = 'Ремонт не окончен'
        self.print_params = []
    def __str__(self):
        print('fdfdfddfdfffffffffffffffff')
        return str(dir(self))
class ClientWork(Work):
    def __init__(self,worker_id,worker_name):
        super().__init__(worker_id,worker_name)
        self.client_name = ''
        self.client_phone = ''
    def info(self):
        print(self.print_params)
        s = "-----------------------------------------------------\nКлиентский ремонт\n"
        for i in self.print_params:
            s+=i[1]
            print(s)
            if getattr(self, i[0]):
                s+=getattr(self, i[0])
            else:
                s+=' ____\n'
        return s
