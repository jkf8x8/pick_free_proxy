def write_logs(info):
    handler = open("./static/logs.txt",'a+')
    handler.write("error [{}]".format(info))
    handler.close()