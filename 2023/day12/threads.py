import threading

def iterate(num):
  for i in range(num):
    pass
  return num

if __name__ =="__main__":
  t1 = threading.Thread(target=iterate, args=(int(1073741824/4),))
  t2 = threading.Thread(target=iterate, args=(int(1073741824/4),))
  t3 = threading.Thread(target=iterate, args=(int(1073741824/4),))
  t4 = threading.Thread(target=iterate, args=(int(1073741824/4),))

  a = t1.start()
  t2.start()
  t3.start()
  t4.start()

  b = t1.join()
  t2.join()
  t3.join()
  t4.join()

  print("Done!", a, b)
