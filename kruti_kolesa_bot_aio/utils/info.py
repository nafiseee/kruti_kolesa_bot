client_work_keys = ['work_type', 'full_name', 'phone_number', 'act_id', 'b_model', 'b_id', 'iot_id']
client_work = ['', '', 'Номер телефона: ', 'Акт №', 'Модель велосипеда: ', 'Номер велосипеда: ', 'IoT: ']
async def info(state):
    data = await state.get_data()
    s = f"<b>Мастер:</b> {data['employer']} | {data['start_time']}\n\n"
    for q,w in enumerate(client_work_keys):
        if w in data:
            if client_work[q]:
                s+=f"<b>{client_work[q]}</b> {data[w]}\n"
            else:
                s+=f"<b>{data[w]}\n</b>"
    s+='\n<b>Выполненные работы:</b>\n'
    if data['works']==[]:
        for i in range(3):
            print('fdddddddddddddddddddd')
            s+='____________\n'
    else:
        for i in data['works']:
            if i not in data['works_count']:
                s+=f"{i}\n"
            else:
                if data['works_count'][i]==1:
                    s += f"{i}\n"
                else:
                    s += f"{i} ({data['works_count'][i]}x)\n"
    s+="\n<b>Запчасти:</b>\n"
    if data['spares']==[]:
        for i in range(3):
            print('fdddddddddddddddddddd')
            s+='____________\n'
        else:
            for i in data['spares']:
                if i not in data['works_count']:
                    s += f"{i}\n"
                else:
                    if data['works_count'][i] == 1:
                        s += f"{i}\n"
                    else:
                        s += f"{i} ({data['works_count'][i]}x)\n"

    else:
        for i in data['spares']:
            s+=f"{i}\n"
    s+=f"\n<b>Норма часы:</b> {sum(data['norm_time'])}👺"
    return s