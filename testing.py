import math as m
for i in range(100):
    for j in range(10):
        accuracy = i + float((j + 1)/10)
        wpm = 100
        combo = 150
        log_combo =  m.log(combo, 10)
        exponentiated = pow(accuracy, m.log(accuracy, 10)) * log_combo * wpm
        print("%.1f = %.4f" % (accuracy, exponentiated))
# for i in range(100):
#     for j in range(10):
#         accuracy = i + float((j + 1)/10)
#         wpm = 80
#         combo = 100
#         log_wpm = m.log(wpm, 8)
#         function = pow(accuracy, log_wpm) * combo
#         print("%.2f = %.4f" % (accuracy, function))