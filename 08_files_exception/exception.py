"""Once upon a time,
there was a brave knight,
who fought dragons."""

try:
    f1=open('/Users/olaoluwatunmise/fessopro/8_files_exception/story.txt')
    d = f1.read()
    print(d)
    print(100/0)

except:
    print('something went wrong')

print('This is very important line')
