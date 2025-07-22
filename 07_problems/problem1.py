a = 'level'

def is_plaindrome(word:str)->str:
    l=len(word)
    indexes = range(-1,-(l+1),-1)
    ans=""
    for i in indexes:
        ans=ans+word[i]
    return ans

def is_plaindrome(word:str)->bool:
    rev_word = rev_string(word)
    print(rev_word)

    if word == rev_word:
        return True
    else:
        return False
    
word = 'hello'
a = is_plaindrome(word)
print(a)
print(rev_string)