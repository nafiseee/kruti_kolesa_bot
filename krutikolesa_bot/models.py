getting_sort = ['client_name','client_phone','act','bycycle_model','bycycle_id','iot_id']
class Work():
    def __init__(self,worker_id,worker_name):
        self.worker_id = worker_id
        self.worker_name = worker_name
        self.act = ''
        self.bycycle_model = ''
        self.bycycle_id = ''
        self.iot_id = ''

        self.works = {}
        self.spare_parts = []
        self.status = 'Ремонт не окончен'
        self.print_params = {}
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
        s = f"{'='*20}\nКлиентский ремонт\n"
        for i in getting_sort:
            if i in self.print_params:
                if self.print_params[i]:
                    s+=f"{self.print_params[i]} {getattr(self,i)}"
                else:
                    s+='____\n'
        return s
