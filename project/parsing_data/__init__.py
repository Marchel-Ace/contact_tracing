
def rssi_to_meter(rssi):
    power = -69
    current_rssi = -rssi
    first_step = power - current_rssi 
    second_step = first_step / 20
    second_step = pow(10, second_step)
    return second_step

def parsing_timestamp(data):
    number = ""
    for x in range(len(data)+1):
        if int(x) % 2 != 0:
            number += data[x]
    return int(number)


async def seperate_data(list_data):
    new_list = []
    for x in list_data:
        try:
            payload = x.split('2c')
            unique_id = payload[0]
            timestamp = parsing_timestamp(payload[1])
            rssi = "".join([x for x in payload[2][1::2]][:2])
            new_list.append([unique_id, timestamp, rssi])
        except :
            continue
    return new_list


async def group_by_idx(seqs,idx=0,merge=True):
    d = dict()
    for seq in seqs:
        if isinstance(seq,tuple): seq_kind = tuple
        if isinstance(seq,list): seq_kind = list
        k = seq[idx]
        v = d.get(k,seq_kind()) + (seq[:idx]+seq[idx+1:] if merge else seq_kind((seq[:idx]+seq[idx+1:],)))
        d.update({k:v})
    return d

async def post_data(list_data, thingsapi):
    for key in list_data:
        msg = {
        'unique_id':key,
        'contact_time':0,
        'average_range': rssi_to_meter(int(list_data[key][0][1]))
        }
        count_meter = 1
        len_value = 0
        for timestamp, rssi in list_data[key]:
            meter = rssi_to_meter(int(rssi))
            if len_value != len(list_data[key])-1:
                next_timestamp = list_data[key][len_value+1][0]
                if next_timestamp - timestamp > 40:
                    thingsapi.send_telemetry(msg)
                    msg['contact_time'] = 0
                    msg['average_range'] = meter
                    count_meter += 1
                else:
                    msg['contact_time'] = next_timestamp - timestamp + msg['contact_time']
                    msg['average_range'] = meter + msg['average_range'] / count_meter
                    count_meter += 1
                len_value += 1
            else:
                if msg['contact_time'] != 0:
                    pass
                else:
                    msg['contact_time'] = 0
                    msg['average_range'] = meter
        thingsapi.send_telemetry(msg)
        