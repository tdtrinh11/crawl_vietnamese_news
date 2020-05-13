label_list = {
    "CTXH":0,
    "DS":1,
    "GD":2,
    "KD":3,
    "KHCN":4,
    "PL":5,
    "SK":6,
    "TT":7,
    "VH":8,
    "XC":9
}

def present_label(label):
    label_vec = [0.0 for _ in range(len(label_list))]
    label_vec[label_list[label]] = 1.0
    return label_vec